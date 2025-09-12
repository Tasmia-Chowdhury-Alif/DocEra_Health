import stripe
from stripe.error import SignatureVerificationError
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from . import models, serializers
from patient.models import Patient
from doctor.models import Doctor, AvailableTime
from core.permissions import IsPatientOrAdmin
import logging


stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

class AppointmentViewset(viewsets.ModelViewSet):
    queryset = models.Appointment.objects.all().select_related('doctor', 'patient')  # Optimized N+1
    serializer_class = serializers.AppointmentSerializer
    permission_classes = [IsAuthenticated, IsPatientOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        patient_id = self.request.query_params.get("patient_id")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        return queryset.filter(patient__user=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsPatientOrAdmin])
    def create_online(self, request):
        """For online appointments: Create Stripe Checkout session. Frontend redirects to session.url."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if data['appointment_type'] != 'Online':
                return Response({"error": "Checkout only for online appointments."}, status=status.HTTP_400_BAD_REQUEST)
            doctor = data['doctor']
            amount = doctor.fee * 100  # Stripe uses cents
            patient = Patient.objects.get(user=request.user)

            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'bdt', 
                            'product_data': {'name': f'Appointment with Dr. {doctor.user.first_name} {doctor.user.last_name}'},
                            'unit_amount': amount, 
                        },
                        'quantity': 1,
                    }],
                    mode='payment',  # One-time payment
                    success_url=request.build_absolute_uri('/success?session_id={CHECKOUT_SESSION_ID}'),  # Frontend handle
                    cancel_url=request.build_absolute_uri('/cancel'),
                    metadata={
                        'patient_id': str(patient.id),
                        'doctor_id': str(doctor.id),
                        'time_id': str(data['time'].id),
                        'symptom': data['symptom'],
                    }, 
                    automatic_tax={'enabled': True},  # Tax handling
                )
                return Response({'session_id': session.id, 'session_url': session.url})
            
            except stripe.error.StripeError as e: 
                logger.error(f'Stripe error: {e}')
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        """Override: For offline, create directly + PDF logic. For online, error → use checkout."""
        data = request.data
        if data.get('appointment_type') == 'Online':
            return Response({"message": "Use /create-online/ for online payments."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Offline logic
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            appointment = serializer.save(patient=Patient.objects.get(user=request.user))
            appointment.appointment_status = 'Running'
            appointment.save()

            # send email for appointment confirmation with details
            
            return Response({'appointment': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @csrf_exempt
    @require_http_methods(["POST"])
    def stripe_webhook(self, request):
        """Webhook: On payment success, create appointment + email."""
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except ValueError:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except SignatureVerificationError:
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            if session['payment_status'] == 'paid':
                # Idempotency check
                if models.Appointment.objects.filter(stripe_session_id=session['id']).exists():
                    logger.info(f'Idempotent webhook for session {session["id"]}')
                    return JsonResponse({'status': 'idempotent'})
                
                metadata = session['metadata']
                try:
                    patient = get_object_or_404(Patient, id=metadata['patient_id'])
                    doctor = get_object_or_404(Doctor, id=metadata['doctor_id'])
                    time = get_object_or_404(AvailableTime, id=metadata['time_id'])
                    symptom = metadata['symptom']   

                except KeyError as e:  
                    logger.error(f'Missing metadata: {e}')
                    return JsonResponse({'error': 'Invalid metadata'}, status=400)

                appointment = models.Appointment.objects.create(
                    patient=patient, 
                    doctor=doctor, 
                    appointment_type='Online',
                    appointment_status='Pending', 
                    payment_status='paid',
                    stripe_session_id=session['id'], 
                    payment_intent_id=session.payment_intent,
                    symptom=symptom, 
                    time=time
                )
                logger.info(f'Created appointment {appointment.id} from session {session["id"]}')

        return JsonResponse({'status': 'success'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsPatientOrAdmin])
    def cancel_appointment(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment)
        if not serializer.data['can_cancel']:
            return Response({'error': 'This appointment cannot be canceled.'}, status=status.HTTP_400_BAD_REQUEST)
        appointment.cancel = True
        appointment.appointment_status = 'Cancelled'
        appointment.save()
        if appointment.appointment_type == 'Online' and appointment.payment_status == 'paid' and appointment.payment_intent_id:
            stripe.refund.create(payment_intent=appointment.stripe_session_id)
        return Response({'message': 'Appointment cancelled successfully'})
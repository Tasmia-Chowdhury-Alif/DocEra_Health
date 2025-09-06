from rest_framework import serializers
from . import models


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Designation
        fields = "__all__"


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = "__all__"


class AvailableTimeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.AvailableTime
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    designation = serializers.StringRelatedField(many=True)
    # this Hyperlink Related Field is working correctly . the view_name must be like 'fieldName-details'
    # designation = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='designation-detail')
    specialization = serializers.StringRelatedField(many=True)
    available_time = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Doctor
        fields = ('id', 'user', 'image', 'designation', 'specialization', 'available_time', 'fee', 'meet_link')

    def validate_fee(self, value):
        if value <= 0:
            raise serializers.ValidationError("Fee must be a positive integer.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(many=False)
    doctor = serializers.StringRelatedField()

    class Meta:
        model = models.Review
        fields = ('id', 'reviewer', 'doctor', 'body', 'created', 'rating')

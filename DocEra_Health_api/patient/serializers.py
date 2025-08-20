from rest_framework import serializers
from . import models 

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Patient
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required= True)
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password1 = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password1 != confirm_password :
            raise serializers.ValidationError({'error' : "Password Doesn't match"})
        elif models.User.objects.filter(email= email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        
        account = models.User(username= username, first_name= first_name, last_name= last_name, email= email)
        print(account)
        account.set_password(password1)
        account.is_active = False
        account.save()
        return account
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required= True)
    password = serializers.CharField(required= True)
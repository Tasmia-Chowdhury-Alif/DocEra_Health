from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

##################### Will be Uncommented in Production #########################################
    # def validate_email(self, value):
    #     if value and User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("This email is already in use.")
    #     return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data.get("email", ""),
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", ""),
                password=validated_data["password"],
            )
        except ValueError as e:
            raise serializers.ValidationError({"user": str(e)})
        return user


class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = models.Patient
        fields = ("user", "image", "mobile_no")

    def validate_mobile_no(self, value):
        if not re.match(r"^\+\d{10,14}$", value):
            raise serializers.ValidationError("Invalid mobile number format.")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)
        try:
            patient = models.Patient.objects.create(
                user=user,
                image=validated_data.get("image", None),
                mobile_no=validated_data["mobile_no"],
            )
        except Exception as e:
            user.delete()  # Rollback user creation if patient creation fails
            raise serializers.ValidationError({"patient": str(e)})
        return patient


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Patient
        fields = ("id", "user", "image", "mobile_no")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation["image"] = instance.image.url
        return representation

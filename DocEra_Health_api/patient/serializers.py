from rest_framework import serializers
from . import models
import re


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Patient
        fields = ("id", "user", "image", "mobile_no")

    def validate_mobile_no(self, value):
        if not re.match(r"^\+\d{10,14}$", value):
            raise serializers.ValidationError("Invalid mobile number format.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation["image"] = instance.image.url
        return representation

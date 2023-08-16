from django.contrib.auth import get_user_model
from rest_framework import serializers
import logging

log = logging.getLogger(__name__)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()

        return user

from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models
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


class AddBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookmarkModel
        fields = "__all__"
        read_only_fields = (
            "title",
            "description",
            "url_type",
            "image",
            "created",
            "updated",
            "collections",
        )


class AddToCollectionBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookmarkModel
        fields = (
            "title",
            "url",
            "collections",
        )
        read_only_fields = (
            "title",
            "url",
        )


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookmarkModel
        fields = "__all__"
        read_only_fields = (
            "title",
            "description",
            "url",
            "url_type",
            "image",
            "created",
            "updated",
            "collections",
        )


class BookmarkCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookmarkCollectionModel
        fields = "__all__"
        read_only_fields = (
            "created",
            "updated",
        )

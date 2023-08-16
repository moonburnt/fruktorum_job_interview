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


class AddToCollectionBookmarkSerializer(serializers.Serializer):
    bookmark_id = serializers.PrimaryKeyRelatedField(
        queryset=models.BookmarkModel.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["bookmark_id"].queryset = self.context["view"].get_queryset()

    # def validate_bookmark_id(self, data):
    #     if self.context["view"].get_queryset().filter(bookmark_id).first() is not None:
    #         raise serializers.ValidationError()

    # def validate(self, data):
    #     validated_data = super().validate(data)
    #     if not self.context["view"].get_queryset().filter(validated_data["bookmark_id"]).first():
    #         raise serializers.ValidationError(
    #             f"bookmark with id {validated_data['bookmark_id']} "
    #             "already exists in this collection"
    #         )

    #     return validated_data

    # class Meta:
    #     model = models.BookmarkModel
    #     fields = (
    #         "bookmark_id",
    #         "pk",
    #         "title",
    #         "url",
    #         "collections",
    #     )
    #     read_only_fields = (
    #         "title",
    #         "url",
    #         "collections",
    #     )

    # def validate_book


# class AddToCollectionBookmarkSerializer(serializers.Serializer):
#     bookmark_id = serializers.IntegerField()

#     def validate(self):
#         bookmark_id in


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

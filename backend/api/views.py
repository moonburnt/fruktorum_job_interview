from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from . import models


class CreateOnlyModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class IsUnauthenticated(BasePermission):
    def has_permission(self, request, view):
        return not (request.user and request.user.is_authenticated)


class CreateRetrieveListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class RegisterUserView(CreateOnlyModelViewSet):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = [IsUnauthenticated]
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return HttpResponseRedirect(redirect_to="/auth/login/")


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.BookmarkModel.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.AddBookmarkSerializer
        else:
            return super().get_serializer_class()


class BookmarkCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookmarkCollectionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.BookmarkCollectionModel.objects.all()


class BookmarkInCollectionViewSet(CreateRetrieveListDestroyViewSet):
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.BookmarkModel.objects.all()

    def get_queryset(self):
        if self.action == "create":
            return models.BookmarkModel.objects.filter(
                ~Q(collections=self.kwargs["collection_pk"])
            )
        else:
            return models.BookmarkModel.objects.filter(
                collections=self.kwargs["collection_pk"]
            )

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.AddToCollectionBookmarkSerializer
        else:
            return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.validated_data["bookmark_id"])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def perform_create(self, obj):
        obj.collections.add(self.kwargs["collection_pk"])

    def perform_destroy(self, instance):
        instance.collections.remove(self.kwargs["collection_pk"])

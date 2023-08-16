from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
import logging

log = logging.getLogger(__name__)


router = DefaultRouter()
router.register("auth/register", views.RegisterUserView)
router.register("bookmarks", views.BookmarkViewSet)
router.register("collections", views.BookmarkCollectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]

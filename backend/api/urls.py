from django.urls import path, include
from rest_framework_nested import routers
from . import views
import logging

log = logging.getLogger(__name__)


router = routers.DefaultRouter()
router.register("auth/register", views.RegisterUserView)
router.register("bookmarks", views.BookmarkViewSet)
router.register("collections", views.BookmarkCollectionViewSet)

bookmarks_in_collection_counter = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix="collections",
    lookup="collection",
)
bookmarks_in_collection_counter.register("bookmark", views.BookmarkInCollectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(bookmarks_in_collection_counter.urls)),
    path("auth/", include("rest_framework.urls")),
]

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .parser import process_bookmark
from api.models import BookmarkModel


@receiver(pre_save, sender=BookmarkModel)
def on_bookmark_save(sender, instance: BookmarkModel, **kwargs):
    process_bookmark(instance, save=False)

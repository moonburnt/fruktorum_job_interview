from django.db import models
from django.utils import timezone


class BookmarkCollectionModel(models.Model):
    # Because there was no requirement to restrict collection deletion to current
    # user - hold no references to any user
    title = models.TextField()
    description = models.TextField()

    created = models.DateTimeField(auto_now=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)


class BookmarkModel(models.Model):
    # Since new types can be added in future, we could implement these as a model
    WEBSITE = 1
    BOOK = 2
    ARTICLE = 3
    MUSIC = 4
    VIDEO = 5

    WEBSITE_CHOICES = (
        (WEBSITE, "Website"),
        (BOOK, "Book"),
        (ARTICLE, "Article"),
        (MUSIC, "Music"),
        (VIDEO, "Video"),
    )

    title = models.TextField()
    description = models.TextField()
    url = models.URLField(unique=True)
    url_type = models.PositiveSmallIntegerField(
        choices=WEBSITE_CHOICES,
        default=WEBSITE,
    )

    # Its unclear if we should cache image locally or use remote image url
    # For now, lets assume it expects us to cache things.
    # TODO: give image unique name, like UUID4+default name.
    # Probably via create/on change signal
    image = models.ImageField()

    collections = models.ManyToManyField(
        to=BookmarkCollectionModel,
        related_name="bookmarks",
    )

    created = models.DateTimeField(auto_now=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)

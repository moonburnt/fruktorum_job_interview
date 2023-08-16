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
    WEBSITE = "website"
    BOOK = "book"
    ARTICLE = "article"
    MUSIC = "music"
    VIDEO = "video"

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
    url_type = models.CharField(
        choices=WEBSITE_CHOICES,
        default=WEBSITE,
        max_length=10,
    )

    # Its unclear if we should cache image locally or use remote image url
    # Assuming it should be a link, for sake of simplicity and speed
    image = models.URLField()

    collections = models.ManyToManyField(
        to=BookmarkCollectionModel,
        related_name="bookmarks",
    )

    created = models.DateTimeField(auto_now=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)

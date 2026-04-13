
from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class ArtistProfile(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=120, blank=True)

    portrait = models.ImageField(upload_to="artist/portraits/", blank=True, null=True)

    short_bio = models.CharField(max_length=300, blank=True)
    biography = models.TextField(blank=True)
    statement = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)

    website_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    ecommerce_portal_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artist Profile"
        verbose_name_plural = "Artist Profile"

    def __str__(self) -> str:
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base = slugify(self.name)[:200] or "series"
            slug = base
            i = 2
            while Series.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Artwork(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    class Availability(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        RESERVED = "RESERVED", "Reserved"
        SOLD = "SOLD", "Sold"

    slug = models.SlugField(max_length=240, unique=True, blank=True)

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    availability = models.CharField(
        max_length=9, choices=Availability.choices, default=Availability.AVAILABLE
    )

    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    title = models.CharField(max_length=220)
    year = models.PositiveIntegerField(blank=True, null=True)

    technique = models.CharField(max_length=220, blank=True)
    support = models.CharField(max_length=120, blank=True)

    height_cm = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    width_cm = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    depth_cm = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )

    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField(blank=True)
    tags = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated tags. Example: flamenco, bull, abstract",
    )

    price_eur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    show_price = models.BooleanField(default=False)
    enquire_only = models.BooleanField(
        default=True,
        help_text="If true, show 'Enquire/Consult' instead of direct purchase even if price exists.",
    )

    # Optional: handy main image shortcut (you can also use first ArtworkImage by order)
    main_image = models.ImageField(upload_to="artworks/main/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base = slugify(self.title)[:200] or "artwork"
            slug = base
            i = 2
            while Artwork.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="artworks/gallery/")
    caption = models.CharField(max_length=250, blank=True)
    alt_text = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Artwork Image"
        verbose_name_plural = "Artwork Images"

    def __str__(self) -> str:
        return f"{self.artwork.title} (#{self.order})"
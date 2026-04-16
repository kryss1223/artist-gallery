
from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language


class ArtistProfile(models.Model):
    name = models.CharField(max_length=200)
    
    city_es = models.CharField(max_length=120, blank=True)
    city_en = models.CharField(max_length=120, blank=True)
    city_ja = models.CharField(max_length=120, blank=True)


    portrait = models.ImageField(upload_to="artist/portraits/", blank=True, null=True)

    short_bio_es = models.CharField(max_length=300, blank=True)
    short_bio_en = models.CharField(max_length=300, blank=True)
    short_bio_ja = models.CharField(max_length=300, blank=True)

    biography_es = models.TextField(blank=True)
    biography_en = models.TextField(blank=True)
    biography_ja = models.TextField(blank=True)

    statement_es = models.TextField(blank=True)
    statement_en = models.TextField(blank=True)
    statement_ja = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)

    website_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    ecommerce_portal_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def _translated(self, field_base: str) -> str:
        lang = (get_language() or "es").split("-")[0]

        value = getattr(self, f"{field_base}_{lang}", "")
        if value:
            return value

        value_es = getattr(self, f"{field_base}_es", "")
        if value_es:
            return value_es

        return ""

    @property
    def city(self):
        return self._translated("city")

    @property
    def short_bio(self):
        return self._translated("short_bio")

    @property
    def biography(self):
        return self._translated("biography")

    @property
    def statement(self):
        return self._translated("statement")
    
    class Meta:
        verbose_name = "Artist Profile"
        verbose_name_plural = "Artist Profile"

    def __str__(self) -> str:
        return self.name


class Series(models.Model):
    name_es = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    name_ja = models.CharField(max_length=200, blank=True)

    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description_es = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_ja = models.TextField(blank=True)

    display_order = models.PositiveIntegerField(default=0)
    def _translated(self, field_base: str) -> str:
        lang = (get_language() or "es").split("-")[0]

        value = getattr(self, f"{field_base}_{lang}", "")
        if value:
            return value

        value_es = getattr(self, f"{field_base}_es", "")
        if value_es:
            return value_es

        return ""

    @property
    def name(self):
        return self._translated("name")

    @property
    def description(self):
        return self._translated("description")
    class Meta:
        ordering = ["display_order", "name_es"]
        verbose_name = "Series"
        verbose_name_plural = "Series"
    

    def __str__(self) -> str:
        return self.name_es

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base = slugify(self.name_es)[:200] or "series"
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
    availability = models.CharField(max_length=9, choices=Availability.choices, default=Availability.AVAILABLE)

    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    title_es = models.CharField(max_length=220)
    title_en = models.CharField(max_length=220, blank=True)
    title_ja = models.CharField(max_length=220, blank=True)

    year = models.PositiveIntegerField(blank=True, null=True)

    technique_es = models.CharField(max_length=220, blank=True)
    technique_en = models.CharField(max_length=220, blank=True)
    technique_ja = models.CharField(max_length=220, blank=True)

    support_es = models.CharField(max_length=120, blank=True)
    support_en = models.CharField(max_length=120, blank=True)
    support_ja = models.CharField(max_length=120, blank=True)

    height_cm = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    width_cm = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    depth_cm = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])

    series = models.ForeignKey("Series", on_delete=models.SET_NULL, null=True, blank=True)

    description_es = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_ja = models.TextField(blank=True)

    tags = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated tags. Example: flamenco, bull, abstract",
    )

    price_eur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    show_price = models.BooleanField(default=False)
    enquire_only = models.BooleanField(default=True)

    main_image = models.ImageField(upload_to="artworks/main/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def _translated(self, field_base: str) -> str:
        lang = (get_language() or "es").split("-")[0]

        value = getattr(self, f"{field_base}_{lang}", "")
        if value:
            return value

        value_es = getattr(self, f"{field_base}_es", "")
        if value_es:
            return value_es

        return ""

    @property
    def title(self):
        return self._translated("title")

    @property
    def technique(self):
        return self._translated("technique")

    @property
    def support(self):
        return self._translated("support")

    @property
    def description(self):
        return self._translated("description")
    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self) -> str:
        return self.title_es

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base = slugify(self.title_es)[:200] or "artwork"
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
    
    caption_es = models.CharField(max_length=250, blank=True)
    caption_en = models.CharField(max_length=250, blank=True)
    caption_ja = models.CharField(max_length=250, blank=True)

    alt_text_es = models.CharField(max_length=250, blank=True)
    alt_text_en = models.CharField(max_length=250, blank=True)
    alt_text_ja = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def _translated(self, field_base: str) -> str:
        lang = (get_language() or "es").split("-")[0]

        value = getattr(self, f"{field_base}_{lang}", "")
        if value:
            return value

        value_es = getattr(self, f"{field_base}_es", "")
        if value_es:
            return value_es

        return ""

    @property
    def caption(self):
        return self._translated("caption")

    @property
    def alt_text(self):
        return self._translated("alt_text")
    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Artwork Image"
        verbose_name_plural = "Artwork Images"

    def __str__(self) -> str:
        return f"{self.artwork.title} (#{self.order})"
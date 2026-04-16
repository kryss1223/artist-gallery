from django.contrib import admin
from django.utils.html import format_html

from .models import ArtistProfile, Series, Artwork, ArtworkImage


@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "city_display", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "city_es", "city_en", "city_ja")

    def city_display(self, obj):
        return obj.city
    city_display.short_description = "City"


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name_display", "display_order")
    list_editable = ("display_order",)
    search_fields = ("name_es", "name_en", "name_ja")
    prepopulated_fields = {"slug": ("name_es",)}

    def name_display(self, obj):
        return obj.name
    name_display.short_description = "Name"


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 0
    fields = (
        "preview",
        "image",
        "caption_es",
        "caption_en",
        "caption_ja",
        "alt_text_es",
        "alt_text_en",
        "alt_text_ja",
        "order",
    )
    readonly_fields = ("preview",)
    ordering = ("order",)

    def preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:6px;" />',
                obj.image.url
            )
        return "-"

    preview.short_description = "Preview"


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = (
        "title_display",
        "status",
        "availability",
        "series",
        "is_featured",
        "display_order",
        "updated_at",
        "thumb",
    )
    list_filter = ("status", "availability", "series", "is_featured")
    search_fields = (
        "title_es", "title_en", "title_ja",
        "technique_es", "technique_en", "technique_ja",
        "support_es", "support_en", "support_ja",
        "description_es", "description_en", "description_ja",
        "tags",
    )
    list_editable = ("status", "availability", "is_featured", "display_order")
    prepopulated_fields = {"slug": ("title_es",)}
    inlines = [ArtworkImageInline]

    def title_display(self, obj):
        return obj.title
    title_display.short_description = "Title"

    def thumb(self, obj):
        img = obj.main_image
        if not img and obj.images.exists():
            img = obj.images.first().image
        if img:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:6px;" />',
                img.url
            )
        return "-"

    thumb.short_description = "Preview"
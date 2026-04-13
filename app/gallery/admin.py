from django.contrib import admin
from django.utils.html import format_html

from .models import ArtistProfile, Series, Artwork, ArtworkImage


@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "city")


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    list_editable = ("display_order",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 0
    fields = ("preview", "image", "caption", "alt_text", "order")
    readonly_fields = ("preview",)
    ordering = ("order",)

    def preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;" />', obj.image.url)
        return "-"


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "availability",
        "series",
        "is_featured",
        "display_order",
        "updated_at",
        "thumb",
    )
    list_filter = ("status", "availability", "series", "is_featured")
    search_fields = ("title", "technique", "support", "tags", "description")
    list_editable = ("status", "availability", "is_featured", "display_order")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ArtworkImageInline]

    def thumb(self, obj):
        img = obj.main_image
        if not img and obj.images.exists():
            img = obj.images.first().image
        if img:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;" />', img.url)
        return "-"
    thumb.short_description = "Preview"
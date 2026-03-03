from django.shortcuts import get_object_or_404, render
from .models import ArtistProfile, Artwork, Series

def home(request):
    artist = ArtistProfile.objects.filter(is_active=True).first()
    featured = (
        Artwork.objects.filter(status=Artwork.Status.PUBLISHED)
        .order_by("display_order", "-created_at")[:12]
    )
    return render(request, "gallery/home.html", {"artist": artist, "featured": featured})


def artworks_list(request):
    qs = Artwork.objects.filter(status=Artwork.Status.PUBLISHED).select_related("series")
    series_slug = request.GET.get("series")
    if series_slug:
        qs = qs.filter(series__slug=series_slug)
    qs = qs.order_by("display_order", "-created_at")
    series = Series.objects.all()
    return render(request, "gallery/artworks_list.html", {"artworks": qs, "series": series, "series_slug": series_slug})


def artwork_detail(request, slug):
    artwork = get_object_or_404(
        Artwork.objects.filter(status=Artwork.Status.PUBLISHED).prefetch_related("images").select_related("series"),
        slug=slug,
    )
    return render(request, "gallery/artwork_detail.html", {"artwork": artwork})


def series_list(request):
    series = Series.objects.all()
    return render(request, "gallery/series_list.html", {"series": series})


def series_detail(request, slug):
    s = get_object_or_404(Series, slug=slug)
    artworks = (
        Artwork.objects.filter(status=Artwork.Status.PUBLISHED, series=s)
        .order_by("display_order", "-created_at")
        .select_related("series")
    )
    return render(request, "gallery/series_detail.html", {"series": s, "artworks": artworks})
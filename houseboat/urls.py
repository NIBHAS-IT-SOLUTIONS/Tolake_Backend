from django.urls import path, include
from rest_framework.routers import DefaultRouter
from houseboat.views import (
    HouseboatViewSet,
    ServiceViewSet,
    PackageViewSet,
    ComplementaryServiceViewSet,
    ContactInquiryViewSet,
    BookingViewSet,
    ReviewViewSet,
    booking_form_view,
    booking_success_view,
    contact_form_view,
    contact_success_view,
    check_availability,
    houseboats_embed_view  # ✅ HTML for WordPress
)

from django.views.decorators.csrf import csrf_exempt

# ✅ Set up REST Framework router
router = DefaultRouter()
router.register('Houseboats', HouseboatViewSet)
router.register('services', ServiceViewSet)
router.register('Packages', PackageViewSet)
router.register('Complementary-services', ComplementaryServiceViewSet, basename='complementaryservice')
router.register('Bookings', BookingViewSet)
router.register('Contact-inquiries', ContactInquiryViewSet)
router.register('Reviews', ReviewViewSet)

# ✅ Define URL patterns
urlpatterns = [
    # API Endpoints
    path('', include(router.urls)),

    # Form views (for WordPress or direct submissions)
    path('booking/', csrf_exempt(booking_form_view), name='booking_form'),
    path('booking-success/', booking_success_view, name='booking_success'),
    path('contact/', csrf_exempt(contact_form_view), name='contact_form'),
    path('contact-success/', contact_success_view, name='contact_success'),

    # AJAX/JS availability check
    path('check-availability/', check_availability, name='check_availability'),it

    # Iframe-based WordPress embed
    path('houseboats_embed/', houseboats_embed_view, name='houseboats_embed'),
]

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
    houseboats_embed_view  # ✅ Include this for the HTML view
)

from django.views.decorators.csrf import csrf_exempt

# ✅ Create router and register viewsets
router = DefaultRouter()
router.register('Houseboats', HouseboatViewSet)
router.register('services', ServiceViewSet)
router.register('Packages', PackageViewSet)
router.register('Complementary-services', ComplementaryServiceViewSet, basename='complementaryservice')
router.register('Bookings', BookingViewSet)
router.register('Contact-inquiries', ContactInquiryViewSet)
router.register('Reviews', ReviewViewSet)

# ✅ Main URL patterns
urlpatterns = [
    # Include API endpoints from router
    path('', include(router.urls)),

    # Booking and Contact Form views (if used separately)
    path('booking/', csrf_exempt(booking_form_view), name='booking_form'),
    path('booking-success/', booking_success_view, name='booking_success'),
    path('contact/', csrf_exempt(contact_form_view), name='contact_form'),
    path('contact-success/', contact_success_view, name='contact_success'),

    # Custom availability checker
    path('check-availability/', check_availability, name='check_availability'),

    # ✅ HTML card view for embedding in WordPress
    path('houseboats_embed/', houseboats_embed_view, name='houseboats_embed'),
]
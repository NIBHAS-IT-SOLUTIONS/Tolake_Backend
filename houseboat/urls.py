from django.urls import path, include
from rest_framework.routers import DefaultRouter
from houseboat.views import (HouseboatViewSet,ServiceViewSet,PackageViewSet,ComplementaryServiceViewSet,ContactInquiryViewSet,BookingViewSet,
    ReviewViewSet,
    booking_form_view,
    booking_success_view,
    contact_form_view,
    contact_success_view,
    check_availability,
)

# ✅ Create a single router instance
router = DefaultRouter()

# ✅ Register all API ViewSets
router.register('Houseboats', HouseboatViewSet)
router.register('services', ServiceViewSet)
router.register('Packages', PackageViewSet)
router.register('Complementary-services', ComplementaryServiceViewSet, basename='complementaryservice')
router.register('Bookings', BookingViewSet)
router.register('Contact-inquiries', ContactInquiryViewSet)
router.register('Reviews', ReviewViewSet)

# Main URL patterns
urlpatterns = [
    # Include all API endpoints
    path('', include(router.urls)),

    #  Booking form endpoints
    path('booking/', booking_form_view, name='booking_form'),
    path('booking-success/', booking_success_view, name='booking_success'),

    #  Contact form endpoints
    path('contact/', contact_form_view, name='contact_form'),
    path('contact-success/', contact_success_view, name='contact_success'),

    #  Availability checking endpoint
    path('check-availability/', check_availability, name='check_availability'),
]

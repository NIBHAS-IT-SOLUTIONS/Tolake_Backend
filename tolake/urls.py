from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.static import serve

from houseboat.views import (
    booking_success_view,
    contact_success_view,
    houseboats_embed_view
)

# Simple welcome page
def home_view(request):
    return HttpResponse("✅ Welcome to the Tolake API! Visit <code>/houseboat/</code> for available endpoints.")

urlpatterns = [
    path('', home_view),  # Root path

    # Admin panel
    path('admin/', admin.site.urls),

    # App URLs
    path('houseboat/', include('houseboat.urls')),

    # JWT Authentication
    path('houseboat/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('houseboat/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Booking and contact success pages
    path('booking-success/', booking_success_view, name='root_booking_success'),
    path('contact-success/', contact_success_view, name='root_contact_success'),

    # Embedded houseboats view for WordPress iframe
    path('houseboat/houseboats_embed/', houseboats_embed_view, name='houseboats_embed'),

    # Serve favicon from staticfiles (place favicon.ico inside /static)
    re_path(r'^favicon\.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': settings.STATIC_ROOT,
    }),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

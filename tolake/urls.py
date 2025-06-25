# tolake/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from houseboat.views import booking_success_view

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

    # Booking success page (if used in WordPress or redirect)
    path('booking-success/', booking_success_view, name='root_booking_success'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

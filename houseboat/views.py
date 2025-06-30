from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from datetime import datetime

from .models import (
    Houseboat, Service, Packages, Review, ComplementaryService,
    ContactInquiry, Booking, FAQ
)

from .serializers import (
    HouseboatSerializer, ServiceSerializer, PackageSerializer,
    ReviewSerializer, ComplementaryServiceSerializer,
    ContactInquirySerializer, BookingSerializer, FAQSerializer
)

from .forms import BookingForm, ContactInquiryForm

# -------------------- API ViewSets -------------------- #

class HouseboatViewSet(ModelViewSet):
    queryset = Houseboat.objects.all()
    serializer_class = HouseboatSerializer
    permission_classes = [AllowAny]


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]


class PackageViewSet(ModelViewSet):
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [AllowAny]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        houseboat = serializer.validated_data['houseboat']
        email = serializer.validated_data.get('email', None)

        if email and Review.objects.filter(houseboat=houseboat, email=email).exists():
            raise serializer.ValidationError("You have already reviewed this houseboat.")

        if self.request.user.is_authenticated:
            serializer.save(
                name=self.request.user.get_full_name() or self.request.user.username,
                email=self.request.user.email
            )
        else:
            serializer.save()


class ComplementaryServiceViewSet(ReadOnlyModelViewSet):
    queryset = ComplementaryService.objects.filter(is_active=True)
    serializer_class = ComplementaryServiceSerializer
    permission_classes = [AllowAny]


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        package_name = request.data.get('package_name')
        package = Packages.objects.filter(name=package_name).first() if package_name else None

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user if request.user.is_authenticated else None

        booking = serializer.save(
            user=user,
            package=package,
            total_price=package.Price if package else 0
        )

        headers = self.get_success_headers(serializer.data)

        try:
            send_mail(
                'New Houseboat Booking',
                f'Booking from user_name {booking.user.username if booking.user else "Anonymous"} '
                f'for houseboat_name {booking.houseboat.name}.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL]
            )
        except Exception as e:
            print(f"Admin email sending failed: {e}")

        if booking.user and booking.user.email:
            try:
                send_mail(
                    'Booking Confirmation',
                    'Thank you for booking. Your booking is confirmed.',
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.user.email]
                )
            except Exception as e:
                print(f"User confirmation email failed: {e}")

        return Response(serializer.data, status=201, headers=headers)


class ContactInquiryViewSet(ModelViewSet):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        inquiry = serializer.save()
        try:
            send_mail(
                'New Contact Inquiry',
                f'Inquiry from {inquiry.name} ({inquiry.email}): {inquiry.message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL]
            )
            send_mail(
                'Inquiry Received',
                f'Thank you for your inquiry, {inquiry.name}. We will get back to you soon.',
                settings.DEFAULT_FROM_EMAIL,
                [inquiry.email]
            )
        except Exception as e:
            print(f"Contact inquiry email failed: {e}")


class FaqViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

# -------------------- HTML View: Houseboats Embed -------------------- #

def houseboats_embed_view(request):
    houseboats = Houseboat.objects.filter(is_available=True)
    return render(request, 'houseboat/houseboats_embeded.html', {'houseboats': houseboats})

# -------------------- Booking Form Views -------------------- #

def booking_form_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.total_price = booking.package.Price if booking.package and booking.package.Price else 0
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'houseboat/booking_form.html', {'form': form})


def booking_success_view(request):
    return render(request, 'houseboat/booking_success.html')

# -------------------- Contact Inquiry Form Views -------------------- #

def contact_form_view(request):
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            try:
                send_mail(
                    'New Contact Inquiry',
                    f'Inquiry from {inquiry.name} ({inquiry.email}): {inquiry.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL]
                )
                send_mail(
                    'Inquiry Received',
                    f'Thank you for your inquiry, {inquiry.name}. We will get back to you soon.',
                    settings.DEFAULT_FROM_EMAIL,
                    [inquiry.email]
                )
            except Exception as e:
                print(f"Email sending error in contact form: {e}")
            return redirect('contact_success')
    else:
        form = ContactInquiryForm()
    return render(request, 'houseboat/contact_form.html', {'form': form})


def contact_success_view(request):
    return render(request, 'houseboat/contact_success.html')

# -------------------- Availability Checker -------------------- #

@api_view(['GET'])
def check_availability(request):
    houseboat_name = request.query_params.get('houseboat')
    check_in = request.query_params.get('check_in')
    check_out = request.query_params.get('check_out')

    if not all([houseboat_name, check_in, check_out]):
        return Response({'error': 'Missing parameters: houseboat, check_in, check_out'}, status=400)

    try:
        check_in_date = datetime.fromisoformat(check_in)
        check_out_date = datetime.fromisoformat(check_out)
        if check_out_date <= check_in_date:
            return Response({'error': 'Check-out must be after check-in'}, status=400)
    except ValueError:
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

    try:
        houseboat = Houseboat.objects.get(name=houseboat_name)
    except Houseboat.DoesNotExist:
        return Response({'error': 'Houseboat not found'}, status=404)

    overlapping = Booking.objects.filter(
        houseboat=houseboat,
        status='confirmed',
        check_in__lt=check_out,
        check_out__gt=check_in
    )

    if overlapping.exists():
        return Response({
            'available': False,
            'message': f'{houseboat_name} is not available from {check_in} to {check_out}.'
        })

    return Response({
        'available': True,
        'message': f'{houseboat_name} is available from {check_in} to {check_out}.'
    })

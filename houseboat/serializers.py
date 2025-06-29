from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Houseboat,
    Service,
    Booking,
    Packages,
    Review,
    SeasonalPrice,
    ComplementaryService,
    ContactInquiry,
    FAQ,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ComplementaryServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplementaryService
        fields = ['id', 'complementary_service', 'is_active']


class HouseboatSerializer(serializers.ModelSerializer):
    houseboat_name = serializers.CharField(source='name', read_only=True)
    image = serializers.ImageField()
    complementary_services = serializers.SlugRelatedField(
        many=True,
        queryset=ComplementaryService.objects.all(),
        slug_field='complementary_service'
    )

    class Meta:
        model = Houseboat
        fields = [
            'id',
            'houseboat_name',
            'slug',
            'image',
            'capacity',
            'bedrooms',
            'location',
            'price',
            'price_per_day',
            'category',
            'is_available',
            'complementary_services',
            'amenities',
            'description',
        ]


class ServiceSerializer(serializers.ModelSerializer):
    houseboats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Service
        fields = [
            'id',
            'service',
            'description',
            'price',
            'houseboats',
            'is_active'
        ]


class PackageSerializer(serializers.ModelSerializer):
    houseboat = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Houseboat.objects.all()
    )

    class Meta:
        model = Packages
        fields = [
            'id',
            'package',
            'slug',
            'houseboat',
            'description',
            'price',
            'max_guests',
            'duration',
        ]


class BookingSerializer(serializers.ModelSerializer):
    houseboat_name = serializers.CharField(source='houseboat.name', read_only=True)
    service_name = serializers.CharField(source='Service.service', read_only=True)
    package_name = serializers.CharField(source='Package.package', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    houseboat = serializers.SlugRelatedField(
        queryset=Houseboat.objects.all(),
        slug_field='name'
    )
    service = serializers.SlugRelatedField(
        queryset=Service.objects.all(),
        slug_field='service'
    )
    package = serializers.SlugRelatedField(
        queryset=Packages.objects.all(),
        slug_field='package',
        required=False,
        allow_null=True
    )
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    complementary_services = serializers.SlugRelatedField(
        many=True,
        queryset=ComplementaryService.objects.all(),
        slug_field='complementary_service',
        required=False
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'user', 'user_name',
            'houseboat', 'houseboat_name',
            'service', 'service_name',
            'package', 'package_name',
            'check_in', 'check_out',
            'total_guests', 'total_price',
            'status',
            'name', 'email', 'phone', 'address',
            'complementary_services',
            'category'
        ]
        read_only_fields = ['id', 'total_price']

    def validate(self, data):
        overlapping = Booking.objects.filter(
            houseboat=data['houseboat'],
            check_in__lt=data['check_out'],
            check_out__gt=data['check_in']
        )
        if self.instance:
            overlapping = overlapping.exclude(id=self.instance.id)
        if overlapping.exists():
            raise serializers.ValidationError("This houseboat is already booked for the selected dates.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    houseboat_name = serializers.CharField(source='houseboat.name', read_only=True)
    user_name = serializers.CharField(source='User', read_only=True)

    houseboat = serializers.SlugRelatedField(
        queryset=Houseboat.objects.all(),
        slug_field='slug'
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='user_name'
    )

    class Meta:
        model = Review
        fields = [
            
            'user','user_name',
            'houseboat', 'houseboat_name',
            'rating',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user_name', 'houseboat_name', 'created_at', 'updated_at']
    



class SeasonalPriceSerializer(serializers.ModelSerializer):
    houseboat_name = serializers.CharField(source='houseboat.name', read_only=True)

    class Meta:
        model = SeasonalPrice
        fields = [
            'id',
            'houseboat',
            'houseboat_name',
            'start_date',
            'end_date',
            'discounted_price',
            'is_active'
        ]


class ContactInquirySerializer(serializers.ModelSerializer):
    houseboat = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Houseboat.objects.all()
    )

    class Meta:
        model = ContactInquiry
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'message',
            'houseboat',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'id',
            'question',
            'answer',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class ComplementaryService(models.Model):
    complementary_service = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.complementary_service

    class Meta:
        ordering = ['complementary_service']
        verbose_name = "complementary_service"
        verbose_name_plural = "complementary_services"


class Houseboat(models.Model):
    CATEGORY_CHOICES = [
        ('luxury', 'Luxury'),
        ('deluxe', 'Deluxe'),
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('budget', 'Budget'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='standard')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='houseboat_images/', null=True, blank=True)
    bedrooms = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.CharField(max_length=500, null=True, blank=True)
    complementary_services = models.ManyToManyField(
        ComplementaryService, blank=True, related_name='houseboats'
    )
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            similar_slugs = Houseboat.objects.filter(slug__startswith=base_slug).count()
            if similar_slugs:
                self.slug = f"{base_slug}-{similar_slugs + 1}"
            else:
                self.slug = base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        ordering = ['name']


class Service(models.Model):
    service = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    houseboat = models.ManyToManyField(Houseboat, related_name='services')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.service

    class Meta:
        ordering = ['service']


class Packages(models.Model):
    PACKAGE_CHOICES = [
        ('overnight', 'Overnight'),
        ('honeymoon', 'Honeymoon'),
        ('night_stay', 'Night Stay'),
        ('day_cruise', 'Day Cruise'),
        ('group', 'Group'),
    ]

    package = models.CharField(max_length=100, choices=PACKAGE_CHOICES, default='day_cruise')
    slug = models.SlugField(unique=True, blank=True)
    houseboat = models.ForeignKey(Houseboat, on_delete=models.CASCADE, related_name='packages')
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(help_text="Duration in hours")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.houseboat.name}-{self.get_package_display()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_package_display()} Package"

    class Meta:
        ordering = ['package']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    CATEGORY_CHOICES = [
        ('luxury', 'Luxury'),
        ('deluxe', 'Deluxe'),
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('budget', 'Budget'),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    houseboat = models.ForeignKey(Houseboat, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Packages, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    complementary_services = models.ManyToManyField(ComplementaryService, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    total_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out must be after check-in.")

    def __str__(self):
        return f"Booking by {self.name or self.user.username} for {self.houseboat.name}"

    class Meta:
        ordering = ['-check_in']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    houseboat = models.ForeignKey(Houseboat, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}★"

    class Meta:
        ordering = ['-created_at']


class SeasonalPrice(models.Model):
    houseboat = models.ForeignKey(Houseboat, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.houseboat.name} ({self.start_date} to {self.end_date})"

    class Meta:
        ordering = ['start_date']


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveIntegerField(unique=True)
    houseboat = models.ForeignKey(Houseboat, on_delete=models.CASCADE, related_name='inquiries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name} for {self.houseboat.name}"

    class Meta:
        ordering = ['-created_at']


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_at']

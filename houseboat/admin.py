from django.contrib import admin
from .models import Houseboat, Service, Booking, Packages, ComplementaryService

@admin.register(Houseboat)
class HouseboatAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'is_available')  # changed from 'houseboat'
    list_filter = ('is_available',)
    search_fields = ('name', 'location')  # changed from 'houseboat'
    ordering = ['name']  # changed from 'houseboat'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'houseboat', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status',)
    search_fields = ('user__username', 'houseboat__name')
    ordering = ['-check_in']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service', 'description', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('service', 'description')
    ordering = ['service']

@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('package', 'houseboat', 'price', 'max_guests', 'duration')
    search_fields = ('package', 'description')
    ordering = ['package']

@admin.register(ComplementaryService)
class ComplementaryServiceAdmin(admin.ModelAdmin):
    list_display = ('complementary_service', 'is_active')
    list_filter = ('complementary_service',)
    search_fields = ('complementary_service',)
    ordering = ['complementary_service']

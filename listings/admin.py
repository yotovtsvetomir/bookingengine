from django.contrib import admin

from .models import Listing, HotelRoomType, HotelRoom, Reservation, BookingInfo


class HotelRoomTypeInline(admin.StackedInline):
    model = HotelRoomType
    extra = 1
    show_change_link = True


class ReservationInline(admin.StackedInline):
    model = Reservation
    extra = 1
    show_change_link = True


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    inlines = [HotelRoomTypeInline, ReservationInline]
    list_display = (
        'title',
        'listing_type',
        'country',
        'city',
    )
    list_filter = ('listing_type',)


class HotelRoomInline(admin.StackedInline):
    model = HotelRoom
    extra = 1


@admin.register(HotelRoomType)
class HotelRoomTypeAdmin(admin.ModelAdmin):
    inlines = [HotelRoomInline]
    list_display = ('hotel', 'title',)
    show_change_link = True


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    inlines = [ReservationInline]
    list_display = ('room_number',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reserved_from', 'reserved_to',)
    show_change_link = True


@admin.register(BookingInfo)
class BookingInfoAdmin(admin.ModelAdmin):
    pass

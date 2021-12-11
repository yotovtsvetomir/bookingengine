from django.db.models import Min
from rest_framework import serializers

import json

from .models import Listing, Reservation, HotelRoomType, HotelRoom, BookingInfo


class BookingInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingInfo
        fields = ['price']


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"


class HotelRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelRoom
        fields = "__all__"


class HotelRoomTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelRoomType
        fields = "__all__"


class ListingSerializer(serializers.ModelSerializer):
    booking_info = BookingInfoSerializer()

    class Meta:
        model = Listing
        fields = ['id', 'listing_type', 'title', 'country', 'city', 'booking_info']

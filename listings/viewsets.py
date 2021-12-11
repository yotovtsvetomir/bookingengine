from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from django.db.models import Prefetch, Min

import io
import json

from .serializers import ListingSerializer
from .models import Listing, Reservation, HotelRoom


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.prefetch_related(
        'hotel_room_types', 'hotel_room_types__hotel_rooms', 'hotel_rooms', 'reservations', 'booking_info').all().order_by('booking_info__price')
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Prefetching all needed querysets for better performance
        qs = Listing.objects.prefetch_related(
            'hotel_room_types', 'hotel_room_types__hotel_rooms', 'hotel_rooms', 'reservations', 'booking_info').all().order_by('booking_info__price')

        # Getting params
        reserved_from = self.request.query_params.get('check_in', None)
        reserved_to = self.request.query_params.get('check_out', None)
        price = self.request.query_params.get('max_price', None)

        for listing in qs:

            if listing.listing_type == 'apartment':
                if reserved_from != None and reserved_to != None:
                    # If the number of reservations for those dates for this apartment is greater than 0 -> it is booked
                    if listing.reservations.filter(listing=listing.id, reserved_from__lte=reserved_from, reserved_to__gte=reserved_to).count() > 0:
                        qs = qs.exclude(id=listing.id)

                if price != None:
                    # If the price is higher than the desired one exclude the apartment
                    if listing.booking_info.price > int(price):
                        qs = qs.exclude(id=listing.id)

            else:
                # If the number of reservations for those dates for this hotel is equal to number of rooms -> the hotel is fully booked
                if reserved_from != None and reserved_to != None:
                    if listing.reservations.filter(listing=listing.id, reserved_from__lte=reserved_from, reserved_to__gte=reserved_to).count() == listing.hotel_rooms.count():
                        qs = qs.exclude(id=listing.id)

                if price != None:
                    # If the number of room types with price higher than max_price = to the number of the room types -> hotel doesn't have any rooms with our price
                    if listing.hotel_room_types.filter(booking_info__price__gt=int(price)).count() == listing.hotel_room_types.count():
                        qs = qs.exclude(id=listing.id)
                    else:
                        # Getting the cheapest available room to display in the listing with price lower than max_price
                        listing.booking_info = listing.hotel_room_types.filter(
                            booking_info__price__lte=int(price),
                            hotel_rooms__in=listing.hotel_rooms.exclude(reservations__in=listing.reservations.filter(
                                                                        listing=listing,
                                                                        reserved_from__lte=reserved_from,
                                                                        reserved_to__gte=reserved_to))
                        ).order_by('booking_info__price')[0].booking_info
                        listing.booking_info.save()
                elif reserved_from != None and reserved_to != None:
                    # Getting the cheapest available room to display in the listing
                    listing.booking_info = listing.hotel_room_types.filter(
                        hotel_rooms__in=listing.hotel_rooms.exclude(reservations__in=listing.reservations.filter(
                                                                    listing=listing,
                                                                    reserved_from__lte=reserved_from,
                                                                    reserved_to__gte=reserved_to))
                    ).order_by('booking_info__price')[0].booking_info
                    listing.booking_info.save()

        # Ordering by price
        qs = qs.order_by('booking_info__price')

        return qs

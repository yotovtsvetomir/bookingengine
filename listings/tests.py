from django.test import TestCase, Client
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.db import connection

from .models import Listing, HotelRoomType, HotelRoom, BookingInfo, Reservation


class ListingTestCase(TestCase):

    def setUp(self):
        # Apartments
        a = Listing.objects.create(listing_type="apartment",
                                   title="Luxurious Studio", country="UK", city="London")
        BookingInfo.objects.create(listing=a, price=40)

        a = Listing.objects.create(
            listing_type="apartment", title="Excellent 2 Bed Apartment Near Tower Bridge", country="UK", city="London")
        BookingInfo.objects.create(listing=a, price=90)
        Reservation.objects.create(listing=a, reserved_from='2021-12-09', reserved_to='2021-12-13')

        # Hotel
        l = Listing.objects.create(
            listing_type="hotel", title="Hotel Lux 5***", country="UK", city="London")

        # Hotel Room Type 1
        hrt1 = HotelRoomType.objects.create(hotel=l, title="Single Room")
        hm1 = HotelRoom.objects.create(hotel=l, hotel_room_type=hrt1, room_number=103)
        BookingInfo.objects.create(hotel_room_type=hrt1, price=50)
        Reservation.objects.create(listing=l, hotel_room=hm1,
                                   reserved_from='2021-12-09', reserved_to='2021-12-13')

        # Hotel Room Type 2
        hrt2 = HotelRoomType.objects.create(hotel=l, title="Double Room")
        hm1 = HotelRoom.objects.create(hotel=l, hotel_room_type=hrt2, room_number=102)
        hm2 = HotelRoom.objects.create(hotel=l, hotel_room_type=hrt2, room_number=104)
        BookingInfo.objects.create(hotel_room_type=hrt2, price=60)
        Reservation.objects.create(listing=l, hotel_room=hm1,
                                   reserved_from='2021-12-09', reserved_to='2021-12-13')

        # Hotel Room Type 3
        hrt3 = HotelRoomType.objects.create(hotel=l, title="Triple Room")
        HotelRoom.objects.create(hotel=l, hotel_room_type=hrt3, room_number=101)
        BookingInfo.objects.create(hotel_room_type=hrt3, price=200)

    def test_listing_performance(self):
        client = Client()

        with CaptureQueriesContext(connection) as ctx:
            response = client.get("/listings")

            # Checking if any query is slow (we need larger dataset for real testing, but just to show that we can dive into the it)
            for query in ctx.captured_queries:
                self.assertEqual('0.000', query['time'])

    def test_listing_ordering(self):
        client = Client()

        response = client.get(
            "/listings/?max_price=100&check_in=2021-12-09&check_out=2021-12-12")

        r = response.json()

        # In this case we have 2 results
        # 1. Hotel -> cheapest available room price 60
        # 2. Apartment -> price 40
        # We are checking if the lower price comes first

        self.assertEqual('40.00', r['results'][0]['booking_info']['price'])

    def test_listing_apartment(self):
        client = Client()

        response = client.get(
            "/listings/?max_price=100&check_in=2021-12-09&check_out=2021-12-12")

        r = response.json()

        # In this case we have 2 apartments ->
        # 1. Luxurious Studio -> price 40 -> available
        # 2. Excellent 2 Bed Apartment Near Tower Bridge -> price 90 -> booked
        # We are checking if we are getting only the free one

        counter = 0
        for res in r['results']:
            if res['listing_type'] == 'apartment':
                counter = counter + 1

        # In our case the number of apartments in the result should be 1
        self.assertEqual(1, counter)

    def test_listing_hotel(self):
        client = Client()

        response = client.get(
            "/listings/?max_price=100&check_in=2021-12-09&check_out=2021-12-12")

        r = response.json()

        # In this case we have a hotel with 2 available rooms ->
        # 1. Double room -> price 60 (we have one more which is booked)
        # 2. Triple room -> price 200
        # We are checking if we are getting price 60 for the hotel listing

        for res in r['results']:
            if res['listing_type'] == 'hotel':
                self.assertEqual('60.00', res['booking_info']['price'])

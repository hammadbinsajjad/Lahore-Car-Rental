from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Booking
from .helpers import format_date


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "vehicle", "start_date", "end_date"]

    def validate(self, attrs):
        current_booking = super().validate(attrs)

        if current_booking["start_date"] > current_booking["end_date"]:
            raise ValidationError("Start Date cannot be after End date")

        overlapping_bookings = Booking.objects.filter(
            vehicle=current_booking["vehicle"],
            end_date__gte=current_booking["start_date"],
            start_date__lte=current_booking["end_date"]
        )

        if overlapping_bookings:
            overlapped_booking = overlapping_bookings.first()
            booking_error = {
                "error": (f"Booking already exists on {format_date(overlapped_booking.start_date)}"
                          f" to {format_date(overlapped_booking.end_date)}")
            }

            raise ValidationError(booking_error)

        return current_booking

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.timezone import now, timedelta
from .models import Booking, Notification
from redis.exceptions import ConnectionError

User = get_user_model()


@shared_task
def send_upcoming_showtime_reminders():
    """
    Send reminders for all showtimes starting within the next 24 hours.
    """
    try:
        window_start = now()
        window_end = window_start + timedelta(hours=24)

        bookings = Booking.objects.filter(
            status__in=["Confirmed", "Pending"],
            showtime__start_time__range=(window_start, window_end),
        )

        print(f"Debug: Bookings queryset - {bookings}")
        count = 0
        for booking in bookings:
            try:
                obj, created = Notification.objects.get_or_create(
                    user=booking.user, message=f"⏰ Reminder: your showtime for “{booking.showtime.movie.title}” "
                    f"is at {booking.showtime.start_time.strftime('%Y-%m-%d %H:%M')}."
                )
                if created:
                    count += 1
            except Exception as e:
                print(f"Error: Exception occurred during get_or_create - {e}")

        return f"Reminders sent for {count} bookings."
    except ConnectionError as e:
        print(f"Error: Redis connection issue - {e}")
        return "Failed to send reminders due to Redis connection issues."


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_pending_booking_reminder(self, booking_id):
    booking = Booking.objects.filter(pk=booking_id, status='Pending').first()
    if not booking:
        return
    Notification.objects.get_or_create(
        user=booking.user,
        message=(
            f"⏳ You still have a pending booking #{booking.showtime.movie.title}. "
            "Please complete payment within 24 hours."
        )
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def delete_unpaid_booking(self, booking_id):
    with transaction.atomic():
        booking = Booking.objects.filter(
            pk=booking_id,
            status='Pending'
        ).first()
        if not booking:
            return f"Booking {booking_id} not found or not pending"

        # mark it cancelled
        booking.status = 'Cancelled'
        booking.save(update_fields=['status'])
        Notification.objects.create(
            user=booking.user,
            message=(
                f"❌ Your booking for “{booking.showtime.movie.title}” was not paid in time "
                "and has been automatically cancelled."
            )
        )

        # Mark seats as available and increase available seats
        for seat in booking.seats.all():
            seat.is_booked = False
            seat.save(update_fields=['is_booked'])

        booking.showtime.available_seats += len(booking.seats.all())
        booking.showtime.save(update_fields=['available_seats'])

        return f"Booking {booking_id} cancelled"


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_showtime_reminder(self, booking_id):
    booking = Booking.objects.filter(pk=booking_id, status='Confirmed').first()
    if not booking:
        return
    showtime = booking.showtime
    Notification.objects.get_or_create(
        user=booking.user,
        message=(
            f"⏰ Reminder: your showtime for “{showtime.movie.title}” "
            f"is on {showtime.start_time.strftime('%Y-%m-%d %H:%M')}."
        )
    )


@shared_task
def update_booking_status_after_showtime():
    """
    Update booking statuses after the showtime ends:
    - Mark confirmed bookings as attended.
    - Cancel pending bookings.
    """
    try:
        current_time = now()

        # Mark confirmed bookings as attended
        confirmed_bookings = Booking.objects.filter(
            status='Confirmed',
            attended=False,
            showtime__end_time__lte=current_time
        )
        for booking in confirmed_bookings:
            booking.attended = True
            booking.save(update_fields=['attended'])
            Notification.objects.create(
                user=booking.user,
                message=(
                    f"✅ Thank you for attending the showtime for “{booking.showtime.movie.title}” on "
                    f"{booking.showtime.start_time.strftime('%Y-%m-%d %H:%M')}!"
                    f"You can leave a review for our service which helps us improve."
                    f"By visiting the booking details page."
                )
            )

        # Cancel pending bookings
        pending_bookings = Booking.objects.filter(
            status='Pending',
            showtime__end_time__lte=current_time
        )
        for booking in pending_bookings:
            booking.status = 'Cancelled'
            booking.save(update_fields=['status'])
            Notification.objects.create(
                user=booking.user,
                message=(
                    f"❌ Your booking for “{booking.showtime.movie.title}” was not confirmed in time "
                    f"and has been automatically cancelled."
                )
            )

            # Mark seats as available and increase available seats
            for seat in booking.seats.all():
                seat.is_booked = False
                seat.save(update_fields=['is_booked'])

            booking.showtime.available_seats += len(booking.seats.all())
            booking.showtime.save(update_fields=['available_seats'])

        return (
            f"Updated statuses: {confirmed_bookings.count()} bookings marked as attended, "
            f"{pending_bookings.count()} bookings cancelled."
        )
    except Exception as e:
        print(f"Error: Exception occurred while updating booking statuses - {e}")
        return "Failed to update booking statuses due to an error."

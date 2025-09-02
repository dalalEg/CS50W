from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from .models import Booking, Notification, Payment

User = get_user_model()


@shared_task
def send_upcoming_showtime_reminders():
    """
    Send reminders for all showtimes starting within the next 24 hours.
    """
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
                user=booking.user, message=f"⏰ Reminder: your showtime for"
                f"”{booking.showtime.movie.title}” "
                f"is at {booking.showtime.start_time.strftime('%Y-%m-%d %H:%M')}.")
            if created:
                count += 1
        except Exception as e:
            print(f"Error: Exception occurred during get_or_create - {e}")

    return f"Reminders sent for {count} bookings."


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
    # use the TextChoices constant so casing always matches
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

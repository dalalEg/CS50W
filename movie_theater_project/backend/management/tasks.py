from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from .models import Booking,Notification

User = get_user_model()


@shared_task
def send_upcoming_showtime_reminders():
    """
    Send reminders for upcoming showtimes within 24 hours.
    """
    window_start = now()
    window_end = window_start + timedelta(hours=24)

    bookings = Booking.objects.filter(status=['Confirmed','Pending'])
    for booking in bookings:
        Notification.objects.create(
            user=booking.user,
            message=f"Reminder: Your showtime is at {booking.showtime.start_time}"
        )
    return f"Reminders sent for {bookings.count()} bookings."


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_pending_booking_reminder(self, booking_id):
    booking = Booking.objects.filter(pk=booking_id, status='Pending').first()
    if not booking:
        return
    Notification.objects.get_or_create(
        user=booking.user,
        message=(
          f"⏳ You still have a pending booking #{booking.id}. "
          "Please complete payment within 24 hours."
        )
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def delete_unpaid_booking(self, booking_id):
    booking = Booking.objects.filter(pk=booking_id, status='Pending').first()
    if not booking:
        return
    booking.delete()
    Notification.objects.create(
        user=booking.user,
        message=(
          f"❌ Your booking #{booking.id} was not paid in time "
          "and has been automatically cancelled."
        )
    )
    # optionally log or notify admins here


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

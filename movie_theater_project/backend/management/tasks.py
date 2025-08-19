from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from .models import Booking,Notification
# from notifications.utils import send_notification

User = get_user_model()


@shared_task
def send_upcoming_showtime_reminders():
    """
    Send reminders for upcoming showtimes within 24 hours.
    """
    window_start = now()
    window_end = window_start + timedelta(hours=24)

    bookings = Booking.objects.filter(showtime__start_time__range=(window_start, window_end))
    for booking in bookings:
        Notification.objects.create(
            user=booking.user,
            message=f"Reminder: Your showtime is at {booking.showtime.start_time}"
        )
    return f"Reminders sent for {bookings.count()} bookings."

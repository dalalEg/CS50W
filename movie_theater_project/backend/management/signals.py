from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Showtime, Movie, Notification, watchlist, Favourite

@receiver(post_save, sender=Showtime)
def notify_watchlist_on_new_showtime(sender, instance, created, **kwargs):
    if not created:
        return
    movie = instance.movie
    # all users who have this movie in their watchlist
    watcher_ids = watchlist.objects.filter(movie=movie).values_list('user_id', flat=True).distinct()
    for uid in watcher_ids:
        Notification.objects.create(
            user_id=uid,
            message=f"📅 New showtime for {movie.title} at {instance.start_time:%Y-%m-%d %H:%M}"
        )

@receiver(post_save, sender=Movie)
def notify_favourites_on_related_movie(sender, instance, created, **kwargs):
    if not created:
        return
    # users who favourited any movie by the same director
    director_ids = Favourite.objects.filter(movie__director=instance.director).values_list('user_id', flat=True)
    # users who favourited any movie by the same producer
    producer_ids = Favourite.objects.filter(movie__producer=instance.producer).values_list('user_id', flat=True)
    # users who favourited any movie by either the same director or producer
    user_ids = set(director_ids) | set(producer_ids)

    for uid in user_ids:
        role = []
        if uid in director_ids:
            role.append('director')
        if uid in producer_ids:
            role.append('producer')
        rel = ' & '.join(role)
        Notification.objects.create(
            user_id=uid,
            message=f"🎬 New movie “{instance.title}” from your favorite {rel}"
        )
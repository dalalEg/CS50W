from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management'

    def ready(self):
        import management.signals
        # Ensures signal handlers are connected
        # This is necessary to ensure that the signal handlers are registered
        management.signals.notify_watchlist_on_new_showtime
        management.signals.notify_favourites_on_related_movie
# -----------------------------------------------------------------------------

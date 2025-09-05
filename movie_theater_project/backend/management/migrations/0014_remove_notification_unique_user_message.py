from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('management', '0013_notification_unique_user_message'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Check if the constraint exists before removing it
            PRAGMA table_info(management_notification);
            """,
            reverse_sql="",
        ),
    ]
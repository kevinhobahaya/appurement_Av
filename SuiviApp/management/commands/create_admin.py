from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="kahayabanywesizekevin@gmail.com",
                password="admin@occkasindi2310"
            )
            self.stdout.write("Admin created")
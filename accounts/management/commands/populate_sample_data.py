from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile
import random
from datetime import date, timedelta
import os
from django.core.files import File
from django.conf import settings
import shutil
from PIL import Image, ImageDraw

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample profiles'

    def handle(self, *args, **kwargs):
        # Create media directory if it doesn't exist
        media_dir = 'media/profile_pics'
        os.makedirs(media_dir, exist_ok=True)

        # Create default profile picture if it doesn't exist
        default_pic_path = os.path.join(media_dir, 'default.jpg')
        if not os.path.exists(default_pic_path):
            img = Image.new('RGB', (200, 200), color='lightgray')
            draw = ImageDraw.Draw(img)
            draw.ellipse((50, 50, 150, 150), fill='gray')
            img.save(default_pic_path)

        # Sample data
        sample_users = [
            {
                'email': 'john@example.com',
                'name': 'John Doe',
                'location': 'New York',
                'bio': 'Software engineer looking for a life partner',
                'age': 28,
                'gender': 'M'
            },
            {
                'email': 'jane@example.com',
                'name': 'Jane Smith',
                'location': 'Los Angeles',
                'bio': 'Doctor seeking meaningful connections',
                'age': 30,
                'gender': 'F'
            },
            {
                'email': 'mike@example.com',
                'name': 'Mike Johnson',
                'location': 'Chicago',
                'bio': 'Business professional interested in long-term relationships',
                'age': 32,
                'gender': 'M'
            },
        ]

        for user_data in sample_users:
            # Check if user already exists
            user, created = CustomUser.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'name': user_data['name'],
                    'password': 'testpass123'
                }
            )

            if created:
                # Create profile for new user
                Profile.objects.create(
                    user=user,
                    location=user_data['location'],
                    bio=user_data['bio'],
                    profile_picture=default_pic_path,
                    age=user_data['age'],
                    gender=user_data['gender']
                )
                self.stdout.write(self.style.SUCCESS(f'Created profile for {user_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user_data["name"]} already exists'))

        self.stdout.write(self.style.SUCCESS('Sample data population completed')) 
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from media.models import MediaItem
from pathlib import Path

class Command(BaseCommand):
    help = 'Register existing media files in the database'
    
    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        
        # Supported file extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.webm']
        audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a']
        
        # Walk through media directory
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, media_root)
                
                # Determine media type based on extension
                ext = os.path.splitext(file)[1].lower()
                
                if ext in image_extensions:
                    media_type = 'image'
                elif ext in video_extensions:
                    media_type = 'video'
                elif ext in audio_extensions:
                    media_type = 'audio'
                else:
                    continue  # Skip unsupported file types
                
                # Check if this file is already in the database
                if not MediaItem.objects.filter(file=relative_path).exists():
                    # Create a title from filename
                    title = os.path.splitext(file)[0].replace('_', ' ').title()
                    
                    # Create database entry
                    MediaItem.objects.create(
                        title=title,
                        description=f"Auto-registered {media_type} file",
                        media_type=media_type,
                        file=relative_path
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Registered: {relative_path} as {media_type}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Skipped (already exists): {relative_path}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Finished registering media files')
        )
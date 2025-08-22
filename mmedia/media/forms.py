from django import forms
from .models import MediaItem

class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['title', 'description', 'media_type', 'file']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'accept': 'image/*,video/*,audio/*'})
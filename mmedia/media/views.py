from django.shortcuts import render, redirect
from .models import MediaItem
from .forms import MediaUploadForm

def media_list(request):
    media_items = MediaItem.objects.all()
    
    # Filter by type if requested
    media_type = request.GET.get('type')
    if media_type:
        media_items = media_items.filter(media_type=media_type)
    
    return render(request, 'media/list.html', {'media_items': media_items})

def media_detail(request, pk):
    media_item = MediaItem.objects.get(pk=pk)
    return render(request, 'media/detail.html', {'media_item': media_item})

def upload_media(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('media_list')
    else:
        form = MediaUploadForm()
    
    return render(request, 'media/upload.html', {'form': form})
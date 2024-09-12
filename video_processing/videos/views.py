import os
import subprocess
from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Video, Subtitle
from .forms import VideoForm
from .tasks import parse_srt_file, test_celery


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            video_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
            subtitle_output_path = os.path.join(settings.MEDIA_ROOT, 'subtitle', f'{video.title}_{video.pk}.srt')
            os.makedirs(os.path.dirname(subtitle_output_path), exist_ok=True)

            parse_srt_file(subtitle_output_path, video, video_path) # add .delay to run as async

            return redirect('video_list')
    else:
        form = VideoForm()

    return render(request, 'videos/upload_video.html', {'form': form})


def play_video(request, pk):
    video = Video.objects.get(pk=pk)
    return render(request, 'videos/play_video.html', {'video': video})


def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    print(f'{video.title}_{video.pk}.srt')
    # Delete subtitle files
    subtitles = Subtitle.objects.filter(video_id=pk)
    for subtitle in subtitles:
        subtitle_file_path = os.path.join(settings.MEDIA_ROOT, 'subtitle', f'{video.title}_{video.pk}.srt')
        vtt_subtitle_file_path = os.path.join(settings.MEDIA_ROOT, 'subtitle', f'{video.title}_{video.pk}.vtt')
        if os.path.exists(subtitle_file_path):
            os.remove(subtitle_file_path)
        if os.path.exists(vtt_subtitle_file_path):
            os.remove(vtt_subtitle_file_path)
    
    video_file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    if os.path.exists(video_file_path):
        os.remove(video_file_path)

    subtitles.delete()

    video.delete()

    return HttpResponseRedirect(reverse('video_list'))

def video_list(request):
    query = request.GET.get('q')  
    videos_with_start_times = []  

    if query:
        subtitles = Subtitle.objects.filter(content__icontains=query)

        for subtitle in subtitles:
            videos_with_start_times.append((subtitle.video, subtitle.start_time))
    else:
        videos_with_start_times = [(video, None) for video in Video.objects.all()]

    return render(request, 'videos/video_list.html', {
        'videos_with_start_times': videos_with_start_times,
        'query': query
    })

def play_video(request, pk):
    video = get_object_or_404(Video, pk=pk)

    start_time = request.GET.get('start_time', None)

    return render(request, 'videos/play_video.html', {
        'video': video,
        'start_time': start_time
    })
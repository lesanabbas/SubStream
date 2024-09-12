import subprocess
from django.utils.html import strip_tags
from celery import shared_task
from .models import Subtitle


@shared_task
def test_celery(name: str):
    print(f"Hello! {name} celery working...........")
    return



@shared_task
def parse_srt_file(srt_file_path, video, video_path):

    subprocess.run([
        'ffmpeg',  
        '-i', video_path,                                  
        '-c:s', 'srt',
        srt_file_path,
    ])

    with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
        subtitle_block = []
        for line in srt_file:
            line = line.strip()
            if not line:

                if len(subtitle_block) >= 3:
                    times = subtitle_block[1].split(' --> ')
                    start_time = times[0].replace(',', '.')
                    end_time = times[1].replace(',', '.')

                    raw_content = ' '.join(subtitle_block[2:])
                    content = strip_tags(raw_content) 

                    Subtitle.objects.create(
                        video=video,
                        start_time=start_time,
                        end_time=end_time,
                        content=content,
                        language='eng'
                    )

                subtitle_block = []
            else:
                subtitle_block.append(line)
    
    convert_srt_to_vtt(srt_file_path, f"{srt_file_path.split('srt')[0]}vtt")  # add .delay to run as async

@shared_task
def convert_srt_to_vtt(srt_file, vtt_file):
    with open(srt_file, 'r', encoding='utf-8') as srt:
        with open(vtt_file, 'w', encoding='utf-8') as vtt:
            vtt.write("WEBVTT\n\n")
            
            for line in srt:
                # Skip sequence numbers
                if line.strip().isdigit():
                    continue
                
                # Replace commas with dots in timecodes
                if "-->" in line:
                    line = line.replace(",", ".")
                
                # Remove <font> tags if present
                line = line.replace("<font", "").replace("</font>", "")
                line = line.replace('color="#ffff00">', '').replace('size="14">', '')

                vtt.write(line)
                
    print(f"Converted {srt_file} to {vtt_file}")

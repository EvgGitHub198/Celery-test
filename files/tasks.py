from PIL import Image
from celery import shared_task
from .models import File
from docx import Document
from docx.shared import Pt
from pydub import AudioSegment


def process_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((100, 100))
    img.save(file_path)


def process_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    audio = audio[:30000]
    audio.export(file_path, format="mp3")


def process_text(file_path):
    document = Document(file_path)
    watermark = document.sections[0].footer.paragraphs[0]
    watermark.text = "Watermark created by Celery"
    watermark.alignment = 1
    watermark.runs[0].font.size = Pt(12)
    document.save(file_path)


@shared_task
def process_uploaded_file(file_id):
    try:
        file = File.objects.get(pk=file_id)
        file_extension = file.file.name.split('.')[-1].lower()

        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            process_image(file.file.path)
        elif file_extension in ['mp3', 'wav', 'flac', 'ogg', 'm4a', 'wma']:
            process_audio(file.file.path)
        elif file_extension in ['docx', 'doc']:
            process_text(file.file.path)

        file.processed = True
        file.file_type = file_extension
        file.save()
    except File.DoesNotExist:
        pass

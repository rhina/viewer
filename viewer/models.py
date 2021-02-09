import os
import requests
from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import PIL.Image


class Image(models.Model):
    file = models.ImageField(upload_to='image')
    width = models.IntegerField(null=False, blank=False)
    height = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    @staticmethod
    def create(image_url=None, image_pil=None, upload_path=None):
        assert upload_path and os.path.splitext(upload_path)[-1] in [".jpeg", ".jpg"], \
            "Currently, only jpeg image is accepted"
        if image_pil is None:
            assert image_url is not None
            response = requests.get(image_url)
            assert response.status_code != 403, f"403 error occured when downloading image {image_url}"
            image_pil = PIL.Image.open(BytesIO(response.content)).convert("RGB")
        buffer = BytesIO()
        image_pil.save(buffer, format='JPEG')
        buffer.seek(0)
  
        width, height = image_pil.size[:2]
        image = Image(width=width, height=height)
        image_file = InMemoryUploadedFile(buffer, None, upload_path, 'image/jpeg',
                                          buffer.getbuffer().nbytes, None)
                                          
        image.file.save(upload_path, image_file, save=True)
        return image


class Book(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.title}"


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_index = models.IntegerField(default=0, null=False, blank=False)
    title = models.TextField(blank=False, null=False)
    name = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=None)
    page_index = models.IntegerField(null=False, blank=False)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True,
                              blank=True, related_name='original_image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f"{str(self.chapter)} p{self.page_index}"

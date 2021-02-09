from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'created_at', 'updated_at')

@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'book', 'created_at', 'updated_at')

@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
  list_display = ('id', 'image', 'chapter', 'created_at', 'updated_at')

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
  list_display = ('id', 'width', 'height', 'created_at', 'updated_at')

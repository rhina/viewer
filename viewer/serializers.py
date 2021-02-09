from rest_framework import serializers
from .models import Book, Chapter, Image, Page
from django.shortcuts import get_list_or_404


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "chapter_ids")
    chapter_ids = serializers.SerializerMethodField()

    def get_chapter_ids(self, instance):
        return [c.id for c in instance.chapter_set.all()]


class PageSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = Page
        fields = ("id", "page_index", "image")


class ChapterSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    pages = PageSerializer(many=True, source="page_set")
    class Meta:
        model = Chapter
        fields = ("id", "title", "book", "chapter_index", "pages")


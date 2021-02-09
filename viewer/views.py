from .models import Book, Chapter
from .serializers import BookSerializer, ChapterSerializer
from django.shortcuts import get_list_or_404, render
from django.http import Http404
from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response

class BookViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ChapterViewSet(viewsets.GenericViewSet,
                     mixins.RetrieveModelMixin):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


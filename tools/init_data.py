import _init_django
import os
import argparse
import requests
import boto3
import random
from tqdm import tqdm
from django.db import transaction
import glob
import PIL.Image
from viewer.models import Image, Page, Chapter, Book


@transaction.atomic
def init_data(data_dir):
    book_titles = [f for f in os.listdir(data_dir) if f != ".DS_Store"]
    book_titles = [b for b in book_titles if b != ".DS_Store"]
    assert len(book_titles) > 0
    for book_title in tqdm(book_titles):
        book, created = Book.objects.update_or_create(title=book_title)
        chapter_titles = sorted(os.listdir(os.path.join(data_dir, book_title)))
        chapter_titles = [c for c in chapter_titles if c != ".DS_Store"]
        assert len(chapter_titles) > 0
        for chapter_index, chapter_title in enumerate(tqdm(chapter_titles)):
            chapter, created = Chapter.objects.update_or_create(book=book, chapter_index=chapter_index,
                                                defaults={
                                                    "book": book,
                                                    "chapter_index": chapter_index,
                                                    "title": chapter_title,
                                                })
            page_paths = sorted(glob.glob(os.path.join(data_dir, book_title, chapter_title) + "/*.jpg"))
            assert len(page_paths) > 0
            for page_index, page_path in enumerate(page_paths):
                page, created = Page.objects.update_or_create(chapter=chapter, page_index=page_index)
                if created:
                    image_pil = PIL.Image.open(page_path)
                    image = Image.create(image_pil=image_pil, upload_path=os.path.join(book_title, chapter_title, os.path.basename(page_path)))
                    page.image = image
                    page.save()



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_dir", type=str, default="test")
    args = parser.parse_args()
    init_data(args.data_dir)

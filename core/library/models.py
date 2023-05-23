from enum import Enum

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify


def document_file_path(instance, filename):
    return f"documents/{slugify(instance.name)}-{filename}"


class SupportedDocumentFormats(Enum):
    PDF: str = "pdf"
    DOC: str = "doc"
    DOCX: str = "docx"
    MP4: str = "mp4"
    PPTX: str = "pptx"
    PPT: str = "ppt"
    PPTM: str = "pptm"
    MOV: str = "mov"
    WEBM: str = "webm"
    PNG: str = "png"
    JPG: str = "jpg"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, SupportedDocumentFormats))


class Document(models.Model):
    name = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to=document_file_path, validators=[FileExtensionValidator(
        allowed_extensions=SupportedDocumentFormats.list())])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

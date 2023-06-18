from datetime import datetime, timezone
from enum import Enum

from django.contrib.auth import get_user_model
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
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def created_date(self):
        return datetime.fromisoformat(str(self.created_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")

    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")

    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)

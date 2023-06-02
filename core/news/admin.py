from django.contrib import admin
from news.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "language", "created_at", "updated_at"]
    prepopulated_fields = {"slug": ("title",)}  
    search_fields = ["title"]
    ordering = ["-created_at"]

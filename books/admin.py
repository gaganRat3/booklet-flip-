from django.contrib import admin
from .models import FlipBook, BookView


@admin.register(FlipBook)
class FlipBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumbnail_preview', 'created_by', 'total_pages', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['total_pages', 'thumbnail_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'description', 'pdf_file', 'thumbnail', 'thumbnail_preview')
        }),
        ('Settings', {
            'fields': ('is_published', 'created_by')
        }),
        ('Metadata', {
            'fields': ('total_pages', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return f'<img src="{obj.thumbnail.url}" style="max-width: 200px; max-height: 200px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />'
        return '<span style="color: #999;">No thumbnail</span>'
    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BookView)
class BookViewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['book__title', 'ip_address']
    readonly_fields = ['book', 'user', 'ip_address', 'viewed_at']

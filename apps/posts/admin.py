from django.contrib import admin
from django import forms

from .models import Post, Comentario
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "titulo",
            'slug',
            'autor',
            "contenido",
            'estado',
            'image',
            'tags',
        ]
        widgets = {
            "contenido": forms.CharField(widget=CKEditorUploadingWidget()),
            # "contenido":forms.CharField(widget=CKEditorWidget()),
        }


class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'slug', 'estado', 'created')
    list_filter = ('estado', 'created', 'autor')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {"slug": ("titulo",)}
    raw_id_fields = ("autor",)
    date_hierarchy = 'publish'
    ordering = ('publish', 'estado')
    form = PostAdminForm


admin.site.register(Post, PostAdmin)


class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'active')
    list_filter = ('active', 'created')
    search_fields = ('nombre', 'correo')
    date_hierarchy = 'created'
    ordering = ('created', 'active')


admin.site.register(Comentario, ComentarioAdmin)

from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'
urlpatterns = [
    path('', post_list, name='post_list'),
    path('tag/<tag_slug>', post_list, name='post_list_by_tag'),
    path('<str:slug>', post_detail, name='post_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

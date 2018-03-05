from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import  RichTextUploadingField
from taggit.managers import TaggableManager

"""
from apps.posts.models import Post
posts = Post.objects.all()
publicados = Post.publicados.all()
"""


class PostPublished(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(estado='publicado').order_by('-created')


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.slug, filename)


class Post(models.Model):
    ESTADO_POST = (
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    )
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    # contenido = models.TextField()
    # contenido = RichTextField()
    contenido = RichTextUploadingField()
    publish = models.DateField(default=timezone.localtime)
    created = models.DateField(auto_now_add=True, verbose_name='creado')
    updated = models.DateField(auto_now=True)
    estado = models.CharField(max_length=10, choices=ESTADO_POST, default='borrador')
    image = models.ImageField(upload_to=user_directory_path, blank=True, )

    objects = models.Manager()  # The default manager.
    publicados = PostPublished()  # The PostPublished manager.
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post_detail', args=[str(self.slug)])


class Comentario(models.Model):
    post = models.ForeignKey(Post, related_name='comentarios', on_delete=models.CASCADE, )
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contenido = models.TextField()
    created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comentario por {}'.format(self.nombre)

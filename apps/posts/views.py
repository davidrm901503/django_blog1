from django.shortcuts import render, get_object_or_404
from taggit.models import Tag

from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    response = render(request, 'index.html')

    if not request.COOKIES.get('visits'):
        response.set_cookie('visits', '1', 3600)
    else:
        visits = int(request.COOKIES.get('visits', '1')) + 1
        response.set_cookie('visits', str(visits), 3600)

    return response


def post_list(request, tag_slug=None):
    object_list = Post.publicados.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 5)  # Show n posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
    return render(request, 'blog/posts_list.html', {'posts': posts, 'titulo': 'Listado', 'tag': tag})


def post_detail(request, slug):
    post = get_object_or_404(Post, estado='publicado', slug=slug)
    context = {'post': post, 'titulo': "Detalle"}
    return render(request, 'blog/post_detail.html', context)

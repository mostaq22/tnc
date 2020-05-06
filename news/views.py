from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Fact, Post


# Create your views here.
def homepage(request):
    context = {
        "facts": Fact.objects.filter(show_in_homepage=True)[:6],
        "newspaper_posts": Post.objects.filter(show_in_homepage=True)[:6]
    }
    return render(request, template_name='pages/home.html', context=context)


def fact_detail(request, id=None):
    context = {
        "fact": get_object_or_404(Fact, pk=id)
    }
    return render(request, template_name='pages/fact.html', context=context)


def post_detail(request, id=None):
    context = {
        "post": get_object_or_404(Post, pk=id)
    }
    return render(request, template_name='pages/post.html', context=context)


def category(request, id=None):
    posts = Post.objects.filter(fact__category=id).order_by('-id')
    posts = post_pagination(request, posts)

    context = {
        "posts": posts
    }
    return render(request, 'pages/category.html', context=context)


def post_pagination(request, posts):
    post_page = request.GET.get('post_page', 1)
    post_paginator = Paginator(posts, 2)
    try:
        posts = post_paginator.page(post_page)
    except PageNotAnInteger:
        posts = post_paginator.page(1)
    except EmptyPage:
        posts = post_paginator.page(post_paginator.num_pages)

    return posts

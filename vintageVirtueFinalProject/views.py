from django.shortcuts import render
from operator import attrgetter
from post.models import BlogPost


def home(request):
    context = {}
    blog_posts = sorted(BlogPost.objects.all(), key=attrgetter('date_publish'), reverse=True)
    context['blog_posts'] = blog_posts
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def conditions(request):
    return render(request, 'conditions.html')


def contact(request):
    return render(request, 'contact.html')


def privacy(request):
    return render(request, 'privacy.html')

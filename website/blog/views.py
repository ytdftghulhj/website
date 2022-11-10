from django.shortcuts import render
from django.http import HttpResponse
from .models import Article

def home(reqest):
    posts = Article.objects.order_by('-created_at')
    return render(reqest, 'blog/home.html',{'posts': posts })

def test(reqest):
    posts = Article.objects.all()
    res = '<h1>Список статей</h1>'
    for post in posts:
        res += f'<div><h3>{post.title}</h3><div>{post.content}</div></div><hr>'
    return HttpResponse(res)

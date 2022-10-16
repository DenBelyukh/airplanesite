from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статтю", 'url_name': 'add_page'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
        {'title': "Зайти", 'url_name': 'login'}
]


def index(request):
    posts = Plane.objects.all()
    # cats = Category.objects.all()

    context = {
        'posts': posts,
        # 'cats': cats,
        'menu': menu,
        'title': 'Головна сторінка',
        'cat_selected': 0,
    }

    return render(request, 'planes/index.html', context=context)


def about(request):
    return render(request, 'planes/about.html', {'menu': menu, 'title': 'Про сайт'})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            try:
                Plane.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Помилка додавання поста')

    else:
        form = AddPostForm()
        return render(request, 'planes/addpage.html', {'form': form, 'menu': menu, 'title': 'Додавання статті'})


def contact(request):
    return HttpResponse("Зворотній зв'язок")


def login(request):
    return HttpResponse("Авторизація")


def show_post(request, post_slug):
    post = get_object_or_404(Plane, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'planes/post.html', context=context)


def show_category(request, cat_id):
    posts = Plane.objects.filter(cat_id=cat_id)
    # cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        # 'cats': cats,
        'menu': menu,
        'title': 'По категоріям',
        'cat_selected': cat_id,
    }

    return render(request, 'planes/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')

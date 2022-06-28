from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from ..models import Post, Product
'''
https://isofix-msk.ru/blog/instrukciya-isofix/
https://isofix-msk.ru/blog/neskolko-kresel/
https://isofix-msk.ru/blog/podushka-bezopasnosti/
https://isofix-msk.ru/blog/avto-s-isofix/
https://isofix-msk.ru/blog/sertificati-kresel/
https://isofix-msk.ru/blog/isofix-standart/
'''

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                 'shop/post/list.html',
                 {'page': posts,
                  'posts': posts})


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published')
    
    return render(request,
                  'shop/post/detail.html',
            {
                  'post': post,
            })


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'shop/post/list.html'
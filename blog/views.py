from django.db.models import Count
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,\
    PageNotAnInteger
from taggit.models import Tag



from .models import Post 
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    tags = Post.tags.all
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator   = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
    'blog/post/list.html',
    {'page':page,
    'posts': posts,
    'tag':tag,  
    'tags':tags})

def post_detail(request, year,month,day,post):
    post = get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html',
                            {'post':post,
                            'similar_posts': similar_posts})                           

def post_share(request,post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data

            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f" {cd['name']} recommends you read " \
                        f" {post.title} "
            message = f" Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']} "
            send_mail(subject, message, 'mainulislamfaruqi@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post,
                                                'form':form,
                                                'sent':sent})

             



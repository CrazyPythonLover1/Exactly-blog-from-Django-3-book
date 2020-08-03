from django.db.models import Count
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,\
    PageNotAnInteger
from taggit.models import Tag



from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
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

     # List of active comments for this particular post 
    comments = post.comments.filter(active=True)
    tags = post.tags.all()
    new_comment = None
    if request.method == 'POST':
        # A Comment was Posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment Object (instance) but don't save to database yet
            # this comes in handy when you want to modify the object before finally saving it,
            # which is what you will do next.
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html',
                            {'post':post,
                            'similar_posts': similar_posts,
                            'tags':tags,
                            'comments':comments,
                            'new_comment':new_comment,
                            'comment_form':comment_form})                           

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

            


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            search_vector = SearchVector('title', weight='A') +\
                            SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank= SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
            # results = Post.published.annotate(
            #     search=SearchVector('title','body'),
            #     ).filter(search=query)


    return render(request,'blog/post/search.html',
                  {'form':form,
                  'query':query,
                  'results':results})
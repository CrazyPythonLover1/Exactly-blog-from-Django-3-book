from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse

from taggit.managers import TaggableManager
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset()\
                        .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published','Published'),
    )
    title    = models.CharField(max_length = 200)
    slug     = models.SlugField(max_length= 200,
                                unique_for_date='publish')
    author   = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='blog_posts')
    body     = models.TextField()
    publish  = models.DateField( default =timezone.now)
    # timezone.now method returns current datetime
    created  = models.DateField( auto_now_add=True)
    # auto_now_add will be saved automatically when
    # creating an object
    updated  = models.DateField( auto_now=True)
    # auto_now will be updated automatically when\
    #  saving an obj(showing last updated time)
    status   = models.CharField( max_length=10,
                                choices=STATUS_CHOICES,
                                default='darft')
    # This field shows the status of a psot.You use a chices parameter \
    # so the value of this field can only be set to one of the given choices.
    objects  = models.Manager() # the default manager.
    published= PublishedManager() # Our custom manager.

    tags = TaggableManager()


    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])
    

    def __str__(self):
        return self.title         


class Comment(models.Model):
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments')
 

    """The Relative_name attribute allows you to name the attribute that you use
    for the relationship from the related object back to this one. You can retrieve
    the post of a comment object using comment.post and retrieve all comments of a post
    using post.commets.all()  . If YOu don't define related_name attribute. 
    Django will use the name of the model in lowercase follwed by _set (that is, comment_set)
    to name the relationship of the related object of the model, where this relationship 
    has been defined."""

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
                                                                                                                                                                                                                                                                                                                                   
    

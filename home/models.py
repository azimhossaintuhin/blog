from django.db import models
from accounts.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


class Tag(models.Model):
    title = models.CharField(max_length=255 , blank=True, null = True)
    slug = models.SlugField(max_length=255 , blank=True, null = True)
    created_at = models.DateField(auto_now_add=True)



    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True , blank=True , null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Blog (models.Model):
    Banner = models.ImageField(upload_to = 'blog')
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='blog_user')
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name='blog_category')
    description = RichTextField()
    tags = models.ManyToManyField(Tag , related_name ='blog_tag', blank=True)
    likes = models.ManyToManyField(User,  blank=True, related_name ='blog_likes', )
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True , unique=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

class Comment(models.Model):
    user  = models.ForeignKey(User , related_name = 'user_comment', on_delete= models.CASCADE)
    blog = models.ForeignKey(Blog, related_name = 'blog_comment', on_delete= models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
       return self.user.username 

class replay(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name='comment_user', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True, null=True, related_name='replay_comment', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.user.username
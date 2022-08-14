from webbrowser import get
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.shortcuts import get_object_or_404, render , redirect
from django.db.models import Q
from .models import *
from django.http import JsonResponse
from home.forms import Textform , AddBlog
from django.contrib import messages


# Create your views here.
def index(request):
    blogs = Blog.objects.order_by('-created')
    tag = Tag.objects.order_by('-created_at')
    context = {'blogs':blogs,
                'tags':tag
              }   
    return render(request,'index.html',context)

def blog(request):
  queryset = Blog.objects.order_by('-created')
  tag = Tag.objects.order_by('-created_at')
  page = request.GET.get('page', 1)
  paginator = Paginator(queryset, 4)
  
  try:
    blog = paginator.page(page)
  except EmptyPage:
    blog =  paginator.page(1)
  except PageNotAnInteger:
    blog = paginator.page(1)

  context = {'blogs':blog,'tags':tag,'paginator':paginator}
  return render(request,'post.html',context)


def blog_datails(request, slug):
  form = Textform()
  blogs = Blog.objects.order_by('created')
  blog =  get_object_or_404(Blog, slug=slug)
  tag = Tag.objects.order_by('-created_at')
  liked_by = request.user in blog.likes.all()
  if request.method == 'POST' and request.user.is_authenticated:
    form =Textform(request.POST)
    if form.is_valid():
      Comment.objects.create(
          user = request.user,
          blog = blog,
          text = form.cleaned_data.get('text')
          
      )
      return redirect('blog_datails',slug = slug)
  context = {'blog':blog, 'blogs':blogs,'tags':tag,'form':form , "liked_by":liked_by}
  return render(request,'post_details.html',context)


def category_blog(request, slug):
  category = get_object_or_404(Category, slug=slug)
  queryset = category.blog_category.all()
  tags = Tag.objects.order_by('-created_at')[:5]
  print(queryset)
  
  page = request.GET.get('page', 1)
  paginator = Paginator(queryset, 3)
  
  try:
    blog = paginator.page(page)
  except EmptyPage:
    blog =  paginator.page(1)
  except PageNotAnInteger:
    blog = paginator.page(1)

  context = {'blogs':blog,'tags':tags,'paginator':paginator}
 
  return render(request,'category_blog.html',context)



def tags_blog(request, slug):
  tags = get_object_or_404(Tag, slug=slug)
  queryset = tags.blog_tag.all()
  category = Category.objects.all()[:3]
  all_tags = Tag.objects.all()
  print(queryset)
  page = request.GET.get('page', 1)
  paginator = Paginator(queryset, 3)
  
  try:
    blog = paginator.page(page)
  except EmptyPage:
    blog =  paginator.page(1)
  except PageNotAnInteger:
    blog = paginator.page(1)

  context = {'blogs':blog,'category':category, 'alltags':all_tags ,'paginator':paginator }
  return render(request,'tag_blog.html',context)


@login_required
def Replay(request, comment_id , blog_id):
   blog = get_object_or_404(Blog, id=blog_id)
   if request.method == "POST":
        form = Textform(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            replay.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
   return redirect('blog_datails', slug=blog.slug)
def like_blog(request, pk):
  context = {}
  blog = get_object_or_404(Blog, pk=pk) 
  if request.user in blog.likes.all():
    blog.likes.remove(request.user)
    context['liked'] = False
    context['like_count'] = blog.likes.all().count()
  else:
     blog.likes.add(request.user)
     context['liked'] = True
     context['like_count'] = blog.likes.all().count()
  return JsonResponse(context , safe=False)


def serch_blog(request):
  serch_key =  request.GET.get('search')
  recent_blog = Blog.objects.order_by('-created')
  print(serch_key)
  if serch_key:
    blogs = Blog.objects.filter(
      Q(title__icontains = serch_key)|
      Q(category__title__icontains = serch_key)|
      Q(tags__title__icontains = serch_key )

    ).distinct()
    context = {
      'blogs':blogs, 
      'recent_blogs': recent_blog
    }
    return render(request , 'search.html' , context)
  else:
    blogs = Blog.objects.all()
    context = {
      "blogs": blogs
    }
    return render(request , 'search.html' , context)
  

@login_required(login_url='login')
def my_blog(request):
  queryset = request.user.blog_user.all()
  
  page = request.GET.get('page', 1)
  paginator = Paginator(queryset, 3)
  delete =  request.GET.get('delete', False)

  if delete:
    blog = get_object_or_404(Blog , pk = delete)
    blog.delete()
    messages.success(request, 'blog deleted successfully')

  print(paginator)
  try:
    blog = paginator.page(page)
  except EmptyPage:
    blog =  paginator.page(1)
  except PageNotAnInteger:
    blog = paginator.page(1)
  context = {
    'blogs':blog,
    "paginator": paginator
  }
  return render(request, 'my_blogs.html',context)



@login_required(login_url='login')
def add_blog(request):
  form = AddBlog()
  
  if request.method == "POST":
    form = AddBlog(request.POST , request.FILES)
    
    if form.is_valid():
      user = get_object_or_404(User, pk=request.user.pk)
      category = get_object_or_404(Category, pk=request.POST['category'])
      tags = request.POST['tags'].split(',')
      blog = form.save(commit=False)
      blog.user = user
      blog.category = category
      form.save()

      for tag in tags:
        tag_input = Tag.objects.filter(
          title__iexact=tag.strip(),
          slug = slugify(tag.strip())
        )
        if tag_input.exists():
          t = tag_input.first()
          print(t)
          blog.tags.add(t)

        else:
          if tag != '':
            new_tag = Tag.objects.create(
              title = tag.strip(),
              slug = slugify(tag.strip())
            )
            blog.tags.add(new_tag)
      messages.success(request, "Blog added")
      return redirect('blog_datails', slug=blog.slug)
    
     


 
 
 
  context = {'form': form
  }
  return render(request, 'add_blog.html',context)


@login_required(login_url='login')
def update_blog(request , slug):
   
  blog = get_object_or_404(Blog, slug=slug)
  form = AddBlog(instance=blog)


  if request.method == "POST":
      form = AddBlog(request.POST, request.FILES, instance=blog)
          
      if form.is_valid():
              
              if request.user.pk != blog.user.pk:
                  return redirect('home')

              tags = request.POST['tags'].split(',')
              user = get_object_or_404(User, pk=request.user.pk)
              category = get_object_or_404(Category, pk=request.POST['category'])
              blog = form.save(commit=False)
              blog.user = user
              blog.category = category
              blog.save()

              for tag in tags:
                  tag_input = Tag.objects.filter(
                      title__iexact=tag.strip(),
                      slug=slugify(tag.strip())
                  )
                  if tag_input.exists():
                      t = tag_input.first()
                      blog.tags.add(t)

                  else:
                      if tag != '':
                          new_tag = Tag.objects.create(
                              title=tag.strip(),
                              slug=slugify(tag.strip())
                          )
                          blog.tags.add(new_tag)

              messages.success(request, "Blog updated successfully")
              return redirect('blog_datails', slug=blog.slug)
      else:
              print(form.errors)


  context = {
        "form": form,
        "blog": blog
    }
  return render(request, 'blog_update.html', context)
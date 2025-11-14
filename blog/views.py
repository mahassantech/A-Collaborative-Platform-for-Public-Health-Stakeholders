from django.shortcuts import render, redirect
from .forms import BlogForm
from .models import Blog

def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blog_list")
    else:
        form = BlogForm()
    
    return render(request, "blog/create_blog.html", {"form": form})

def blog_list(request):
    blogs = Blog.objects.all().order_by("-created_at")
    return render(request, "blog/blog_list.html", {"blogs": blogs})

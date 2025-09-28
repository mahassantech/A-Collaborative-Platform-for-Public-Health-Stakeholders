from django.shortcuts import render

# Create your views here.
def BlogPage(request):
    return render(request, "core/blog.html")
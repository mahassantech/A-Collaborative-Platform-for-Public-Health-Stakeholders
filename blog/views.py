from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment, Prescription
from .forms import BlogForm, CommentForm, PrescriptionForm 
from django.db.models import Case, When, Value, CharField
from blog.models import BlogPost, Prescription
from blog.forms import PrescriptionForm

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_list(request):
    """
    Show blogs depending on user role:
    - Doctor: only patient posts
    - Patient: all posts (including own)
    """
    if request.user.role == 'doctor':
        # Doctor sees only patient posts
        blogs = BlogPost.objects.filter(author__role='patient').order_by('-created_at')
    else:
        # Patient sees all posts
        blogs = BlogPost.objects.all().order_by('-created_at')

    return render(request, 'blog/blog_list.html', {'blogs': blogs})

@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    comment_form = CommentForm()
    prescription_form = PrescriptionForm()
    
    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                return redirect('blog_detail', pk=pk)
        elif 'prescription_submit' in request.POST and request.user.role == 'doctor':
            prescription_form = PrescriptionForm(request.POST)
            if prescription_form.is_valid():
                presc = prescription_form.save(commit=False)
                presc.blog = blog
                presc.doctor = request.user
                presc.save()
                return redirect('blog_detail', pk=pk)
    
    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comment_form': comment_form,
        'prescription_form': prescription_form,
    })

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('blog_list')

    patient_posts = BlogPost.objects.filter(author__role='patient').order_by('-created_at')

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if post_id:
            try:
                blog = BlogPost.objects.get(id=int(post_id))
            except BlogPost.DoesNotExist:
                # Safeguard: blog post not found
                return render(request, 'blog/doctor_dashboard.html', {
                    'patient_posts': patient_posts,
                    'prescription_form': PrescriptionForm(),
                    'error_message': 'Blog post not found. Please refresh the page and try again.'
                })

            form = PrescriptionForm(request.POST)
            if form.is_valid():
                presc = form.save(commit=False)
                presc.blog = blog
                presc.doctor = request.user
                presc.save()
                return redirect('doctor_dashboard')
        else:
            # post_id missing
            return render(request, 'blog/doctor_dashboard.html', {
                'patient_posts': patient_posts,
                'prescription_form': PrescriptionForm(),
                'error_message': 'Invalid submission. Post ID missing.'
            })
    else:
        form = PrescriptionForm()

    return render(request, 'blog/doctor_dashboard.html', {
        'patient_posts': patient_posts,
        'prescription_form': form,
    })

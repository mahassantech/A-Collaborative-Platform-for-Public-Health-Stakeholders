from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
from .models import BlogPost, Comment
from .forms import BlogForm, CommentForm 


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Author assign
            blog.save()
            return redirect('blog_list')
        else:
            # Debug: print errors
            print(form.errors)
    else:
        form = BlogForm()
    
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_list(request):
    category_id = request.GET.get('category')  # query param ?category=1
    blogs = BlogPost.objects.all().order_by('-created_at')
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    return render(request, 'blog/blog_list.html', {'blogs': blogs})



@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                # doctor advice only if checkbox submitted
                if request.user.role == "doctor" and request.POST.get("is_advice"):
                    comment.is_advice = True
                comment.save()
                return redirect('blog_detail', pk=pk)

    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comment_form': comment_form,
    })
    
    
@login_required
def doctor_dashboard(request):
    # Only doctors can access
    if request.user.role != 'doctor':
        return redirect('blog_list')

    # Patient posts
    patient_posts = BlogPost.objects.filter(author__role='patient').order_by('-created_at')

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment_text')

        if post_id and comment_text:
            try:
                blog = BlogPost.objects.get(id=int(post_id))
            except BlogPost.DoesNotExist:
                return render(request, 'blog/doctor_dashboard.html', {
                    'patient_posts': patient_posts,
                    'error_message': 'Blog post not found. Please refresh the page and try again.'
                })

            # Save comment as advice
            from .models import Comment
            Comment.objects.create(
                blog=blog,
                user=request.user,
                comment_text=comment_text,
                is_advice=True  # Mark as doctor advice
            )
            return redirect('doctor_dashboard')
        else:
            return render(request, 'blog/doctor_dashboard.html', {
                'patient_posts': patient_posts,
                'error_message': 'Invalid submission. Please provide comment text.'
            })

    return render(request, 'blog/doctor_dashboard.html', {
        'patient_posts': patient_posts,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
from .models import BlogPost, Comment,Notification
from .forms import BlogForm, CommentForm 
# views.py
from category.models import Category  # app name অনুযায়ী adjust করো


def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Author assign
            blog.save()
            form.save_m2m()  # ⭐ Must for ManyToManyField
            return redirect('blog_list')
        else:
            # Debug: print errors
            print(form.errors)
    else:
        form = BlogForm()
    
    return render(request, 'blog/blog_form.html', {'form': form})



def blog_list(request, category_slug=None):
    categories = Category.objects.all()
    selected_category = None
    blogs = BlogPost.objects.all().order_by('-created_at')

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        blogs = blogs.filter(category=selected_category)

    context = {
        'blogs': blogs,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'core/blog.html', context)



# comment 

def get_depth(comment):
    depth = 0
    while comment.parent:
        depth += 1
        comment = comment.parent
    return depth

@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.user = request.user

            parent_id = request.POST.get("parent_id")
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment

                    if parent_comment.user != request.user:
                        Notification.objects.create(
                            user=parent_comment.user,
                            message=f"{request.user.username} replied to your comment"
                        )
                except Comment.DoesNotExist:
                    comment.parent = None

            if request.user.role == "doctor" and request.POST.get("is_advice"):
                comment.is_advice = True

            comment.save()
            return redirect("blog_detail", pk=pk)

    top_comments = blog.comments.filter(parent__isnull=True)

    return render(
        request,
        "blog/blog_detail.html",
        {
            "blog": blog,
            "comment_form": comment_form,
            "top_comments": top_comments,
        },
    )


@login_required
def notifications(request):
    notes = request.user.notifications.order_by("-created_at")
    notes.update(is_read=True)
    return render(request, "blog/notifications.html", {"notes": notes})


    
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


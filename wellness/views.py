from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import WellnessPostForm, WellnessCommentForm
from django.http import HttpResponseForbidden
from .models import WellnessPost, WellnessComment



def wellness_list(request):
    posts = WellnessPost.objects.select_related('category', 'author')
    return render(request, 'wellness/list.html', {'posts': posts})


def wellness_detail(request, pk):
    post = get_object_or_404(WellnessPost, pk=pk)
    comments = post.comments.filter(parent__isnull=True)  # only top-level comments

    if request.method == 'POST' and request.user.is_authenticated:
        form = WellnessCommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            if parent_id:
                parent_comment = WellnessComment.objects.get(id=parent_id)
                comment.parent = parent_comment
            comment.save()
            return redirect('wellness_detail', pk=pk)
    else:
        form = WellnessCommentForm()

    return render(request, 'wellness/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })
    
@login_required
def wellness_create(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Only doctors can post")


    if request.method == 'POST':
        form = WellnessPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('wellness_list')
    else:
        form = WellnessPostForm()

    return render(request, 'wellness/create.html', {'form': form})


@login_required
def wellness_edit(request, pk):
    post = get_object_or_404(WellnessPost, pk=pk)

    # Role-based permission
    if request.user != post.author or request.user.role != 'doctor':
        return HttpResponseForbidden("You are not allowed to edit this post")

    if request.method == 'POST':
        form = WellnessPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('wellness_detail', pk=pk)
    else:
        form = WellnessPostForm(instance=post)

    return render(request, 'wellness/edit.html', {
        'form': form,
        'post': post
    })

@login_required
def wellness_delete(request, pk):
    post = get_object_or_404(WellnessPost, pk=pk)

    if request.user != post.author or request.user.role != 'doctor':
        return HttpResponseForbidden("You are not allowed")

    if request.method == 'POST':
        post.delete()
        return redirect('wellness_list')

    return render(request, 'wellness/delete.html', {'post': post})

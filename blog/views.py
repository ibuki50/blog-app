from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Category
from .forms import PostForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    authors = User.objects.all()
    categories = Category.objects.all()

    author = request.GET.get('author')
    category = request.GET.get('category')



    if author:
        posts = posts.filter(author__username=author)
    if category:
        posts = posts.filter(category__name=category)

    return render(request, 'blog/post_list.html', {'posts': posts, 'authors': authors, 'categories': categories})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('post_list')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post has been deleted.")
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def user_logout(request):
    logout(request)
    return redirect('post_list')
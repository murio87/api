from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from post.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from post.models import BlogPost


def create(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login-url')
    if request.method == 'POST':
        form = CreateBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a BlogPost object but do not save it to the database yet (commit=False)
            obj = form.save(commit=False)
            # Get the author from the Account model based on the user's email
            author = Account.objects.filter(email=user.email).first()
            obj.author = author  # Set the author for the BlogPost object
            obj.save()  # save the BlogPost object to the db

            messages.success(request, 'Successfully created')
            return redirect('home-url')

    else:
        form = CreateBlogPostForm()

    context = {'form': form}

    return render(request, 'post/create.html', context)


def detail_blog(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    context = {'blog_post': blog_post}

    return render(request, 'post/detail_blog.html', context)


def edit_blog(request, slug):
    if not request.user.is_authenticated:
        return redirect('authenticate-url')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = UpdateBlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect('home-url')

    form = UpdateBlogPostForm(instance=blog_post)
    return render(request, 'post/edit_blog.html', {'form': form})


def delete_blog(request, slug):
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate-url')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    # Check if the logged-in user is the author of the blog post
    if user == blog_post.author:
        # Delete the associated image file
        blog_post.image.delete(False)
        # Delete the blog post
        blog_post.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('home-url')


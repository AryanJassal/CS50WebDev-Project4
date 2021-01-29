from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import datetime
import json

from .models import User, Posts, Following, Like


def index(request):
    allPosts = Posts.objects.all()
    paginator = Paginator(allPosts, 10)

    pageNum = request.GET.get('page')
    posts = paginator.get_page(pageNum)

    return render(request, 'network/index.html', {
        'posts': posts
    })


def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('index')
        else:
            errors = ['Invalid username and/or password.']

        if errors:
            return render(request, 'network/login.html', {
                'errors': errors
            })
    else:
        return render(request, 'network/login.html')


def logout_(request):
    logout(request)

    return redirect('index')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        email = 'someone@emailprovider.com'
        errors = []

        if password != confirm:
            errors.append('The passwords do not match.')

        if User.objects.filter(username=username).exists():
            errors.append('A user with the provided username already exists.')

        if errors:
            return render(request, 'network/register.html', {
                'errors': errors
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)

        return redirect('index')

    else:
        return render(request, 'network/register.html')


def newPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            content = request.POST.get('content')

            post = Posts(
                user=request.user,
                content=content,
                likes=0
            )

            post.save()

            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')


def following(request):
    if request.user.is_authenticated:
        followers = Following.objects.filter(follower=request.user)
        allPosts = Posts.objects.all()

        posts = []

        for post in allPosts:
            for person in followers:
                if post.user == person.following:
                    posts.append(post)

        return render(request, 'network/following.html', {
            'posts': posts
        })
    else:
        return redirect('index')


def likePost(request):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            data = json.loads(request.body)

            if data.get('postID') is not None:
                post = Posts.objects.get(pk=data['postID'])

                like = Like.objects.filter(user=request.user, post=post).first()

                if like is not None:
                    like.delete()
                    post.likes -= 1
                    post.save()
                else:
                    newLike = Like(
                        user=request.user,
                        post=post
                    )
                    newLike.save()

                    post.likes += 1
                    post.save()

            return HttpResponse(json.dumps({
                'likes': Posts.objects.get(pk=data['postID']).likes
            }))
        else:
            return redirect('index')
    else:
        return redirect('index')


def profile(request, username):
    if request.user.is_authenticated:
        follower = Following.objects.filter(follower=request.user, following=User.objects.get(username=username)).first()

        if follower is not None:
            isFollowing = True
        else:
            isFollowing = False

        user_ = User.objects.get(username=username)

        return render(request, 'network/profile.html', {
            'user_': user_,
            'following': isFollowing,
            'followingNum': Following.objects.filter(follower=user_).count(),
            'followerNum': Following.objects.filter(following=user_).count(),
            'posts': Posts.objects.filter(user=user_)
        })
    else:
        return redirect('index')


def toggleFollowing(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)

        entry = Following.objects.filter(follower=request.user, following=user).first()

        if entry is not None:
            entry.delete()
        else:
            newFollow = Following(
                follower=request.user,
                following=user
            )
            newFollow.save()

        return redirect('profile', username=username)
    else:
        return redirect('index')


def editPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            body = json.loads(request.body)
            postID = body['postID']
            newText = body['newText']

            post = Posts.objects.get(pk=postID)
            post.content = newText
            post.modified = datetime.now()
            post.save()

            return HttpResponse('Post edited.')
        else:
            return redirect('index')
    else:
        return redirect('index')


def deletePost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            body = json.loads(request.body)
            postID = body['postID']

            post = Posts.objects.get(pk=postID)
            post.delete()

            return HttpResponse('Deleted')
        else:
            return redirect('index')
    else:
        return redirect('index')


def haveLiked(request):
    if request.user.is_authenticated:
        body = json.loads(request.body)
        postID = body['postID']

        post = Like.objects.filter(user=request.user, post=postID).first()

        if post is not None:
            return HttpResponse(json.dumps({
                'status': 1
            }))
        else:
            return HttpResponse(json.dumps({
                'status': 0
            }))

    else:
        return redirect('index')


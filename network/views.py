from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'network/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'network/login.html')


def logout_(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        email = 'someone@emailprovider.com'

        if password != confirmPassword:
            return render(request, 'network/register.html', {
                'message': 'The passwords do not match.'
            })

        if len(password) < 6:
            return render(request, 'network/register.html', {
                'message': 'The password must be atleast 6 characters long.'
            })

        if len(username) > 32:
            return render(request, 'network/register.html', {
                'message': 'The selected username is too long. (max 32 characters)'
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'network/register.html', {
                'message': 'The username is already taken.'
            })

        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'network/register.html')


def newPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            content = request.POST['content']

            post = Posts(
                user=request.user,
                content=content,
                likes=0
            )

            post.save()

            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


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
        return HttpResponseRedirect(reverse('index'))


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
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


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
        return HttpResponseRedirect(reverse('index'))


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

        return HttpResponseRedirect(reverse('profile', kwargs={'username': user}))
    else:
        return HttpResponseRedirect(reverse('index'))


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
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


def deletePost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            body = json.loads(request.body)
            postID = body['postID']

            post = Posts.objects.get(pk=postID)
            post.delete()

            return HttpResponse('Deleted')
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


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
        return HttpResponseRedirect(reverse('index'))


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.utils.timesince import timesince
from .models import Profile, Post, Like, Comment, Follow, Notification
from .forms import RegisterForm, LoginForm, PostForm, ProfileForm, CommentForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to SocialSpace, {user.username}!')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'feed')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def feed_view(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(
        Q(author__in=following_ids) | Q(author=request.user)
    ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))

    suggested_users = User.objects.exclude(
        Q(id=request.user.id) | Q(id__in=following_ids)
    ).select_related('profile')[:5]

    return render(request, 'feed.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'post_form': PostForm(),
        'comment_form': CommentForm(),
        'suggested_users': suggested_users,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
    return redirect('feed')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('feed')


@login_required
def toggle_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
            # Remove the notification when unliking
            Notification.objects.filter(
                sender=request.user,
                recipient=post.author,
                notification_type=Notification.LIKE,
                post=post,
            ).delete()
        else:
            liked = True
            # Notify post author (not for own posts)
            if post.author != request.user:
                Notification.objects.get_or_create(
                    sender=request.user,
                    recipient=post.author,
                    notification_type=Notification.LIKE,
                    post=post,
                )
        return JsonResponse({'liked': liked, 'count': post.likes_count})
    return JsonResponse({'error': 'Invalid method'}, status=405)


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content', '').strip()
        if content:
            comment = Comment.objects.create(author=request.user, post=post, content=content)
            # Notify post author (not for own comments)
            if post.author != request.user:
                Notification.objects.create(
                    sender=request.user,
                    recipient=post.author,
                    notification_type=Notification.COMMENT,
                    post=post,
                )
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'author': request.user.username,
                'author_avatar': request.user.profile.get_avatar_url(),
                'content': comment.content,
                'created_at': comment.created_at.strftime('%b %d, %Y'),
                'count': post.comments_count,
            })
        return JsonResponse({'success': False, 'error': 'Empty comment'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_id = comment.post_id
    comment.delete()
    post = Post.objects.get(id=post_id)
    return JsonResponse({'success': True, 'count': post.comments_count})


@login_required
def toggle_follow(request, username):
    if request.method == 'POST':
        target = get_object_or_404(User, username=username)
        if target == request.user:
            return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
            following = False
            Notification.objects.filter(
                sender=request.user,
                recipient=target,
                notification_type=Notification.FOLLOW,
            ).delete()
        else:
            following = True
            Notification.objects.get_or_create(
                sender=request.user,
                recipient=target,
                notification_type=Notification.FOLLOW,
                defaults={'post': None},
            )
        return JsonResponse({
            'following': following,
            'followers_count': target.profile.followers_count,
        })
    return JsonResponse({'error': 'Invalid method'}, status=405)


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    is_following = False
    liked_post_ids = set()
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))

    followers = Follow.objects.filter(following=profile_user).select_related('follower__profile')
    following = Follow.objects.filter(follower=profile_user).select_related('following__profile')

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'liked_post_ids': liked_post_ids,
        'followers': followers,
        'following_list': following,
        'comment_form': CommentForm(),
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            if 'first_name' in request.POST:
                request.user.first_name = request.POST.get('first_name', '')
                request.user.last_name = request.POST.get('last_name', '')
                request.user.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})


def explore_view(request):
    query = request.GET.get('q', '')
    users = []
    posts = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).select_related('profile').exclude(id=request.user.id if request.user.is_authenticated else None)[:10]
        posts = Post.objects.filter(content__icontains=query).select_related('author', 'author__profile')[:20]
    else:
        posts = Post.objects.all().select_related('author', 'author__profile').prefetch_related('likes', 'comments')[:30]

    liked_post_ids = set()
    following_ids = set()
    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))

    return render(request, 'explore.html', {
        'query': query,
        'users': users,
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'following_ids': following_ids,
        'comment_form': CommentForm(),
    })


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).select_related(
        'sender__profile', 'post'
    )
    # Mark all as read when the page is opened
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def notifications_unread(request):
    """API endpoint polled by the frontend every 10 s."""
    unread = Notification.objects.filter(recipient=request.user, is_read=False).select_related(
        'sender__profile', 'post'
    )
    data = []
    for n in unread[:10]:
        data.append({
            'id': n.id,
            'type': n.notification_type,
            'message': n.get_message(),
            'sender': n.sender.username,
            'sender_avatar': n.sender.profile.get_avatar_url(),
            'post_id': n.post_id,
            'time': timesince(n.created_at) + ' ago',
        })
    return JsonResponse({'count': len(data), 'notifications': data})


@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'ok': True})
    return JsonResponse({'error': 'Invalid method'}, status=405)

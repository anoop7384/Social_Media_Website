from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Notification
from django.contrib.auth.models import User
from users.models import Profile
from django.http import HttpResponseRedirect
from django.utils import timezone
from chatrooms.views import ChatRoom, Message


# Create your views here.
posts = []


def home(request):
    return redirect('login')


class PostListView(ListView):
    model = Post
    template_name = 'connect/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add objects of AnotherModel to the context
        context['comments'] = Comment.objects.all()
        context['chats'] = ChatRoom.objects.filter(sender=self.request.user)
        return context


def main_profile(request):
    context = {
        'title': 'My Posts',
        'posts': Post.objects.filter(author=request.user),
    }
    return render(request, 'connect/profile.html', context)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add objects of AnotherModel to the context
        post_instance = self.object
        context['comments'] = Comment.objects.filter(post=post_instance)
        context['chats'] = ChatRoom.objects.filter(sender=self.request.user)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add objects of AnotherModel to the context
        context['chats'] = ChatRoom.objects.filter(sender=self.request.user)
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add objects of AnotherModel to the context
        context['chats'] = ChatRoom.objects.filter(sender=self.request.user)
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    fields = ['constent', 'image']
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add objects of AnotherModel to the context
        context['chats'] = ChatRoom.objects.filter(sender=self.request.user)
        return context


def profile(request):
    context = {
        'title': 'My Posts',
        'posts': Post.objects.all(),
    }
    return render(request, 'connect/home.html', context)


def user_profile(request, pk):
    obj = User.objects.get(pk=pk)
    context = {
        'title': 'User Profile',
        'account': obj,
        'user': request.user,
        'posts': Post.objects.filter(author=obj),
    }
    return render(request, 'connect/user_profile.html', context)


def create(request):
    return render(request, 'connect/create.html', {'title': 'Create Post'})


def comment(request, pk):
    obj = Post.objects.get(pk=pk)
    text = request.POST.get('textfield')
    new_comment = Comment.objects.create(
        post=obj, author=request.user, text=text, date_commented=timezone.now())
    new_comment.save()
    notification1 = Notification(
        user=obj.author, sender=request.user, notification_type="comment",post=obj,comment=new_comment)
    notification1.save()
    return redirect('connect-profile')


def saving(request, pk):
    logUser = Profile.objects.get(user=request.user)
    obj = Post.objects.get(pk=pk)
    logUser.savedPosts.add(obj)
    logUser.save()
    return redirect('connect-profile')


def unsaving(request, pk):
    logUser = Profile.objects.get(user=request.user)
    obj = Post.objects.get(pk=pk)
    logUser.savedPosts.remove(obj)
    logUser.save()
    return redirect('connect-profile')


def liked(request, pk):
    logUser = Profile.objects.get(user=request.user)
    obj = Post.objects.get(pk=pk)
    logUser.likedPosts.add(obj)
    obj.likes += 1
    obj.save()
    logUser.save()
    notification1 = Notification(
        user=obj.author, sender=request.user, notification_type="like", post=obj)
    notification1.save()
    return redirect('connect-profile')


def unliked(request, pk):
    logUser = Profile.objects.get(user=request.user)
    obj = Post.objects.get(pk=pk)
    logUser.likedPosts.remove(obj)
    obj.likes -= 1
    obj.save()
    logUser.save()
    return redirect('connect-profile')


@login_required
def saved(request):
    logUser = Profile.objects.get(user=request.user)
    context = {
        'title': 'Saved Posts',
        'posts': logUser.savedPosts.all(),
    }
    return render(request, 'connect/saved.html', context)


@login_required
def posts(request):
    logUser = Profile.objects.get(user=request.user)
    context = {
        'title': 'All Posts',
        'posts': Post.objects.all(),
    }
    return render(request, 'connect/posts.html', context)


def user_posts(request, pk):
    obj = User.objects.get(pk=pk)
    context = {
        'title': 'All Posts',
        'posts': Post.objects.all(),
        'account': obj,
    }
    return render(request, 'connect/user_posts.html', context)


def search(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        profiles = User.objects.filter(
            username__icontains=username)

        context = {
            'profiles': profiles,
            'search_query': username
        }
        return render(request, 'connect/search_bar.html', context)

    return render(request, 'connect/search_bar.html')


@login_required
def follow(request, pk):
    if request.method == 'POST':
        user = request.user
        account = User.objects.get(pk=pk)

        if account.profile.followers.filter(id=user.id).exists():
            account.profile.followers.remove(user)
            user.profile.following.remove(account)
        elif account.profile.follower_requests.filter(id=user.id).exists():
            account.profile.follower_requests.remove(user)
            user.profile.following_requests.remove(account)
        else:
            if (account.profile.is_private):
                account.profile.follower_requests.add(user)
                user.profile.following_requests.add(account)
                notification1 = Notification(
                    user=account, sender=user, notification_type="follow-request")
                notification1.save()
            else:
                account.profile.followers.add(user)
                user.profile.following.add(account)
                notification1 = Notification(
                    user=account, sender=user, notification_type="following")
                notification1.save()
        account.save()
        user.save()
        context = {
            'title': 'User Profile',
            'account': account,
            'user': request.user,
            'posts': Post.objects.filter(author=account),
        }
        return render(request, 'connect/user_profile.html', context)


@login_required
def notification(request):
    context = {
        'title': 'Notifications',
        'user': request.user,
        'notifs': Notification.objects.filter(user=request.user),
        'requests': request.user.profile.follower_requests.all(),
    }
    return render(request, 'connect/notification.html', context)


@login_required
def followrequest(request, pk):
    user = request.user
    account = User.objects.get(pk=pk)
    if request.method == 'POST':
        if 'accept' in request.POST:
            account.profile.following.add(user)
            user.profile.followers.add(account)
            notification1 = Notification(
                user=account, sender=user, notification_type="accept-request")
            notification2 = Notification(
                user=user, sender=account, notification_type="following")
            notification1.save()
            notification2.save()
        else:
            account.profile.following_requests.remove(user)
            user.profile.follower_requests.remove(account)
        account.save()
        user.save()
    return redirect('notify')

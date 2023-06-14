from django.urls import path,include
from . import views
from chatrooms.views import chatroom
from users import views as loginV
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='connect-home'),
    path('profile/', PostListView.as_view(), name='connect-profile'),
    path('mainprofile/', views.main_profile, name='main-profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='connect-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/save/', views.saving, name='post-save'),
    path('post/<int:pk>/unsave/', views.unsaving, name='post-unsave'),
    path('post/<int:pk>/like/', views.liked, name='post-like'),
    path('post/<int:pk>/unlike/', views.unliked, name='post-unlike'),
    path('post/<int:pk>/comment/', views.comment, name='post-comment'),
    path('posts/', views.posts, name='connect-posts'),
    path('posts/saved', views.saved, name='connect-saved'),
    path('posts/account/<int:pk>', views.user_posts, name='post-account'),
    path('profile/account/<int:pk>', views.user_profile, name='profile-account'),
    path('profile/search', views.search, name='profile-search'),
    path('profile/follow/<int:pk>', views.follow, name='follow'),
    path('', include('chatrooms.urls')),
]


# urlpatterns += static(settings.MEDIA_URL, documnet_root=settings.MEDIA_ROOT)

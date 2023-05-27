from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('chatroom/<int:pk>', views.chatroom, name='chatroom'),

]

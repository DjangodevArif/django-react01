from django.urls import path

from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='homeapi'),
    path('<int:pk>/', PostDetail.as_view(), name='singleapi'),
    path('<int:pk>/comments/', CommentList.as_view(), name='comment'),


]

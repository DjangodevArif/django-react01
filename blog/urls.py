from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='homeapi'),
    path('<int:pk>/', PostDetail.as_view(), name='singleapi'),
    path('like/', LikeView.as_view(), name='likeapi'),
    path('comments/', CommentList.as_view(), name='comment'),
    path('subcomments/', SubCommentList.as_view(), name='comment'),
    path('catelog/', CategoryList.as_view(), name='catogory'),
    path('com_sub/<model>/<int:pk>/',
         CommSubView.as_view(), name='comment_subcomment'),
    path('most_popular/', TopRatedCategory.as_view(), name='popular_category'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('new_user/', UserCreateView.as_view(), name='new_user'),
    path('<title>/', CategoryView.as_view(), name='category_view'),

]

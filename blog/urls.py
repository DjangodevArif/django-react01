from django.urls import path

from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', PostList.as_view(), name='homeapi'),
    path('<int:pk>/', PostDetail.as_view(), name='singleapi'),
    path('<int:pk>/comments/', CommentList.as_view(), name='comment'),
    path('catelog/', CategoryList.as_view(), name='catogory'),
    path('most_popular/', TopRatedCategory.as_view(), name='popular_category'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<title>/', CategoryView.as_view(), name='category_view'),

]

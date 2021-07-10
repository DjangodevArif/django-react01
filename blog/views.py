from django.apps import apps
from django.db.models import Count
from django.db.models.aggregates import Max
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *
from .serializers import *

# Create your views here.


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-post_date')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        category = Category.objects.get(
            title=self.request.data['post_category'])
        serializer.save(post_author=self.request.user, post_category=category)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CommentList(generics.CreateAPIView):
    queryset = Comment.objects.all().order_by('-comment_date')
    serializer_class = CommentSerializers

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user,
                        post_id=Post.objects.get(id=self.request.data.get('post_id')))


class SubCommentList(generics.CreateAPIView):
    queryset = SubComment.objects.all().order_by('-comment_date')
    serializer_class = SubCommentSerializers

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user,
                        main_comment=Comment.objects.get(id=self.request.data.get('main_comment')))


class CommSubView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializers

    def get_queryset(self):
        model = apps.get_model('blog', self.kwargs['model'])
        data = model.objects.filter(id=self.kwargs['pk'])
        return data

    def get_serializer_class(self):
        model = apps.get_model('blog', self.kwargs['model'])
        if model == Comment:
            return CommentSerializers
        return SubCommentSerializers


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class TopRatedCategory(APIView):

    def get(self, request):
        all = Category.objects.annotate(
            entries=Count('post'))
        post = Category.objects.annotate(
            entries=Count('post')).aggregate(Max('entries'))
        get = all.filter(entries=post['entries__max'])
        serialize = CategorySerializers(
            get, many=True, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class CategoryView(APIView):

    def get(self, request, *args, **kwargs):
        kwarg = kwargs.get('title')
        category = Category.objects.filter(title__icontains=kwarg)
        serialize = CategorySerializers(
            category, many=True, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class UserCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LikeView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.data['post_id'])
        if request.user in post.post_like.all():
            post.post_like.remove(request.user)
        else:
            post.post_like.add(request.user)
        return Response(status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


'''    
q = Category.objects.annotate(entries=Count('post')).aggregate(Max('entries'
))
'''

from django.db.models import Count
from django.db.models.aggregates import Max
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

# Create your views here.


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-post_date')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(post_author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user,
                        post_id=Post.objects.get(id=self.kwargs.get('pk')))


class CategoryList(generics.ListAPIView):
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


'''    
q = Category.objects.annotate(entries=Count('post')).aggregate(Max('entries'
))
'''

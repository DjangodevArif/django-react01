from rest_framework import generics, permissions
from django.http import HttpRequest, request

from .models import *
from .serializers import *

# Create your views here.


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-post_date')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    # ordering = ['post_like']

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


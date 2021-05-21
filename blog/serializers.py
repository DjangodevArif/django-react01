from rest_framework import serializers

from blog.models import *


class PostSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='singleapi', lookup_field='pk',
    )
    author = serializers.SerializerMethodField()
    post_like = serializers.SerializerMethodField()
    post_comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'url',
            'author',
            'post_img',
            'post_title',
            'post_detail',
            'post_date',
            'post_like',
            'post_comment'
        )

    def get_author(self, obj):
        return obj.post_author.username

    def get_post_like(self, obj):
        liker = obj.post_like.all().count()
        return liker

    def get_post_comment(self, obj):
        return obj.comment_set.count()


class PostDetailSerializer(serializers.ModelSerializer):

    post_author = serializers.SerializerMethodField()
    post_like = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comment_url = serializers.HyperlinkedIdentityField(
        view_name='comment', lookup_field='pk',
    )

    class Meta:
        model = Post
        fields = (
            'post_author',
            'post_img',
            'post_title',
            'post_detail',
            'post_date',
            'post_like',
            'comments',
            'comment_url',
        )
        read_only_fields = [
            'post_img', 'post_date',
        ]

    def get_post_author(self, obj):
        return obj.post_author.username

    def get_post_like(self, obj):
        liker = obj.post_like.all().count()
        return liker

    def get_comments(self, obj):
        rel_comment = obj.comment_set.all()
        return CommentSerializers(rel_comment, many=True,).data


class CommentSerializers(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('post_id',
                  'comment_author',
                  'comment_detail',
                  'comment_date',
                  )

    def get_comment_author(self, obj):
        return obj.comment_author.username

    def get_post_id(self, obj):
        return obj.post_id.post_title[:30]

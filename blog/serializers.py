from django.utils import timezone
from rest_framework import serializers

from blog.models import *


class PostSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='singleapi', lookup_field='pk',
    )
    author = serializers.SerializerMethodField()
    post_like = serializers.SerializerMethodField()
    post_date = serializers.SerializerMethodField()
    post_comment = serializers.SerializerMethodField()
    post_category = serializers.ChoiceField(
        choices=Category.objects.values_list('title', flat=True))

    class Meta:
        model = Post
        fields = (
            'url',
            'id',
            'author',
            'post_img',
            'post_title',
            'post_detail',
            'post_date',
            'post_like',
            'post_comment',
            'post_category'
        )

    def get_post_date(self, obj):
        timestamp = timezone.now()-obj.post_date
        if timestamp.days < 1:
            minute = round(timestamp.seconds/60)

            if minute > 60:
                return f"{round(minute/60)} hours ago"
            return f"{minute} minutes ago"

        elif timestamp.days == 1:
            return f'yesterday at {obj.post_date.strftime(" %I %p")}'

        elif timestamp.days > 1 and timestamp.days <= 3:
            return f'{timestamp.days} days ago  at {obj.post_date.strftime(" %I %p")}'

        return obj.post_date.strftime("%a %d. %B %Y %I:%M:%S")

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
    post_category = serializers.ChoiceField(
        choices=Category.objects.values_list('title', flat=True))

    class Meta:
        model = Post
        fields = (
            'post_author',
            'post_img',
            'post_title',
            'post_detail',
            'post_date',
            'post_like',
            'post_category',
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


class CategorySerializers(serializers.ModelSerializer):

    post = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'title', 'post'
        )

    def get_post(self, obj):
        data = obj.post_set.all().order_by('-post_date')
        print('self', self.context['request'])
        return PostSerializer(data, many=True, context={'request': self.context['request']}).data


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

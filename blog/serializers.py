from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
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
    # post_category = serializers.ChoiceField(
    #     choices=Category.objects.values_list('title', 'pk'), allow_blank=True, allow_null=True)

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
    # post_category = serializers.ChoiceField(
    #     choices=Category.objects.values_list('title', 'pk'), allow_blank=True)

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
        )
        read_only_fields = [
            'post_img', 'post_date',
        ]
        extra_kwargs = {
            'post_date': {'format': '%a %d. %B %Y %I %S %p'},
        }

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
        return PostSerializer(data, many=True, context={'request': self.context['request']}).data


class CommentSerializers(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()
    subcomment = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id',
                  'post_id',
                  'comment_author',
                  'comment_detail',
                  'comment_date',
                  'subcomment',
                  )
        extra_kwargs = {
            'comment_date': {'format': '%a %d. %B %Y %I %S %p'},
        }

    def get_comment_author(self, obj):
        return obj.comment_author.username

    def get_post_id(self, obj):
        return obj.post_id.post_title[:30]

    def get_subcomment(self, obj):
        return SubCommentSerializers(obj.subcomment_set.all().order_by('-comment_date'), many=True,).data


class SubCommentSerializers(serializers.ModelSerializer):

    main_comment = serializers.CharField()
    comment_author = serializers.StringRelatedField()

    class Meta:
        model = SubComment
        fields = '__all__'
        extra_kwargs = {
            'comment_date': {'format': '%a %d. %B %Y %I %S %p'},
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password'

        )

    def validate_password(self, attrs):
        validator = [password_validation.CommonPasswordValidator(
        ), password_validation.NumericPasswordValidator(), password_validation.MinimumLengthValidator()]
        password_validation.validate_password(
            password=attrs, password_validators=validator)
        attrs = make_password(attrs)
        return attrs

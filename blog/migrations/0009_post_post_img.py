# Generated by Django 3.2.3 on 2021-07-02 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_post_post_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_img',
            field=models.URLField(max_length=500, null=True),
        ),
    ]

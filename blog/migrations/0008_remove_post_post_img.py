# Generated by Django 3.2.3 on 2021-07-02 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_delete_myuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_img',
        ),
    ]

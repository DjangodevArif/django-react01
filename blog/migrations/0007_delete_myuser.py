# Generated by Django 3.2.3 on 2021-07-01 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('blog', '0006_auto_20210701_2203'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Myuser',
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-26 10:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_remove_post_categories_response_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 4.2.11 on 2024-03-18 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bba_admin', '0006_blog_loc_all_alter_blog_blog_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='long_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

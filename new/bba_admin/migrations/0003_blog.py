# Generated by Django 4.2.11 on 2024-03-14 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bba_admin', '0002_homeblocksection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(blank=True, max_length=255, null=True)),
                ('blog_slug', models.CharField(blank=True, max_length=255, null=True)),
                ('short_description', models.CharField(blank=True, max_length=255, null=True)),
                ('long_description', models.CharField(blank=True, max_length=255, null=True)),
                ('blog_image', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_keyword', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bba_admin.location')),
            ],
        ),
    ]

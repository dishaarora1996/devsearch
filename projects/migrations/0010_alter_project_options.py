# Generated by Django 4.2.1 on 2023-05-18 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_review_owner_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]
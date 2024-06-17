# Generated by Django 5.0.6 on 2024-06-17 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_blogpost_chead1_remove_blogpost_chead2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='chead0',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='author',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='para',
            field=models.CharField(default='', max_length=100000),
        ),
    ]

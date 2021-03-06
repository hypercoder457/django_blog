# Generated by Django 3.1.4 on 2021-01-03 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_blogs', '0002_alter_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'That email is already taken.'}, help_text='Required. Email addresses must be unique.', max_length=254, unique=True, verbose_name='Email address'),
        ),
    ]

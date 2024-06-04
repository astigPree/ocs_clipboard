# Generated by Django 4.2.11 on 2024-05-24 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StickyNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=13)),
                ('nickname_color', models.CharField(max_length=5)),
                ('nickname_font', models.CharField(max_length=20)),
                ('content', models.TextField(max_length=155)),
                ('content_color', models.CharField(max_length=5)),
                ('content_font', models.CharField(max_length=20)),
                ('emoji', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Clipboard',
        ),
    ]

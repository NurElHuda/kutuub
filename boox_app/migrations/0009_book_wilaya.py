# Generated by Django 4.0.3 on 2022-04-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boox_app', '0008_book_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='wilaya',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Wilaya'),
        ),
    ]

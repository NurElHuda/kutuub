# Generated by Django 4.0.3 on 2022-04-11 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boox_app', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='Cover'),
        ),
    ]
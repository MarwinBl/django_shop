# Generated by Django 2.1 on 2018-10-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20181017_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='avatar',
            field=models.ImageField(default='users_avatar/default_user.png', upload_to='users_avatar'),
        ),
    ]

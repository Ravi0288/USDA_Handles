# Generated by Django 4.2 on 2024-09-27 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.CharField(choices=[('logout', 'logout'), ('mint-handles-api', 'mint-handles-api'), ('api-root', 'api-root'), ('login', 'login'), ('mint-handles', 'mint-handles')], max_length=100)),
                ('groups', models.ManyToManyField(to='auth.group')),
            ],
        ),
    ]
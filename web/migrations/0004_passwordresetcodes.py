# Generated by Django 5.0 on 2024-05-29 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passwordresetcodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=120)),
                ('username', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]

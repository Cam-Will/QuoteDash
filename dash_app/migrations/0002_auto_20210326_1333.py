# Generated by Django 2.2.4 on 2021-03-26 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dash_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted', to='dash_app.User'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='users_liked',
            field=models.ManyToManyField(related_name='liked', to='dash_app.User'),
        ),
    ]

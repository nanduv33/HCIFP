# Generated by Django 3.1.5 on 2022-04-13 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coloring', '0002_drawing'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawing',
            name='drawing',
            field=models.JSONField(default=dict),
        ),
    ]
# Generated by Django 3.2.13 on 2022-05-29 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0005_auto_20220529_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crev_likes',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.creview'),
        ),
        migrations.AlterField(
            model_name='prev_likes',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.preview'),
        ),
    ]

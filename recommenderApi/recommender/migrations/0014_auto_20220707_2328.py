# Generated by Django 3.2.13 on 2022-07-07 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0013_auto_20220707_1322'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cquestion',
            options={'ordering': ('-upvotesCounter', '-answersCounter', '-time')},
        ),
        migrations.AlterModelOptions(
            name='creview',
            options={'ordering': ('-likesCounter', '-commentsCounter', '-time')},
        ),
        migrations.AlterModelOptions(
            name='pquestion',
            options={'ordering': ('-upvotesCounter', '-answersCounter', '-time')},
        ),
        migrations.AlterModelOptions(
            name='preview',
            options={'ordering': ('-likesCounter', '-commentsCounter', '-time')},
        ),
    ]

# Generated by Django 2.2.2 on 2019-07-06 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('klazor', '0007_auto_20190705_1316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='subtopics',
            new_name='subtopic_set',
        ),
    ]
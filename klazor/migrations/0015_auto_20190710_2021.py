# Generated by Django 2.2.3 on 2019-07-10 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('klazor', '0014_auto_20190710_0752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtubecell',
            old_name='url',
            new_name='youtube',
        ),
    ]
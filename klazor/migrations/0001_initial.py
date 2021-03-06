# Generated by Django 2.2.4 on 2019-09-04 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_klazor.cell_set+', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'cell',
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='klazor.Folder')),
            ],
            options={
                'db_table': 'folder',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_klazor.instructor_set+', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'instructor',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='klazor.Folder')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_klazor.item_set+', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'item',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RatedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'rated_item',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='AudioCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'audio_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Item')),
                ('release_date', models.DateField(blank=True, null=True)),
                ('instructor_set', models.ManyToManyField(blank=True, to='klazor.Instructor')),
            ],
            options={
                'db_table': 'course',
            },
            bases=('klazor.item',),
        ),
        migrations.CreateModel(
            name='FileCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'file_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='FileItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Item')),
                ('file', models.FileField(null=True, upload_to='files')),
            ],
            options={
                'db_table': 'file',
            },
            bases=('klazor.item',),
        ),
        migrations.CreateModel(
            name='ImageCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('scale', models.FloatField(default=1)),
            ],
            options={
                'db_table': 'image_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='MarkdownCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('text', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'markdown_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceInputCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
            ],
            options={
                'db_table': 'multiple_choice_input_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='NumericalInputCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('answer', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'numerical_input_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='OpenEndedInputCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('answer', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'open_ended_input_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('instructor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Instructor')),
                ('colloquial_name', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'db_table': 'school',
            },
            bases=('klazor.instructor',),
        ),
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Item')),
            ],
            options={
                'db_table': 'sheet',
            },
            bases=('klazor.item',),
        ),
        migrations.CreateModel(
            name='VideoCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('scale', models.FloatField(default=1)),
            ],
            options={
                'db_table': 'video_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='YoutubeCell',
            fields=[
                ('cell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Cell')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('scale', models.FloatField(default=1)),
            ],
            options={
                'db_table': 'youtube_cell',
            },
            bases=('klazor.cell',),
        ),
        migrations.CreateModel(
            name='SharedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klazor.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'shared_item',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='tag_set',
            field=models.ManyToManyField(blank=True, to='klazor.Tag'),
        ),
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField(blank=True, null=True)),
                ('is_true', models.BooleanField(default=False)),
                ('input_cell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klazor.MultipleChoiceInputCell')),
            ],
            options={
                'db_table': 'proposition',
            },
        ),
        migrations.CreateModel(
            name='NoteBook',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Item')),
                ('sheet_set', models.ManyToManyField(blank=True, to='klazor.Sheet')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('klazor.item',),
        ),
        migrations.CreateModel(
            name='CoursePart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='Week', max_length=32)),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('level', models.SmallIntegerField(default=1)),
                ('sequence', models.SmallIntegerField(default=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klazor.Course')),
            ],
            options={
                'db_table': 'course_part',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='resource_set',
            field=models.ManyToManyField(blank=True, to='klazor.FileItem'),
        ),
        migrations.AddField(
            model_name='cell',
            name='sheet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klazor.Sheet'),
        ),
        migrations.CreateModel(
            name='CourseElement',
            fields=[
                ('sheet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='klazor.Sheet')),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('course_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klazor.CoursePart')),
            ],
            options={
                'db_table': 'course_element',
                'ordering': ['sequence'],
            },
            bases=('klazor.sheet',),
        ),
    ]

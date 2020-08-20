import core.models
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asteroid',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Name')),
                ('nasa_jpl_url', models.URLField(blank=True, null=True, verbose_name='External Url with Object image')),
                ('is_potentially_hazardous_asteroid', models.BooleanField(default=False, verbose_name='Potentially Hazaroud asteroid')),
                ('orbital_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='Object data')),
            ],
            options={
                'verbose_name': 'Asteroid',
                'verbose_name_plural': 'Asteroids',
            },
        ),
        migrations.CreateModel(
            name='BookmarkAsteroid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Bookmark',
                'verbose_name_plural': 'Users Bookmarks',
            },
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_datetime', models.DateTimeField(verbose_name='Date/time when image was taken')),
                ('image', models.FileField(blank=True, null=True, storage=core.models.AttachmentStorage(), upload_to=core.models.generate_img_filename, verbose_name='Image with asteroids captured')),
                ('asteroids', models.ManyToManyField(related_name='asteroid_images', to='core.Asteroid', verbose_name='Objects, captured on image')),
            ],
            options={
                'verbose_name': 'Uploaded image',
                'verbose_name_plural': 'Uploaded images',
            },
        ),
    ]

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedimage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Users_images', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='bookmarkasteroid',
            name='asteroid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_who_bookmarked', to='core.Asteroid', verbose_name='Asteroid'),
        ),
        migrations.AddField(
            model_name='bookmarkasteroid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_asteroids', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]

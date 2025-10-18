# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0002_variation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WardrobeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, max_length=50)),
                ('size', models.CharField(blank=True, max_length=20)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
                ('times_worn', models.IntegerField(default=0)),
                ('favorite', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wardrobe_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-purchase_date'],
            },
        ),
    ]

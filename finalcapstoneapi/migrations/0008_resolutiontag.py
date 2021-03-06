# Generated by Django 3.1.4 on 2020-12-21 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finalcapstoneapi', '0007_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResolutionTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resolutiontag', to='finalcapstoneapi.resolution')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='finalcapstoneapi.tag')),
            ],
        ),
    ]

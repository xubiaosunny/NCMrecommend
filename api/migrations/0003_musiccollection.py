# Generated by Django 2.0.8 on 2019-04-15 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_historyrecord_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.IntegerField(db_index=True)),
                ('m_id', models.IntegerField(db_index=True)),
                ('m_name', models.CharField(max_length=50, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

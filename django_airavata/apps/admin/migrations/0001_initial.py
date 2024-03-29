# Generated by Django 3.2.18 on 2023-04-17 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDataArchive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('archive_name', models.CharField(max_length=255)),
                ('archive_path', models.TextField()),
                ('rolled_back', models.BooleanField(default=False)),
                ('max_modification_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDataArchiveEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_path', models.TextField()),
                ('user_data_archive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_airavata_admin.userdataarchive')),
            ],
        ),
    ]

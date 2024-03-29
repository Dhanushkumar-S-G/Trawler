# Generated by Django 4.1.4 on 2023-02-04 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_dumpdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_num', models.CharField(max_length=20, unique=True)),
                ('phonenumber', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('phonenumber_suspect_count', models.TextField(blank=True, null=True)),
                ('email_suspect_count', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('upiid', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='dumpdata',
            name='file',
            field=models.FileField(upload_to='dump_file/'),
        ),
    ]

# Generated by Django 4.0.3 on 2022-03-24 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_customerinfo_create_customerinfo_creating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageContractNft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='imagesNFT/%Y/%m/%d/')),
                ('chain', models.CharField(blank=True, max_length=100, null=True)),
                ('wallet', models.CharField(blank=True, max_length=100, null=True)),
                ('site', models.CharField(blank=True, max_length=100, null=True)),
                ('twitter', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='creating',
            field=models.TimeField(auto_now_add=True),
        ),
    ]

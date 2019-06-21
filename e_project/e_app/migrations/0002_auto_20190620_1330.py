# Generated by Django 2.2.2 on 2019-06-20 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='deleted_at',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='updated_at',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
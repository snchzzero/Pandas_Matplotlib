# Generated by Django 4.0.5 on 2022-09-20 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pnds_mtpltlb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelSort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sorts_1_Model', models.CharField(default='area', max_length=30)),
                ('ASC_DESK_1_Model', models.CharField(default='ASC', max_length=30)),
                ('sorts_2_Model', models.CharField(default='cluster', max_length=30)),
                ('ASC_DESK_2_Model', models.CharField(default='ASC', max_length=30)),
                ('sorts_3_Model', models.CharField(default='cluster_name', max_length=30)),
                ('ASC_DESK_3_Model', models.CharField(default='ASC', max_length=30)),
                ('sorts_4_Model', models.CharField(default='count', max_length=30)),
                ('ASC_DESK_4_Model', models.CharField(default='DESK', max_length=30)),
            ],
        ),
    ]

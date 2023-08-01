# Generated by Django 4.2.3 on 2023-07-21 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_cbtq_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='cbt',
            name='marks',
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cbt',
            name='studentclass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.studentclass'),
        ),
        migrations.AddField(
            model_name='cbt',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.subjects'),
        ),
    ]

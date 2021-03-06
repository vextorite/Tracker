# Generated by Django 4.0.1 on 2022-02-06 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0005_issue_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='state',
            field=models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Overdue', 'Overdue'), ('Due Now', 'Due Now'), ('Due Later', 'Due Later')], default='Open', max_length=20),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.issue')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

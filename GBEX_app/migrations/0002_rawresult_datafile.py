# Generated by Django 3.0.3 on 2020-02-25 13:25

import GBEX_app.helpers
import GBEX_bigfiles.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GBEX_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawresult',
            name='DataFile',
            field=GBEX_bigfiles.fields.ResumableFileField(blank=True, max_length=500, null=True, upload_to=GBEX_app.helpers.get_upload_path),
        ),
    ]

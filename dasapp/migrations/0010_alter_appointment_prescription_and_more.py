# Generated by Django 5.0.2 on 2024-02-19 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dasapp", "0009_appointment_prescription_appointment_remark_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="prescription",
            field=models.FileField(null=True, upload_to="pdfs/"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(
                choices=[(3, "User"), (1, "admin"), (2, "doc")],
                default=1,
                max_length=50,
            ),
        ),
    ]

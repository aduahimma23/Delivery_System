# Generated by Django 4.1 on 2024-06-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="terms_and_conditions",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="user_type",
            field=models.IntegerField(
                choices=[
                    (1, "Admin"),
                    (4, "Food Deliverer"),
                    (3, "Customer"),
                    (2, "Food Vendor"),
                    (5, "Intern Staff"),
                ],
                default=3,
            ),
        ),
    ]

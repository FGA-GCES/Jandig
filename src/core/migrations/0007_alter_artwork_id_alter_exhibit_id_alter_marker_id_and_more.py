# Generated by Django 4.1.2 on 2022-10-30 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_fake_alter_model_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artwork",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="exhibit",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="marker",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="object",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID"
            ),
        )
    ]

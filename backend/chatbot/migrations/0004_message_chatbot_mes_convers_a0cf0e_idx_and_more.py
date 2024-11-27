# Generated by Django 4.2.16 on 2024-11-26 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0003_conversation_state"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="message",
            index=models.Index(fields=["conversation"], name="chatbot_mes_convers_a0cf0e_idx"),
        ),
        migrations.AddIndex(
            model_name="message",
            index=models.Index(fields=["created_at"], name="chatbot_mes_created_2fef1d_idx"),
        ),
        migrations.AlterModelTable(
            name="conversation",
            table=None,
        ),
        migrations.AlterModelTable(
            name="message",
            table=None,
        ),
    ]

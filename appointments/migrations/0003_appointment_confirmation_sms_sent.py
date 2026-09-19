from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0002_alter_appointment_id_alter_consultationslot_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="confirmation_sms_sent",
            field=models.BooleanField(default=False),
        ),
    ]
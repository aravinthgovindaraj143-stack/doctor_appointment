# Deployment

This project is configured for a Python web host such as Render.

## Render settings

Use the included `render.yaml`, or configure a web service with:

- Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- Start command: `gunicorn doctor_appointment.wsgi:application`

Set these environment variables:

- `SECRET_KEY`: a long random production secret
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: the deployed hostname, for example `doctor-appointment.onrender.com`
- `CSRF_TRUSTED_ORIGINS`: the full HTTPS origin, for example `https://doctor-appointment.onrender.com`
- `DATABASE_URL`: the PostgreSQL connection URL
- `TWILIO_ACCOUNT_SID`: your Twilio account SID
- `TWILIO_AUTH_TOKEN`: your Twilio auth token
- `TWILIO_PHONE_NUMBER`: your Twilio phone number in E.164 format

The local SQLite database remains available when `DATABASE_URL` is empty. Production should use PostgreSQL because local SQLite storage is not persistent on most hosted services.

After deployment, create an administrator with:

```bash
python manage.py createsuperuser
```

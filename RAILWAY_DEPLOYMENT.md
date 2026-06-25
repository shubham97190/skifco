# Railway / Railpack Deployment

This project is configured for Railway using Railpack.

`railway.json` forces Railway to use the `RAILPACK` builder. `railpack.json` configures Python, static collection, WeasyPrint system packages, and the Gunicorn start command.

## Required Railway variables

Set these in Railway service variables:

```env
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=replace-with-a-secure-secret
DEBUG=False
ALLOWED_HOSTS=.railway.app,www.skifco.com,skifco.com
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://www.skifco.com,https://skifco.com
DATABASE_URL=${{ Postgres.DATABASE_URL }}
```

## Optional variables

```env
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@skifco.org
```

## What Railpack runs

Railpack installs dependencies from `requirements.txt`, installs the system packages needed by WeasyPrint, runs:

```sh
python manage.py collectstatic --noinput
```

Then starts the app with:

```sh
python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

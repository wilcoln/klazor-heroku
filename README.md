# Deploy commands

```
heroku config:set DISABLE_COLLECTSTATIC=1
heroku run python manage.py migrate
heroku run python manage.py loaddata folders.json
heroku run python manage.py createsuperuser
```
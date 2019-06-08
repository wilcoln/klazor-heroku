
# Production
## Heroku deployment
```
heroku config:set DISABLE_COLLECTSTATIC=1
heroku run python manage.py migrate
heroku run python manage.py loaddata folders.json
heroku run python manage.py createsuperuser
```

# Development
## Local installation
```bash
git clone git@github.com:wilcoln/klazor.git
cd klazor
npm install
pip install -r requirements.txt
```

## Local setup
You need to create a database and then specify it in the `settings.py` file as well as the database user credentials.
> NB: we recommend the use of **"klazor"** as the name of your database.

After that you have to run the following:
```bash
python manage.py migrate
python manage.py loaddata folders.json
python manage.py createsuperuser
```
### Local run
```bash
python manage.py runserver
```

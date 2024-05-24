# Deployment

1. Update `it_portal_poc/settings.py` with connection credentials to a MySQL database.

```python
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'database_name',   
        'USER': 'root',  
        'PASSWORD': 'database_password',  
        'HOST': '172.17.0.2',  
        'PORT': '3306',  
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }  
    }  
}  
```

2. Update `chat/config.json` with openAI API credentials.
```json
{
    "gpt_model": "gpt-3.5-turbo-0125",
    "open_ai_api": "11111111111111111111111111111111111111111"
}
```


3. Install all requirements in your virtual environment.

```shell
pip install -r requirements.py
```

1. Migrate models to database and run the webserver.

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:80
```

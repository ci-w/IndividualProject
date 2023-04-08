# Manual
Various commands and instructions for interacting with Making Projects. 

## Django Models
When you modify any models, you need to migrate these changes. 

` python manage.py makemigrations making ` 

` python manage.py migrate ` 

## Creating a Secret Key
You can use Django's functions to easily generate new secret keys.
In python shell:

` from django.core.management.utils import get_random_secret_key ` 

` print(get_random_secret_key()) `
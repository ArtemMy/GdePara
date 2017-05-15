## Novikov project

1. git clone https://github.com/ArtemMy/GdePara.git
2. cd GdePara
3. pip install virtualenv
4. virtualenv novenv
5. source novenv/bin/activate
6. pip install -r requirements.txt
7. ./manage.py makemigrations core
8. ./manage.py migrate
9. ./manage.py runserver

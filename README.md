Novikov project

git clone https://github.com/ArtemMy/GdePara.git
cd GdePara
pip install virtualenv
virtualenv novenv
source novenv/bin/activate
pip install -r requirements.txt
./manage.py makemigrations core
./manage.py migrate
./manage.py runserver

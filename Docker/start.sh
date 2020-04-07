#!/bin/bash


service ssh start

git clone git@github.com:gonzaloFSF/TFG.git /var/www/TFG
ln -s /var/www/TFG/Traza/pin/pin /bin/pin

cd /var/www/TFG/Simulador/
pip3 install -r requirements.txt
cd ./Proyecto_Simulador
python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver localhost:9999 &

cd
apachectl -DFOREGROUND




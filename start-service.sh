if [ $APP_ENV = 'dev' ]; then
    python3 main.py
else
    sh -c "nohup uwsgi /app/app.ini &" && sh -c "nginx -g 'daemon off;'"
fi
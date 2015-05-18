#Тестовое приложение для загрузки фотографий
Для развертывания:
1. `git git clone git@github.com:dolgiyspb/file-uploader.git`
2. `cd file-uploader/`
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
4. `bower install`
4. `python manage.py migrate`
4. `gunicorn image_upload.wsgi`


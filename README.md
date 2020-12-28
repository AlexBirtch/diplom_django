# Инструкция по запуску проекта!

* Создать виртуальное окружение
* Установить все зависимости командой: 
```
pip install -r requirements.txt

(файл requirements.txt находится в корневой папке проекта)
```

* Для тестового заполнения сайта выполнить следующие команды:

```buildoutcfg
python manage.py migrate
python manage.py loaddata fixtures.json
```

после чего будет доступен аккаунт admin с паролем admin
* Запустить проект комадой:
```
python manage.py runserver
```
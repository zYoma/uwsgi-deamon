# uwsgi-daemon

#### Приложение написано в качестве учебного проекта.
Демон, который по запросу на IPv4 адрес возвращает текущую погоду в городе, к которому относится IP адрес.

### Стек
- python 3.8
- flask
- pydantic
- requests
- uwsgi
- python-dotenv


### Запуск локально
Необходимо указать ключи доступа к API сервисов ipinfo.io и openweathermap.org в файле .env
``` 
IP_INFO_TOKEN=123
OPENWATHERMAP_TOKEN=456
```

Установить зависимости
``` 
pip install poetry 
poetry install
```

Можно запустить через uWSGI указав нужный порт
``` 
uwsgi --socket 0.0.0.0:6000 --protocol=http -w wsgi:app
``` 


### Запуск в systemd
Предусмотрен запуск через systemd, nginx+uwsgi. Конфигурационные файлы данных сервисов приведены в каталоге configs.


# Тестовое задание Music API

### Описание
Каталог исполнителей и их альбомов с песнями следующей структуры:
- Исполнитель
  - Название
- Альбом
  - Исполнитель
  - Год выпуска
- Песня
  - Название
  - Порядковый номер в альбоме

### Используемые технологии
- Django
- Django Rest Framework
- Docker
- Docker-compose
- PostgreSQL

### Подготовка
- Клонировать проект с помощью git clone или скачать ZIP-архив:  
``` git clone <название репозитория> ```
- Создать файл .env со следущим содержимым:
```
SECRET_KEY=<любой набор символов>
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<любой набор символов>
DB_HOST=db
DB_PORT=5432
```

### Запуск проекта
- Запустить docker-compose:   
``` docker-compose up ```
- Создать и применить миграции:  
``` docker-compose exec web python manage.py makemigrations ```              
``` docker-compose exec web python manage.py migrate ```
- Собрать статику:  
``` docker-compose exec web python manage.py collectstatic --no-input ``` 
- Создать суперпользователя Django  
``` docker-compose exec web python manage.py createsuperuser ```

#### Примеры некоторых запросов API (все возможные запросы доступны в документации к API):
Получить список исполнителей:  
``` GET /api/performers/ ```  
Создать исполнителя:    
``` POST /api/performers/ ```      
Получить конкретного исполнителя:    
``` GET /api/performers/{id}/ ```  
Внести изменения для конкретного исполнителя:  
``` PUT /api/performers/{id}/ ```  
Удалить конкретного исполнителя:  
``` DELETE /api/performers/{id}/ ```  
Получить списка альбомов:  
``` GET /api/albums/ ```  
Получить списка песен:  
``` GET /api/songs/ ```  

##### После запуска сервера будет доступна документация к API по адресу [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/).

#### Автор:
Стацюк Виталий - [https://github.com/VitaliySta](https://github.com/VitaliySta)

# BioClinic

BioClinic, клиент-серверное веб-приложение для онлайн-записи пациентов на медицинские услуги.

Приложение позволяет пациентам просматривать филиалы, медицинские услуги и врачей, создавать записи на приём и просматривать личный кабинет. Врач может просматривать расписание приёмов и отмечать завершённые посещения. Администратор управляет справочными данными через административную панель Django.

## Стек технологий

### Backend

- Python
- Django
- Django REST Framework
- Djoser
- PostgreSQL

### Frontend

- React
- JavaScript
- Bootstrap
- Redux

### Развёртывание

- Docker
- Docker Compose
- Nginx

## Основные возможности

- регистрация и авторизация пользователей;
- разграничение ролей пациента, врача и администратора;
- просмотр филиалов, услуг, категорий и врачей;
- фильтрация услуг и врачей;
- создание записи пациента на приём;
- проверка доступности врача, услуги, даты и времени;
- личный кабинет пациента;
- расписание врача;
- изменение статуса записи;
- административная панель для управления справочными данными.

## Запуск проекта через Docker Compose

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ILM0912/bio-clinic
cd bio-clinic
```

### 2. Создать файл окружения

В папке /infra необходимо создать файл .env

```bash
cp .env.exmple .env
```

Пример содержимого:

```env
SECRET_KEY=django-insecure-change-me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend
POSTGRES_DB=bio_clinic
POSTGRES_USER=bio_clinic_user
POSTGRES_PASSWORD=bio_clinic_password
DB_HOST=db
DB_PORT=5432
```

### 3. Запустить контейнеры

```bash
docker compose up -d --build
```

### 4. Создать администратора

```bash
docker compose exec backend python manage.py createsuperuser
```

После запуска приложение будет доступно по адресу:

```text
http://localhost/
```

Административная панель Django:

```text
http://localhost/admin/
```

API серверной части:

```text
http://localhost/api/
```

## Тестовые данные

Для проверки работы приложения предусмотрено заполнение тестовыми данными - филиалами, услугами и врачами.
 - Тестовые профили врачей расположены в файле backend/clinic/management/commands/doctors.py и загружаются командой seed_doctors
 - Тестовые профили врачей расположены в файле backend/clinic/fixtures/db.json

## Основные API-маршруты

| Метод | API-маршрут                          | Назначение                                   |
| ----- | ------------------------------------ | -------------------------------------------- |
| POST  | `/api/auth/users/`                   | Регистрация пользователя                     |
| POST  | `/api/auth/token/login/`             | Авторизация пользователя                     |
| POST  | `/api/auth/token/logout/`            | Выход пользователя из системы                |
| GET   | `/api/auth/users/me/`                | Получение данных текущего пользователя       |
| GET   | `/api/branches/`                     | Получение списка филиалов                    |
| GET   | `/api/groups/`                       | Получение списка категорий медицинских услуг |
| GET   | `/api/services/`                     | Получение списка медицинских услуг           |
| GET   | `/api/doctors/`                      | Получение списка врачей                      |
| GET   | `/api/doctor-services/`              | Получение связей врача, услуги и филиала     |
| POST  | `/api/appointments/`                 | Создание записи на приём                     |
| GET   | `/api/appointments/?scope=upcoming`  | Получение будущих записей пациента           |
| GET   | `/api/appointments/?scope=history`   | Получение истории записей пациента           |
| GET   | `/api/appointments/?date=YYYY-MM-DD` | Получение расписания врача на выбранную дату |
| PATCH | `/api/appointments/{id}/`            | Изменение статуса записи                     |
| GET   | `/api/appointments/busy-slots/`      | Получение занятых временных интервалов врача |


## Автор
Арсений Красоткин, ИКБО-10-23
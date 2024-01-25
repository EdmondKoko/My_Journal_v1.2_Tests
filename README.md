![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-2.2.6-red?style=for-the-badge&logo=django&logoColor=blue)
![SQLite](https://img.shields.io/badge/SQLite-grey?style=for-the-badge&logo=postgresql&logoColor=yellow)
![Pytest-django](https://img.shields.io/badge/pytest-django==3.8.0-orange?style=for-the-badge&logo=nginx&logoColor=green)

# My_Journal - социальная сеть для публикации личных дневников. 

## Описание:
### Расширение проекта My_Journal:

В проекте реализовано:
- тестирование модели приложения posts в My_Journal;
- проверка доступности страниц и названия шаблонов приложения Posts проекта My_Journal, проверка учитывает права доступа;
- проверка корректности использования html-шаблонов во view-функциях;
- проверка соответствия ожиданиям словаря context, передаваемого в шаблон при вызове;
- проверка на корректное отображение поста на главной странице сайта, на странице выбранной группы и в профайле пользователя при создании поста и указании группы, а также проверка, что пост не попал в группу, для которой не был предназначен;
- проверка создания новой записи в базе данных при отправке валидной формы со страницы создания поста, а при отправке валидной формы со страницы редактирования поста изменение поста с post_id в базе данных.

### Запуск приложения:

Клонируем проект:

```bash
git clone https://github.com/edmondkoko/My_Journal_v1.2_Tests.git
```

Переходим в папку с проектом:

```bash
cd My_Journal_v1.2_Tests.git
```

Устанавливаем виртуальное окружение:

```bash
python3 -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/bin/activate
```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

Создаем супер пользователя:

```bash
python manage.py createsuperuser
```

Запускаем проект:

```bash
python manage.py runserver
```

После чего проект будет доступен по адресу (http://127.0.0.1:8000/)

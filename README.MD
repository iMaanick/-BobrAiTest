# Документация
1. Документация api:


```
http://127.0.0.1:8000/docs/
```


2. Документация бота:

 ```
 app\README.MD
 ```

# Тесты
1. Тесты api:


```
api\tests
```


2. Документация бота:

```
app\tests
```

3. Запуск тестов:

```
pytest
```

# Запуск проекта

1. Клонируйте репозиторий:

```
git clone https://github.com/iMaanick/BobrAiTest.git
```

2. Активируйте виртуальное окружение:


3. Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Добавьте файл .env и заполните его как в примере .env.example:
```
TOKEN=your_token
DATABASE_URL=your_db_url
```
5. Для api выполните:

```
uvicorn api.main:app --reload
```

6. Для запуска телеграм бота запустите bot.py:
```
python -m app.bot
```




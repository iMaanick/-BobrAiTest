## Документация бота

### Команды:

1. /weather <город>

* Описание: Возвращает текущую погоду в указанном городе.
* Пример: /weather Москва
* Параметры:
    * <город> - название города, для которого требуется получить информацию о погоде.
* Возможные ответы:
    * Если город не указан (например, /weather): City not specified
    * Если город указан неверно (например, /weather dfgdrgt): /weather command error, city may be incorrect
    * Если аргументами команды являются несколько слов (например, /weather Moscow Tver): Invalid input format

2. /start

* Описание: Возвращает приветственное сообщение.
* Ответ: This bot was created as a test for the BobrAi company.

3. Другие команды:

* Ответ: Unknown command

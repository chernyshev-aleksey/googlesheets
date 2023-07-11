# Напоминание по работе Гугл таблицами 

### Создание сервисного аккаунта

1. [Выбрать или создать проект](https://console.cloud.google.com/welcome)
2. Перейти в APIs & Services -> Enabled APIs & services -> ENABLE APIS AND SERVICES, включить "google sheets api"
3. Перейти в APIs & Services -> Credentials -> Create credentials -> Service account
4. В настройках аккаунта получить ключ, добавить эти данные в бд
5. Добавить почту сервисного аккаунта в таблицу
6. Заполнить .env.server

### Использование

```
from src.googlesheets_api import GoogleSheet
from src.settings import config


gs = GoogleSheet(config.GOOGLESHEETS_ID).get_values_by_range('<Имя листа>!<Ячейки таблицы>')

```

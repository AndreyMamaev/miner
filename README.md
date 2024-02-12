# Игра Сапёр
### Описание
Тестовое задание для "Студия Т_Г"
### Запуск проекта
Клонировать репозиторий и перейти в него в командной строке:

```git clone https://github.com/AndreyMamaev/miner.git```

Перейти в директорию проекта:

```cd miner```

Создать /backend/.env файл (по образцу .envexample)

Создать контейнеры:

```docker-compose up -d --build```

Выполнить миграции:

```./create_migration.sh```

[Ссылка на игру](https://minesweeper-test.studiotg.ru/)

В поле URL API необходимо ввести:

```http://localhost```

Для последующих запусков проекта:

```docker-compose up -d --build```

Для остановки проекта:

```docker-compose down```

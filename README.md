# Игра Сапёр
### Описание
Тестовое задание для "Студия Т_Г"
### Запуск проекта
Клонировать репозиторий и перейти в него в командной строке:

```git clone git@github.com:AndreyMamaev/miner.git```

Создать /backend/.env файл (по образцу .envexample)

Создать контейнеры:

```docker-compose up -d --build```

Выполнить миграции:

```./create_migration.sh```

Для последующих запусков проекта:

```docker-compose up -d --build```

Для остановки проекта:

```docker-compose down```

docker-compose exec backend alembic revision --autogenerate -m "create_table"
docker-compose exec backend alembic upgrade head

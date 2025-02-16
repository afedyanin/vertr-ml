# 2025-02-09

## TODO
- выключить качалку ИСС
- реализовать качалку для Vertr базы свечей и T-инвест (раз в минуту)
- реализовать логирование в предикторе? (какая версия модели?)
- переделать генератор сигналов на работу через API
- реализовать клиента для работы с API

```shell
docker network connect vertr-platform_default infra-pgsql-1
```

# 2025-02-06

## TODO
- [x] prediction API - request & response model, controller, services
- [ ] DI and Singletone for factories, services etc  
- [ ] написать тесты на env для синтетики - проверить правильность работы енва

## Использование API (Клиент)
- [ ] блокнот с клиентом для API
- [ ] положить API в докер контейнер и использовать из Air Flow 

# 2025-02-05

- [x] написать скрипт по тренингу и сохранению модели в новую бд

## реализовать флоу в виде функции или класса

- [x] подготовить и загрузить енв актуальными данными
- [x] загрузить модель из базы
- [x] получить предсказание от модели по текущему стейту енва
- [x] сохранить/вернуть предсказание (словарь или фрейм)

# 2025-02-03

## TODO
- [x] создать gym среду по дата-фрейму
- [x] протестировать и проверить среду
- [-] создать API респонс на основе датафрейма для бенчмарк стратегий (без gym среды)

## T-Invest
https://github.com/RussianInvestments/invest-python
https://russianinvestments.github.io/invest-python/examples/
https://tinkoff.github.io/investAPI/operations/#positionsrequest

# 2025-02-02

## TODO

### Достать из БД свечи и вернуть их с предсказанием

- [x] создать новую бд vertr
- [x] создать структуру таблиц (или одну таблицу) - для T-инвест, для синтетики
- [x] прописать креды в конфиге и уметь их доставать
- [x] рассмотреть возможность ипользования SQLAlchemy
- подготовить группу репозиториев
- заинжектить репозиторий в сервис в зависимости от выбранного source в реквесте

### Уметь создавать и тестировать среду обучения

- доставать свечи и формировать DF
- подключить FeatureComposer
- создать Gym среду 
- наборы тестов для Gym среды на основе синтетических свечей

### Продумать процедуру для тренировки (обучения моделей) онлайн

- варианты использования background process?
- как отслеживать прогресс и логи для TensorBoard?
- как настраивать параметры в Optuna?


# 2025-01-31

## Start Fast API

```shell
cd app
fastapi dev main.py
```

```shell
cd ..
docker compose up
```

# 2025-01-26

## TODO

- [ ] Web API Design
- [ ] DAL (SqlAlchemy?)

## BLOBS
- 
- [Storing a BLOB in a PostgreSQL Database using Python](https://www.geeksforgeeks.org/storing-a-blob-in-a-postgresql-database-using-python/)
- https://stackoverflow.com/questions/1779701/example-using-blob-in-sqlalchemy
- [Attaching Images](https://sqlalchemy-imageattach.readthedocs.io/en/0.8.0/guide/context.html)

## SQLAlchemy

- [docs](https://docs.sqlalchemy.org/en/20/)

## Books

- [Building-Python-Web-APIs-with-FastAPI](https://github.com/PacktPublishing/Building-Python-Web-APIs-with-FastAPI)
- [Building-Python-Microservices-with-FastAPI](https://github.com/PacktPublishing/Building-Python-Microservices-with-FastAPI)
- [Building-Data-Science-Applications-with-FastAPI-Second-Edition](https://github.com/PacktPublishing/Building-Data-Science-Applications-with-FastAPI-Second-Edition)

## Fast API

 - [tutorial](https://fastapi.tiangolo.com/tutorial/)
 - [GH](https://github.com/fastapi/fastapi)

### Docker

- [fast-api-docs](https://fastapi.tiangolo.com/deployment/docker)
- [docker-compose-sample](https://github.com/docker/awesome-compose/tree/master/fastapi)
- [How to Build Fast API Application using Docker Compose](https://www.digitalocean.com/community/tutorials/create-fastapi-app-using-docker-compose)
- [python images](https://hub.docker.com/_/python)

### Modular monolith

- [booking-modular-monolith](https://github.com/meysamhadeli/booking-modular-monolith)
- [A Practical Guide to Modular Monoliths with .NET](https://chrlschn.dev/blog/2024/01/a-practical-guide-to-modular-monoliths/)
- [modular-monolith-with-ddd](https://github.com/kgrzybek/modular-monolith-with-ddd)
- [mm-articles](https://awesome-architecture.com/modular-monolith/#articles)
- [RiverBooks](https://github.com/ardalis/RiverBooks)


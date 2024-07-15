# Ассистент Сберлаб-НГУ

**Интеллектуальная система для студентов и сотрудников Сберлаб-НГУ, позволяющая автоматизировать большинство внутренних процессов в лаборатории, таких как сбор отчетов, расчет показателей, учет посещаемости, активности в дискуссиях и т.д. Система интегрируется с [__Gitlab__](), [__Kimai__](), [__BookStack__]() и [__Plane__]().**

# Начало работы

### Локально:

0. Убедитесь что у вас установлены:
* [Git](https://git-scm.com/)
* [Python3.8.10 or later](https://www.python.org/)
* [Docker](https://www.docker.com/)
* 
1. Скопировать репозиторий
```shell
git clone https://gitlab.sberlab.nsu.ru/a.tishkin/sberlab_nsu_assistant
cd sberlab_nsu_assistant
```
2. Создать виртуальную среду
```shell
python -m venv .venv
source .venv/bin/activate
```
3. Установить зависимости
```shell
pip install -r ./src/requirements.txt
```
4. Установить переменные среды
```shell
cp .env.local.exmaple .env
nano .env
```
5. Запустить базу данных
```shell
```
6. Запустить скрипт
```shell
python app/main.py
```

### Docker:
```shell
docker push andrei1121212/sberlab_assistant:amd64
```


## Контакты

Andrei - Telegram **@Lizarcon** - a.tishkin1@g.nsu.ru

Ссылка на репозиторий: https://gitlab.sberlab.nsu.ru/a.tishkin/sberlab_nsu_assistant#sberlab_nsu_assistant

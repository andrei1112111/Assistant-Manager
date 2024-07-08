# SberLab NSU Assistant

**Intelligent system for students and employees of Sberlab-NSU, which allows to automate most of the internal processes in the laboratory, such as collecting reports, calculating indicators, accounting for attendance, activity in discussions, etc. The system integrates with [__Gitlab__](), [__Kimai__](), [__BookStack__]() and [__Plane__]().**


# Getting Started

### Local:

0. Make sure you have:
* [Git](https://git-scm.com/)
* [Python3.8.10 or later](https://www.python.org/)
* [Docker](https://www.docker.com/)
* 
1. Clone this project
```shell
git clone https://gitlab.sberlab.nsu.ru/a.tishkin/sberlab_nsu_assistant
cd sberlab_nsu_assistant
```
2. Create virtual environments
```shell
python -m venv .venv
source .venv/bin/activate
```
3. Install dependencies
```shell
pip install -r ./src/requirements.txt
```
4. Set up environment variables
```shell
cp .env.local.exmaple .env
nano .env
```
5. Start database
```shell
```
6. Run application
```shell
python app/main.py
```

### Docker:
...


## Contact

Andrei - Telegram **@Lizarcon** - a.tishkin1@g.nsu.ru

Project Link: https://gitlab.sberlab.nsu.ru/a.tishkin/sberlab_nsu_assistant#sberlab_nsu_assistant


# SberLab_NSU_Assistant

**Intelligent system for students and employees of Sberlab-NSU, which allows to automate most of the internal processes in the laboratory, such as collecting reports, calculating indicators, accounting for attendance, activity in discussions, etc. The system integrates with [__Gitlab__](), [__Kimai__](), [__BookStack__]() and [__Plane__]().**
# Getting Started
This is an example of how you may set up this project locally. To get a local copy up and running follow these simple example steps:
## Installation & Usage
### You can __Run it locally__:
Make sure Python3.8.10 or later is installed and added to the PATH together with pip
```bash
git clone https://gitlab.sberlab.nsu.ru/a.tishkin/sberlab_nsu_assistant
cd sberlab_nsu_assistant
./setup.sh
```

### You can __Pull__ this project from  [__Docker Hub__](https://hub.docker.com)
```bash
...
```
And __Run__ it using:
```bash
...
```
## Change settings

### At first, you need to change the [settings.ini](settings.ini)
* Check the timezone 
```
[Time]
...
timezone = Asia/Novosibirsk
```
* Look at wakeup time 
```
[Time]
...
wakeup time = 12:39
```
* Check the Service addresses 
```
[Services hosts]
plane = http://...
kimai = http://...
gitlab = http://...
bookstack = http://...
```
* Enter your API tokens
```
[API Tokens]
plane = plane_api_...
kimai = ...
```
## Contact

Andrei - [@Lizarcon]() - a.tishkin1@g.nsu.ru

Project Link: https://gitlab.sberlab.nsu.ru/a.tishkin/sberlab_nsu_assistant#sberlab_nsu_assistant

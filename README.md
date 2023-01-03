# ismed2022Z_Nuszkiewicz_Pasierbiewicz - measuremed



## 0. Opis projektu, schemat działania i krótka instrukcja
Aplikacja została stworzona w języku Python przy użyciu frameworka Django. 

Całość systemu postanowiliśmy opakować w kontenery przy użyciu narzędzia Docker i opatrzeć plikiem docker-compose.yml, aby umożliwić uruchamianie systemu z dowolnego miejsca bez instalacji dodatkowych bibliotek, uruchamiania dodatkowych procesów czy instalowania bazy danych.

- Jest to aplikacja webowa umożliwiająca dodawanie pomiarów BMI dla pacjentów przez lekarzy. 

- Jest możliwość rejestracji użytkownika jako pacjent lub lekarz. 

- Użytkownik będący w grupie lekarzy ma dostęp do zakładki "Lekarz", w której znajduje się panel do dodawania pomiarów, natomiast pacjent ma dostęp do zakładki "Pacjent", gdzie ma możliwość odczytywania pomiarów BMI.

Aby przetestować działanie aplikacji należy ją uruchomić, proces uruchamiania przy użyciu Dockera opisany jest [2. Quick start](#quick-start).

[**INTERNET**]Postanowiliśmy wdrożyć nasze rozwiązanie na platformę chmurową Azure przy pomocy serwisu Azure Web App Service - rozwiązania serverless do wdrażania aplikacji internetowych. Aby skorzystać z aplikacji należy wpisać w przeglądarce:
```
https://measuremed.azurewebsites.net/
```


[**LOKALNIE**]Po uruchomieniu należy wpisać w przeglądarce adres: 
```
http://localhost:8000
```


## 1. Set up a project in development mode

### Python version

We used <b>Python 3.8.10</b> 

### Virtual environment
To install venv with requirements needed in this project:
```
python3 -m venv env
```

Activate a venv(in folder repo/)(venv could)
```
source env/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

Deactivate while being in a venv. Just type:
```
deactivate
```

Run start.sh script:
```
bash start.sh
```
Then there is need to set up qcluster for djangoq Message Queue and redis, but it can be done with docker-compose automatically in the next step(Quick start)


## 2. For testing purposes we created 2xpatients accounts and 1xdoctor. There are passes:
Patient:
```
username: patient
password: notifymed123
```

Doctor:
```
username: doctor
password: notifymed123
```








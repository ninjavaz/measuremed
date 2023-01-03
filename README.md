measuremed - Django App

## 0. Project description
App in which we can store BMi measures added by Doctors. There are two account types - doctor and patient.

[**GLOBALLY**] App is deployed on Azure Web App Service. Here is the link:
```
https://measuremed.azurewebsites.net/
```


[**LOCALLY**] After starting with venv etc.(as described below), just type in the browser:
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






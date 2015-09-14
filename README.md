# Raccoongang's django application template
This Django application template includes all following functional:
* Authorization using email with confirmation or social networks (Facebook, LinkedIn, Odnoklassniki, Vkontakte)
* Authorization using email or social networks
* Password recovering
* Profile editor
* Email changing
* Password changing

# Instruction
Go to you project folder
Create virtualenv for you project and activate it:
```sh
virtualenv --no-site-packages .venv
source .venv/bin/activate
```
Install Django
```sh
pip install Django
```
Create new application using this template. Dont forget to change  `<project_name>` at the end of this command
```sh
django-admin startproject --template=https://github.com/raccoongang/django_project_templates/archive/master.zip <project_name>
```
Install all libraries from requirements
```sh
cd <project_name>
pip install -r requirements.txt
```

Uncomment settings.local.py on .gitignore.

Follow this instruction for getting social network's access keys:
http://adw0rd.com/2013/2/27/django-social-auth/

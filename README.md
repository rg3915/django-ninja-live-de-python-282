# django-ninja-live-de-python-282

Tutorial de [Django Ninja](https://django-ninja.dev/) apresentado na [Live de Python](https://www.youtube.com/@Dunossauro) [282]() do [Dunossauro](https://github.com/dunossauro/live-de-python/).

Doc: https://django-ninja.dev/


## Este projeto foi feito com:

* [Python 3.12.4](https://www.python.org/)
* [Django 5.1.6](https://www.djangoproject.com/)
* [Django-Ninja 1.3.0](https://django-ninja.dev/)


## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```bash
git clone https://github.com/rg3915/django-ninja-live-de-python-282.git
cd django-ninja-live-de-python-282

python -m venv .venv
source .venv/bin/activate  # Linux
.venv\Scripts\activate  # Windows

pip install -r requirements.txt

python contrib/env_gen.py

python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""

pytest -vv  # Rodando os testes

python manage.py runserver
```

## url da doc

A doc é gerada automaticamente com Swagger.

http://localhost:8000/api/v1/docs



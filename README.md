# Chronos-backend
## celery
PS. first cd to backend folder(`cd backend`)
### create celery worker
```bash
celery -A config worker -l info
```
### create celery flower
```bash
celery -A config flower
```

### inspect task
```bash
celery -A config inspect registered
```

### call task
```bash
celery -A config call tasks.add --args='[2,2]'
```

```
Chronos-backend
├─ .editorconfig
├─ .gitignore
├─ .pre-commit-config.yaml
├─ .vscode
│  └─ settings.json
├─ DockerFile
├─ README.md
├─ backend
│  ├─ chatbot
│  │  ├─ admin.py
│  │  ├─ apis.py
│  │  ├─ apps.py
│  │  ├─ migrations
│  │  │  ├─ __init__.py
│  │  │  └─ ...
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ signals.py
│  │  ├─ tasks.py
│  │  └─ utils.py
│  └─ core
│     ├─ __init__.py
│     ├─ adapters.py
│     ├─ admin.py
│     ├─ apis.py
│     ├─ apps.py
│     ├─ authentication.py
│     ├─ context_processors.py
│     ├─ exceptions.py
│     ├─ forms.py
│     ├─ managers.py
│     ├─ migrations
│     │  ├─ __init__.py
│     │  └─ ...
│     ├─ models.py
│     ├─ schemas.py
│     ├─ tasks.py
│     ├─ tests.py
│     └─ utils.py
├─ config
│  ├─ __init__.py
│  ├─ api.py
│  ├─ asgi.py
│  ├─ auth.py
│  ├─ celery.py
│  ├─ schemas.py
│  ├─ settings
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ docker.py
│  │  └─ local.py
│  ├─ urls.py
│  └─ wsgi.py
├─ docker-compose
├─ docker-entrypoint
│  ├─ celery-entrypoint.sh
│  ├─ django-entrypoint.sh
│  └─ flower-entrypoint.sh
├─ dotenv
├─ erd-full.dot
├─ erd-full.png
├─ erd.dot
├─ erd.png
├─ manage.py
├─ poetry.lock
├─ pyproject.toml
├─ requirements.txt
└─ run_asgi.py

```

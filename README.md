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

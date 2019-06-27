```
sudo docker run -p 5050:80  -e "PGADMIN_DEFAULT_EMAIL=name@example.com" -e "PGADMIN_DEFAULT_PASSWORD=admin"  -d dpage/pgadmin4
```

environ.py

DB_ENGINE = 'django.db.backends.postgresql'
DB_NAME = 'postgres' 
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'db'
DB_PORT = 5432
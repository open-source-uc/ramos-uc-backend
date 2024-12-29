A continuación se muestra un ejemplo del contenido que debe tener tu archivo `.env`:

```ini
MONGO_DB_URI=mongodb://admin:admin@localhost/?retryWrites=true&w=majority&appName=Cluster0
MONGO_DB_NAME=test
SECRET_KEY=holaMundo
```

## Ejecución

```python
python3 main.pt
```

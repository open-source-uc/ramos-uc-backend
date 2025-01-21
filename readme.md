A continuación se muestra un ejemplo del contenido que debe tener tu archivo `.env`:

```ini
SECRET_KEY=holaMundo
POSTGRES_USER=server
POSTGRES_PASSWORD=20242023
POSTGRES_DB=ramos-uc-nuevo
POSTGRES_HOST=127.0.0.0
POSTGRES_PORT=7447
```

## Ejecución

```python
python3 src/main.py
```

## Privacidad

RamosUC no guarda los correos electrónicos de los usuarios. En su lugar, almacena un hash SHA-256 de los correos para evitar la creación de cuentas duplicadas. De este modo, se garantiza que no se pueda conocer el correo ingresado en la plataforma, minimizando el riesgo de filtraciones o de recibir correos no deseados (spam) en el futuro.

# Guía de Configuración del Proyecto

## 1. Configuración del Entorno Virtual de Python

Para garantizar un entorno aislado y controlado de dependencias, es recomendable utilizar un entorno virtual de Python. A continuación se muestran los pasos para su configuración:

1. Instala `virtualenv` (si no lo tienes instalado):
    ```bash
    pip install virtualenv
    ```

2. Crea un entorno virtual con el siguiente comando:
    ```bash
    python3 -m venv py_modules
    ```

## 2. Creación del Archivo Principal `main.py`

Una vez creado el entorno virtual, crea el archivo `main.py` que contendrá la lógica principal de la aplicación.

## 3. Activación del Entorno Virtual

Para activar el entorno virtual, usa el siguiente comando dependiendo de tu sistema operativo:

- En sistemas Unix/macOS/WSL:
    ```bash
    source ./py_modules/bin/activate
    ```


## 4. Instalación de Dependencias

Con el entorno activado, instala las dependencias necesarias para el proyecto:

```bash
pip install python-dotenv fastapi[standard] pymongo uvicorn pydantic
```

## 5 Métodos HTTP: GET, POST, PATCH y DELETE

Los métodos HTTP son una parte fundamental de la comunicación en la web. Cada uno de ellos tiene un propósito específico al interactuar con los recursos del servidor. A continuación, se describen los métodos más comunes: GET, POST, PATCH y DELETE.

## GET

- **Descripción**: Se utiliza para solicitar datos de un recurso específico en el servidor.
- **Características**:
  - Es un método **idempotente**, lo que significa que múltiples solicitudes GET no alteran el estado del servidor.
  - Los parámetros se envían a través de la URL, lo que limita la cantidad de datos que se pueden enviar.
  - Se utiliza comúnmente para obtener información, como páginas web, imágenes o datos JSON.

## POST

- **Descripción**: Se utiliza para enviar datos al servidor para crear un nuevo recurso o enviar información.
- **Características**:
  - No es idempotente; enviar la misma solicitud POST varias veces puede crear múltiples recursos.
  - Los datos se envían en el cuerpo de la solicitud, lo que permite enviar más información que en un GET.
  - Se utiliza comúnmente para enviar formularios o cargar archivos.

## PATCH

- **Descripción**: Se utiliza para aplicar modificaciones parciales a un recurso existente.
- **Características**:
  - No es idempotente en todos los casos, pero a menudo se implementa de esa manera.
  - Los datos enviados en el cuerpo de la solicitud indican solo los cambios que se deben aplicar.
  - Ideal para actualizar recursos sin necesidad de enviar toda la representación del mismo.

## DELETE

- **Descripción**: Se utiliza para eliminar un recurso específico en el servidor.
- **Características**:
  - Es un método **idempotente**; eliminar el mismo recurso varias veces tendrá el mismo efecto que hacerlo una vez.
  - Generalmente no se requiere un cuerpo en la solicitud, ya que la URI especifica qué recurso se debe eliminar.



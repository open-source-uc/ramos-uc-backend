Primero hay que usar un env de python"
pip install virtualenv
python3 -m venv py_modules


Despues crear nuestro main.py
Seleccion del ambiente

source ./py_modules/bin/activate
 pip install python-dotenv fastapi[standard] pymongo uvicorn pydantic

 importante generar el requirements.txt
 pip freeze > requirements.txt

Luego de esto a desarrollar

Crear un .env con ORIGINS=127.0.0.0
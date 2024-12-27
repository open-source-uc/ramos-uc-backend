# Información sobre Ramo

## `ramos_global.py`
Este archivo contiene el CRUD para obtener la **información general** de un ramo. Los campos disponibles son:

1. **Nombre**
2. **Sigla**
4. **Área**

# Endpoints de Calificaciones (Ratings)

## POST `/ratings`
Crear una nueva calificación para un ramo
- Requiere: ramo_id, rating (boolean), comment, user_id

## GET `/ratings/{ramo_id}`
Obtener todas las calificaciones de un ramo específico

## GET `/ratings/stats/{ramo_id}`
Obtener estadísticas de calificaciones de un ramo
- Retorna: conteo de positivos, negativos y total
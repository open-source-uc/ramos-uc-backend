# seed.py
from database.database import Career, Permission
from database.database import get_db

def seed_data():
    """Inicializa los datos por defecto en la base de datos"""
    db = next(get_db())
    try:
        # Permisos por defecto
        default_permissions = [
            'CREATE_EDIT_OWN_REVIEW',
            'SUDO'
        ]
        
        # Insertar permisos
        for permission_name in default_permissions:
            permission = Permission(name=permission_name)
            db.merge(permission)

        # Carreras por defecto
        default_careers = [
            'Actuación',
            'Administración Pública',
            'Agronomía e Ingeniería Forestal',
            'Antropología – Arqueología',
            'Arquitectura',
            'Arte',
            'Astronomía',
            'Biología',
            'Biología Marina',
            'Bioquímica',
            'Ciencia Política',
            'College Artes y Humanidades',
            'College Ciencias Naturales y Matemáticas',
            'College Ciencias Sociales',
            'Construcción Civil',
            'Derecho',
            'Diseño',
            'Enfermería',
            'Estadística',
            'Filosofía',
            'Física',
            'Fonoaudiología',
            'Geografía',
            'Historia',
            'Ingeniería',
            'Ingeniería en Recursos Naturales',
            'Ingeniería Comercial',
            'Kinesiología',
            'Letras Hispánicas',
            'Letras Inglesas',
            'Licenciatura en Ingeniería en Ciencia De Datos',
            'Licenciatura en Ingeniería en Ciencia de la Computación',
            'Licenciatura en Interpretación Musical',
            'Matemática',
            'Medicina',
            'Medicina Veterinaria',
            'Música',
            'Nutrición y Dietética',
            'Odontología',
            'Pedagogía en Educación Especial',
            'Pedagogía en Educación Física y Salud',
            'Pedagogía en Educación Media en Ciencias Naturales y Biología',
            'Pedagogía en Educación Media en Física',
            'Pedagogía en Educación Media en Matemática',
            'Pedagogía en Educación Media en Química',
            'Pedagogía en Educación Parvularia',
            'Pedagogía en Inglés',
            'Pedagogía General Básica',
            'Periodismo – Dirección Audiovisual – Publicidad',
            'Psicología',
            'Química',
            'Química y Farmacia',
            'Sociología',
            'Teología',
            'Terapia Ocupacional',
            'Trabajo Social'
        ]

        # Insertar carreras
        for career_name in default_careers:
            career = Career(name=career_name)
            db.merge(career)

        db.commit()
        print("Datos iniciales insertados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"Error al inicializar datos por defecto: {e}")
        raise e
    finally:
        db.close()

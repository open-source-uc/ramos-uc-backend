from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, create_engine, text
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, CheckConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()

class Career(Base):
    __tablename__ = 'career'
    name = Column(String(255), primary_key=True)

class UserAccount(Base):
    __tablename__ = 'useraccount'
    email_hash = Column(Text, primary_key=True)
    password = Column(String(1024))
    nickname = Column(String(100), nullable=False)
    admision_year = Column(Integer, CheckConstraint("admision_year BETWEEN EXTRACT(YEAR FROM NOW()) - 12 AND EXTRACT(YEAR FROM NOW())", name="check_admission_year"), nullable=False)
    carrer_name = Column(String(255), ForeignKey('career.name'), nullable=False)

class Permission(Base):
    __tablename__ = 'permission'
    name = Column(String(100), primary_key=True)

class Course(Base):
    __tablename__ = 'course'
    sigle = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    credits = Column(Integer)
    school = Column(String(100))
    area = Column(String(100))
    category = Column(String(100))

class Section(Base):
    __tablename__ = 'section'
    sigle = Column(String(50), ForeignKey('course.sigle'))
    number = Column(Integer, nullable=False)
    year = Column(Integer, CheckConstraint("year BETWEEN EXTRACT(YEAR FROM NOW()) - 5 AND EXTRACT(YEAR FROM NOW())", name="check_year"))
    semester = Column(Integer, CheckConstraint("semester IN (1, 2, 3)", name="check_semester"))
    format = Column(String(50))
    is_english = Column(Boolean)
    is_removable = Column(Boolean)
    is_special = Column(Boolean)

    __table_args__ = (
        PrimaryKeyConstraint('sigle', 'number', 'year', 'semester'),
    )

class Quota(Base):
    __tablename__ = 'quota'
    section_sigle = Column(String(50))
    section_number = Column(Integer)
    section_year = Column(Integer)
    section_semester = Column(Integer)
    type = Column(String(200))
    count = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('section_sigle', 'section_number', 'section_year', 'section_semester', 'type'),
        ForeignKeyConstraint(
            ['section_sigle', 'section_number', 'section_year', 'section_semester'],
            ['section.sigle', 'section.number', 'section.year', 'section.semester']
        )
    )

class Teacher(Base):
    __tablename__ = 'teacher'
    name = Column(String(100), primary_key=True)

class Schedule(Base):
    __tablename__ = 'schedule'
    day_block = Column(String(2))
    type = Column(String(50))
    place = Column(String(50))
    campus = Column(String(50), CheckConstraint("campus IN ('Campus Externo', 'Casa Central', 'Lo Contador', 'Oriente', 'San Joaquín', 'Villarrica')", name="check_campus"))

    __table_args__ = (
        PrimaryKeyConstraint('day_block', 'place', 'campus'),
    )

class SectionTeacher(Base):
    __tablename__ = 'sectionteacher'
    section_sigle = Column(String(50))
    section_number = Column(Integer)
    year = Column(Integer)
    semester = Column(Integer)
    teacher_name = Column(String(100), ForeignKey('teacher.name'))

    __table_args__ = (
        PrimaryKeyConstraint('section_sigle', 'section_number', 'year', 'semester', 'teacher_name'),
        ForeignKeyConstraint(
            ['section_sigle', 'section_number', 'year', 'semester'],
            ['section.sigle', 'section.number', 'section.year', 'section.semester']
        )
    )

class SectionSchedule(Base):
    __tablename__ = 'sectionschedule'
    section_sigle = Column(String(50))
    section_number = Column(Integer)
    year = Column(Integer)
    semester = Column(Integer)
    day_block = Column(String(2))
    place = Column(String(50))
    campus = Column(String(50))

    __table_args__ = (
        PrimaryKeyConstraint('section_sigle', 'section_number', 'year', 'semester', 'day_block'),
        ForeignKeyConstraint(
            ['section_sigle', 'section_number', 'year', 'semester'],
            ['section.sigle', 'section.number', 'section.year', 'section.semester']
        ),
        ForeignKeyConstraint(
            ['day_block', 'place', 'campus'],
            ['schedule.day_block', 'schedule.place', 'schedule.campus']
        )
    )

class UserPermission(Base):
    __tablename__ = 'userpermission'
    email_hash = Column(Text, ForeignKey('useraccount.email_hash'))
    permission_name = Column(String(100), ForeignKey('permission.name'))

    __table_args__ = (
        PrimaryKeyConstraint('email_hash', 'permission_name'),
    )

class Review(Base):
    __tablename__ = 'review'
    section_sigle = Column(String(50))
    section_number = Column(Integer)
    year = Column(Integer)
    semester = Column(Integer)
    email_hash = Column(Text, ForeignKey('useraccount.email_hash'))
    liked = Column(Boolean)
    comment = Column(Text)
    estimated_credits = Column(Integer)
    status = Column(String(20), CheckConstraint("status IN ('visible', 'hidden')", name="check_status"))

    __table_args__ = (
        PrimaryKeyConstraint('section_sigle', 'section_number', 'year', 'semester', 'email_hash'),
        ForeignKeyConstraint(
            ['section_sigle', 'section_number', 'year', 'semester'],
            ['section.sigle', 'section.number', 'section.year', 'section.semester']
        )
    )

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Función para obtener una sesión
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def execute_script_sql(archivo_sql):

    with engine.connect() as connection:
        with open(archivo_sql, 'r') as file:
            script_sql = file.read()
            connection.execute(text(script_sql))
            connection.commit()
            print(f"El script '{archivo_sql}' se ha ejecutado correctamente.")
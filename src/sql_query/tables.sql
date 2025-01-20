CREATE TABLE IF NOT EXISTS Career (
    name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS UserAccount (
    email_hash TEXT PRIMARY KEY,
    password VARCHAR(255),
    nickname VARCHAR(100) NOT NULL,
    admision_year INT CHECK (admision_year BETWEEN EXTRACT(YEAR FROM NOW()) - 12 AND EXTRACT(YEAR FROM NOW())),
    carrer_name VARCHAR(255),
    FOREIGN KEY (carrer_name) REFERENCES Career(name)
);

CREATE TABLE IF NOT EXISTS Permission (
    name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Course (
    sigle VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    credits INT,
    school VARCHAR(100),
    area VARCHAR(100),
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Section (
    sigle VARCHAR(50),
    number INT NOT NULL,
    year INT CHECK (year BETWEEN EXTRACT(YEAR FROM NOW()) - 5 AND EXTRACT(YEAR FROM NOW())),
    semester INT CHECK (semester IN (1, 2, 3)),
    format VARCHAR(50),
    is_english BOOLEAN,
    is_removable BOOLEAN,
    is_special BOOLEAN,
    PRIMARY KEY (sigle, number, year, semester),
    FOREIGN KEY (sigle) REFERENCES Course(sigle)
);

CREATE TABLE IF NOT EXISTS Quota (
    section_sigle VARCHAR(50),
    section_number INT,
    section_year INT,
    section_semester INT,
    type VARCHAR(200),
    count INT,
    PRIMARY KEY (section_sigle, section_number, section_year, section_semester, type),
    FOREIGN KEY (section_sigle, section_number, section_year, section_semester) 
        REFERENCES Section(sigle, number, year, semester)
);

CREATE TABLE IF NOT EXISTS Teacher (
    name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Schedule (
    day_block CHAR(2),
    type VARCHAR(50),
    place VARCHAR(50),
    campus VARCHAR(50) CHECK (campus IN ('Campus Externo', 'Casa Central', 'Lo Contador', 'Oriente', 'San Joaquín', 'Villarrica')),
    PRIMARY KEY (day_block, place, campus)
);

-- Relaciones

CREATE TABLE IF NOT EXISTS SectionTeacher (
    section_sigle VARCHAR(50),
    section_number INT,
    year INT,
    semester INT,
    teacher_name VARCHAR(100),
    PRIMARY KEY (section_sigle, section_number, year, semester, teacher_name),
    FOREIGN KEY (section_sigle, section_number, year, semester) 
        REFERENCES Section(sigle, number, year, semester),
    FOREIGN KEY (teacher_name) REFERENCES Teacher(name)
);

CREATE TABLE IF NOT EXISTS SectionSchedule (
    section_sigle VARCHAR(50),
    section_number INT,
    year INT,
    semester INT,
    day_block CHAR(2),
    place VARCHAR(50),
    campus VARCHAR(50),
    PRIMARY KEY (section_sigle, section_number, year, semester, day_block),
    FOREIGN KEY (section_sigle, section_number, year, semester) 
        REFERENCES Section(sigle, number, year, semester),
    FOREIGN KEY (day_block, place, campus) 
        REFERENCES Schedule(day_block, place, campus)
);

CREATE TABLE IF NOT EXISTS UserPermission (
    email_hash TEXT,
    permission_name VARCHAR(100),
    PRIMARY KEY (email_hash, permission_name),
    FOREIGN KEY (email_hash) REFERENCES UserAccount(email_hash),
    FOREIGN KEY (permission_name) REFERENCES Permission(name)
);

CREATE TABLE IF NOT EXISTS Review (
    section_sigle VARCHAR(50),
    section_number INT,
    year INT,
    semester INT,
    email_hash TEXT,
    liked BOOLEAN,
    comment TEXT,
    estimated_credits INT,
    status VARCHAR(20) CHECK (status IN ('visible', 'hidden')),
    PRIMARY KEY (section_sigle, section_number, year, semester, email_hash),
    FOREIGN KEY (section_sigle, section_number, year, semester) REFERENCES Section(sigle, number, year, semester),
    FOREIGN KEY (email_hash) REFERENCES UserAccount(email_hash)
);

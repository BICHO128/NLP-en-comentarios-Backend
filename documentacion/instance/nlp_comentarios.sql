# database nlp_comentarios


create database nlp_comentarios;

use nlp_comentarios;

-- Renombrar las tablas
RENAME TABLE usuarios to users;
RENAME TABLE roles_usuarios TO roles;

-- Renombrar las columnas de la tabla usuarios
ALTER TABLE users
    CHANGE nombre_usuario username VARCHAR(255),
    CHANGE fecha_creacion created_at DATETIME,
    CHANGE nombres first_name VARCHAR(255),
    CHANGE apellidos last_name VARCHAR(255),
    CHANGE es_admin is_admin BOOLEAN,
    CHANGE activo active BOOLEAN;

-- Renombrar las columnas de la tabla roles_usuarios
ALTER TABLE roles
    CHANGE rol name varchar (80),
    CHANGE usuario_id user_id INT;


select * from comentario;
select * from usuarios;
select * from docente;
select * from evaluacion;
select * from roles;
select * from users;
select * from curso;

select * from evaluacion where id = 3;
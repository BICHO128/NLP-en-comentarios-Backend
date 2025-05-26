# database nlp_comentarios
select * from roles;
select * from comentario;
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
    
-- Agregar la columna 'user_id' como clave foránea en la tabla 'users'
ALTER TABLE users
ADD COLUMN user_id INT,
ADD CONSTRAINT fk_user_role
FOREIGN KEY (user_id)
REFERENCES roles(id);
 
create table roles (
id int primary key,
name varchar (80),
user_id int
);   

drop table roles;

alter table users
drop column is_admin;

USE nlp_comentarios;

ALTER TABLE users
  ADD COLUMN role_id INT AFTER active;

ALTER TABLE users
  ADD CONSTRAINT fk_users_roles
    FOREIGN KEY (role_id) REFERENCES roles(id);


-- Creamos los roles base
INSERT INTO roles (name) VALUES 
  ('estudiante'),
  ('docente'),
  ('admin');
  
USE `nlp_comentarios_actual`;

select * from evaluaciones;
select * from docentes;
select * from docente_curso;
select * from estudiantes;
select * from users;
select * from roles;
select * from cursos;
select * from criterios;
select * from calificaciones;
select * from comentarios;

select * from users;
select * from cursos;
select * from docentes;
select * from docente_curso;

select * from cursos where id in (1,2,3, 4, 5,6,7);

select * from evaluaciones where docente_id = 3;
select * from comentarios where fecha = "%2025-05-09";
select count(*) from evaluacion;
select docente_id, count(*) from evaluacion where docente_id = 5 group by docente_id;

select id, email, password from users where email = 'diana.garzon.m@uniautonoma.edu.co';

select * from users where is_admin = 1;

select * from users where email = 'admin@uniautonoma.edu.co';

select * from docente
union 
select * from curso ;

# para realizar una copia de seguridad a la DB
#mysqldump -u root -p nlp_comentarios > restore_nlp_comentarios.sql

# consulta para traer el texto y el sentimiento
SELECT id,texto, sentimiento FROM comentarios;

select count(sentimiento) from comentarios where sentimiento = "positivo";
select count(sentimiento) from comentarios where sentimiento = "neutral";
select count(sentimiento) from comentarios where sentimiento = "negativo";



-- Si existiera alguna tabla “roles” o “users” duplicada, asegúrate de no borrar las de tu modelo nuevo.

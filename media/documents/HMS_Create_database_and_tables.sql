-- CREATE DATABASE hospital_db;
-- USE hospital_db;

-- CREATE TABLE appointments (
-- 	id INT auto_increment PRIMARY KEY,
--     patient_id int,
--     doctor_id int,
--     appointment_date date,
--     email varchar(255),
--     phone varchar(20),
--     status ENUM('confirmed', 'pending', 'canceled'),
--     reminder_sent BOOLEAN DEFAULT FALSE
-- );

-- CREATE TABLE users (
-- 	id int auto_increment primary key,
--     username varchar(100) unique not null,
--     password varchar(255) not null,
--     email varchar(255) unique not null, 
--     phone varchar(20),
--     role enum('staff', 'patient') not null,
--     created_at timestamp default current_timestamp,
--     updated_at timestamp default current_timestamp on update current_timestamp
-- );

-- CREATE TABLE patients (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   user_id INT,
--   first_name VARCHAR(100) NOT NULL,
--   last_name VARCHAR(100) NOT NULL,
--   date_of_birth DATE,
--   gender ENUM('male', 'female'),
--   address VARCHAR(255),
--   phone VARCHAR(20),
--   email VARCHAR(255) UNIQUE,
--   insurance_number VARCHAR(100),
--   FOREIGN KEY (user_id) REFERENCES users(id)
-- );

-- CREATE TABLE doctors (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   user_id INT,
--   first_name VARCHAR(100) NOT NULL,
--   last_name VARCHAR(100) NOT NULL,
--   specialty VARCHAR(100),
--   phone VARCHAR(20),
--   email VARCHAR(255) UNIQUE,
--   office_address VARCHAR(255),
--   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--   FOREIGN KEY (user_id) REFERENCES users(id)
-- );
-- USE hospital_db;

-- ALTER TABLE appointments
-- ADD COLUMN appointment_time TIME NOT NULL;

-- ALTER TABLE users MODIFY COLUMN role VARCHAR(20);


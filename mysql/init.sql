CREATE DATABASE IF NOT EXISTS eda_archives;

USE eda_archives;

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    secret VARCHAR(512),
    date VARCHAR(50),
    location VARCHAR(100),
    pdf_path VARCHAR(1024),
    image_path VARCHAR(1024),
    status VARCHAR(50),
    email VARCHAR(50),
    name VARCHAR(100)
);

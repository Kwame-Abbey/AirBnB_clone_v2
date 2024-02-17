-- Prepares a MySQL server for the project

-- Create a database named 'hbnb_dev_db'
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Creates new user 'hbnb_dev'
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the database 'hbnb_dev_db' to 'hbnb_dev'
GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- hbnb_dev should have SELECT privilege on the database performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

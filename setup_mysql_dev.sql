-- prepares a MySQL server
-- should have all privileges
CREATE DATABASE IF NOT EXISTS lib_dev_db;
CREATE USER IF NOT EXISTS 'lib_dev'@'localhost' IDENTIFIED BY 'lib_dev_pwd';
GRANT ALL PRIVILEGES ON lib_dev_db.* TO 'lib_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'lib_dev'@'localhost';
FLUSH PRIVILEGES;

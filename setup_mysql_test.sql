-- prepsres a MySQL server to test
-- grants all privileges
-- grant select on performance schema
CREATE DATABASE IF NOT EXISTS lib_test_db;
CREATE USER IF NOT EXISTS 'lib_test'@'localhost' IDENTIFIED BY 'lib_test_pwd';
GRANT ALL PRIVILEGES ON lib_test_db.* TO 'lib_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'lib_test'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'tp_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON mundial2026.* TO 'tp_user'@'localhost';
FLUSH PRIVILEGES;
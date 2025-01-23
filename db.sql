DROP DATABASE IF EXISTS pwned_password; CREATE DATABASE pwned_password;use pwned_password;
GRANT ALL PRIVILEGES ON pwned_password TO 'pwned'@'localhost' IDENTIFIED BY 'pWnedTESTOK' WITH GRANT OPTION;

CREATE TABLE IF NOT EXISTS password_check_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password_hash VARCHAR(40) NOT NULL,
    breach_count INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

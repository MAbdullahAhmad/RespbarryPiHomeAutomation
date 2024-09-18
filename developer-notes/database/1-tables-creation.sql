-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL
);

-- Create the devices table
CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200)
);

-- Create the device_mode_options table
CREATE TABLE device_mode_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL,
    label VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);

-- Create the device_status table
CREATE TABLE device_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL,
    mode_id INT NOT NULL,
    last_changed DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_changed_by INT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    FOREIGN KEY (mode_id) REFERENCES device_mode_options(id),
    FOREIGN KEY (last_changed_by) REFERENCES users(id)
);

-- Create the mode_change_history table
CREATE TABLE mode_change_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL,
    mode_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    changed_by INT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    FOREIGN KEY (mode_id) REFERENCES device_mode_options(id),
    FOREIGN KEY (changed_by) REFERENCES users(id)
);

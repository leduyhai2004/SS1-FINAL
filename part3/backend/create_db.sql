CREATE DATABASE todo_app;

USE todo_app;

CREATE TABLE todo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    status ENUM('Doing', 'Done') NOT NULL
);

INSERT INTO todo (description, status) VALUES ('SS1 Assignment 1', 'Done');
INSERT INTO todo (description, status) VALUES ('SS1 Assignment 2', 'Doing');
INSERT INTO todo (description, status) VALUES ('SS1 Final', 'Doing');
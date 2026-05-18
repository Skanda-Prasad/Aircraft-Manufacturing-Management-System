CREATE DATABASE dbms_project;

USE dbms_project;


CREATE TABLE aircraft_model (
  model_id INT NOT NULL AUTO_INCREMENT,
  model_name VARCHAR(255) NOT NULL,
  manufacturer VARCHAR(255) NOT NULL,
  capacity INT,
  max_range INT,
  mtow INT,
  PRIMARY KEY (model_id)
);

CREATE TABLE aircraft_component (
  component_id INT NOT NULL AUTO_INCREMENT,
  component_name VARCHAR(255) NOT NULL,
  manufacturer VARCHAR(255) NOT NULL,
  weight INT,
  cost INT,
  supplier_id INT,
  used_in_model INT
  PRIMARY KEY (component_id),
  FOREIGN KEY (supplier_id) REFERENCES supplier (supplier_id),
  FOREIGN KEY (used_in_model) REFERENCES aircraft_model (model_id)
);

CREATE TABLE supplier (
  supplier_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  contact_info VARCHAR(255) NOT NULL,
  PRIMARY KEY (supplier_id)
);

CREATE TABLE employee (
  employee_id INT NOT NULL AUTO_INCREMENT,
  fullname VARCHAR(255) NOT NULL,
  position VARCHAR(255) NOT NULL,
  contact_info VARCHAR(255) NOT NULL,
  PRIMARY KEY (employee_id)
);


CREATE TABLE aircraft_order (
  order_id INT NOT NULL AUTO_INCREMENT,
  customer_id INT,
  date_placed DATE,
  order_status VARCHAR(255),
  total_cost INT,
  PRIMARY KEY (order_id),
  FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);

CREATE TABLE completed_orders (
  order_id INT NOT NULL AUTO_INCREMENT,
  customer_id INT,
  date_placed DATE,
  order_status VARCHAR(255),
  total_cost INT,
  PRIMARY KEY (order_id),
  FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);

CREATE TABLE customer (
  customer_id INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(255) NOT NULL,
  contact_info VARCHAR(255) NOT NULL,
  PRIMARY KEY (customer_id)
);

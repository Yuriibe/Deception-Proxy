CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

INSERT INTO clients (name, email, phone) VALUES
('Alice Wonderland', 'alice@example.com', '123-456-7890'),
('Bob Builder', 'bob@example.com', '987-654-3210');
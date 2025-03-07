CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(15, 2),
    hire_date DATE
);

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    employee_id INT,
    transaction_date DATE,
    amount DECIMAL(15, 2),
    transaction_type VARCHAR(50),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE company_assets (
    asset_id INT PRIMARY KEY,
    asset_name VARCHAR(100),
    purchase_date DATE,
    asset_value DECIMAL(15, 2)
);

INSERT INTO employees (employee_id, first_name, last_name, department, salary, hire_date)
VALUES
(1, 'Daniel', 'Fitzgerald', 'Engineering', 105000.00, '2019-11-12'),
(2, 'Olivia', 'Sullivan', 'Marketing', 95000.00, '2020-06-08'),
(3, 'James', 'Thompson', 'Sales', 86000.00, '2018-01-22'),
(4, 'Lily', 'Cameron', 'Engineering', 102000.00, '2021-02-15'),
(5, 'Nathan', 'Rivers', 'HR', 78000.00, '2021-03-25'),
(6, 'Charlotte', 'Morgan', 'Finance', 115000.00, '2017-07-10'),
(7, 'Benjamin', 'Lloyd', 'Marketing', 90000.00, '2018-04-03'),
(8, 'Ella', 'Reed', 'Engineering', 99000.00, '2019-08-20');

INSERT INTO transactions (transaction_id, employee_id, transaction_date, amount, transaction_type)
VALUES
(1, 1, '2024-03-01', 1500.00, 'Salary'),
(2, 2, '2024-03-01', 2500.00, 'Salary'),
(3, 3, '2024-03-01', 1800.00, 'Salary'),
(4, 4, '2024-03-01', 1800.00, 'Salary'),
(5, 5, '2024-03-01', 1500.00, 'Salary'),
(6, 6, '2024-03-01', 2300.00, 'Salary'),
(7, 7, '2024-03-01', 2000.00, 'Salary'),
(8, 8, '2024-03-01', 1750.00, 'Salary');

INSERT INTO company_assets (asset_id, asset_name, purchase_date, asset_value)
VALUES
(1, 'Office Building - Downtown', '2015-06-01', 5000000.00),
(2, 'Company Fleet - Sedan', '2020-03-15', 350000.00),
(3, 'Server Cluster', '2022-11-25', 800000.00),
(4, 'Employee Workstations', '2021-01-18', 150000.00),
(5, 'Headquarters Renovation', '2023-05-10', 1200000.00);

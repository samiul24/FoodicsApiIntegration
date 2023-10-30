drop table Customers;
CREATE TABLE Customers (
    house_account_balance NUMBER,
    loyalty_balance NUMBER,
    customer_id VARCHAR2(36),
    name VARCHAR2(255),
    dial_code VARCHAR2(20),
    phone VARCHAR2(20),
    email VARCHAR2(255),
    gender VARCHAR2(10),
    birth_date DATE,
    is_blacklisted VARCHAR2(10),
    is_house_account_enabled VARCHAR2(10),
    house_account_limit NUMBER,
    is_loyalty_enabled VARCHAR2(10),
    order_count NUMBER,
    last_order_at TIMESTAMP,
    notes VARCHAR2(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

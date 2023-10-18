drop table House_Account_Transactions;
CREATE TABLE House_Account_Transactions(
    house_account_transaction_id VARCHAR2(50),
    amount NUMBER(10, 2),
    old_balance NUMBER(10, 2),
    new_balance NUMBER(10, 2),
    notes VARCHAR2(255),
    user_id VARCHAR2(50),
    customer_id VARCHAR2(50),
    order_id VARCHAR2(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

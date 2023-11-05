DROP TABLE House_Account_Transactions;
CREATE TABLE House_Account_Transactions (
    house_account_transaction_id VARCHAR2(36),
    amount NUMBER,
    old_balance NUMBER,
    new_balance NUMBER,
    notes VARCHAR2(255),
    user_id VARCHAR2(36),
    customer_id VARCHAR2(36),
    order_id VARCHAR2(36),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    sys_date date default sysdate
);

drop table Gift_Card_Transactions;
CREATE TABLE Gift_Card_Transactions (
    gift_card_transaction_id VARCHAR2(36),
    amount NUMBER,
    old_balance NUMBER,
    new_balance NUMBER,
    gift_card_id VARCHAR2(36),
    order_id VARCHAR2(36),
    created_at TIMESTAMP,
    sys_date date default sysdate
);
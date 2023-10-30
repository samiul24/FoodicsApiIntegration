drop table Payment_Methods;
CREATE TABLE Payment_Methods (
    Payment_Method_id VARCHAR2(36),
    name VARCHAR2(255),
    code VARCHAR2(50),
    name_localized VARCHAR2(255), 
    type NUMBER(1),
    auto_open_drawer VARCHAR2(10), 
    is_active VARCHAR2(10), 
    created_at TIMESTAMP, 
    updated_at TIMESTAMP, 
    deleted_at TIMESTAMP,
    sys_date date default sysdate
);

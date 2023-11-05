DROP TABLE Groups;
CREATE TABLE Groups (
    group_id VARCHAR2(36),
    name VARCHAR2(255),
    name_localized VARCHAR2(255),
    items_index VARCHAR2(2555),
    product_id VARCHAR2(36),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    sys_date date default sysdate
);
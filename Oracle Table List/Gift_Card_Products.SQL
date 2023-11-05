drop table Gift_Card_Products;
CREATE TABLE Gift_Card_Products (
    gift_card_id VARCHAR2(36),
    name VARCHAR2(255),
    name_localized VARCHAR2(255),
    sku VARCHAR2(255),
    barcode VARCHAR2(255),
    pricing_method NUMBER,
    price NUMBER,
    is_active VARCHAR2(10),
    category_id VARCHAR2(36),
    category_name VARCHAR2(36),
    category_name_localized VARCHAR2(36),
    category_reference VARCHAR2(36),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    sys_date date default sysdate
);
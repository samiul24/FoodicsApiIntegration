drop table Discounts;
CREATE TABLE Discounts (
    discount_id VARCHAR2(36),
    name VARCHAR2(50),
    name_localized VARCHAR2(50),
    qualification NUMBER(1),
    amount NUMBER(10, 2),
    minimum_product_price NUMBER(10, 2),
    minimum_order_price NUMBER(10, 2),
    maximum_amount NUMBER(10, 2),
    is_percentage VARCHAR2(10),
    is_taxable VARCHAR2(10),
    reference VARCHAR2(10),
    order_types VARCHAR2(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    product_id VARCHAR2(36),
    product_tag_id VARCHAR2(36),
    category_id VARCHAR2(36),
    combo_id VARCHAR2(36),
    branch_id VARCHAR2(36),
    branch_name VARCHAR2(50)
);
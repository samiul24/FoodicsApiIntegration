drop table Categories;
CREATE TABLE Categories (         
category_id VARCHAR2(36),
name VARCHAR2(255),
name_localized VARCHAR2(255),
reference VARCHAR2(255),
created_at TIMESTAMP,
updated_at TIMESTAMP,
deleted_at TIMESTAMP, 
sys_date date default sysdate
)
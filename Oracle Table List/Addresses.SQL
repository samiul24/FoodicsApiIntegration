drop table Addresses;
CREATE TABLE Addresses (
    address_id VARCHAR2(36),
    city_id VARCHAR2(36),
    name VARCHAR2(255),
    details VARCHAR2(255),
    description VARCHAR2(255),
    latitude VARCHAR2(50),
    longitude VARCHAR2(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP, 
    customer_id VARCHAR2(36),
    delivery_zone_id VARCHAR2(36),
    sys_date date default sysdate
);

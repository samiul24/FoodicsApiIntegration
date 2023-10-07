CREATE TABLE Inventory_Categories (
    id VARCHAR2(36) PRIMARY KEY,
    name VARCHAR2(255),
    name_localized VARCHAR2(255),
    reference VARCHAR2(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

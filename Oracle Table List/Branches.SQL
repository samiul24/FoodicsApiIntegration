drop table Branches;
CREATE TABLE Branches (
    branch_id VARCHAR2(36),
    name VARCHAR2(255),
    name_localized VARCHAR2(255),
    reference VARCHAR2(50),
    type VARCHAR2(10),
    latitude VARCHAR2(50),
    longitude VARCHAR2(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP, 
    phone VARCHAR2(36),
    address VARCHAR2(36),
    sys_date date default sysdate
);

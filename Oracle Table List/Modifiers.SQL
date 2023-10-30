drop table Modifiers;
CREATE TABLE Modifiers (
    modifier_id VARCHAR2(36),
    name VARCHAR2(255),
    name_localized VARCHAR2(255),
    is_ready VARCHAR2(10),
    reference VARCHAR2(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    sys_date date default sysdate
);
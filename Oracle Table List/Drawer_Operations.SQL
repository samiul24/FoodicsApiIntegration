drop table Drawer_Operations;
CREATE TABLE Drawer_Operations (
    drawer_operation_id VARCHAR2(36),
    type NUMBER,
    amount NUMBER,
    recorded_at TIMESTAMP,
    notes VARCHAR2(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    sys_date date default sysdate
);
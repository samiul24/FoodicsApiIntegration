drop table Charges;
CREATE TABLE Charges (  
charge_id VARCHAR2(36),
name VARCHAR2(255),
name_localized VARCHAR2(255),
type VARCHAR2(10),
is_auto_applied VARCHAR2(10),
order_types VARCHAR2(10),
value number,
is_open_charge VARCHAR2(10),
is_calculated_using_subtotal VARCHAR2(10),
associate_to_all_branches VARCHAR2(10),
created_at TIMESTAMP, 
updated_at TIMESTAMP, 
deleted_at TIMESTAMP,
sys_date date default sysdate
)
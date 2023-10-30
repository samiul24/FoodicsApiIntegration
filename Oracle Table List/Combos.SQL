drop table Combos;
CREATE TABLE Combos (
combo_id VARCHAR2(36)
,sku VARCHAR2(36)
,barcode VARCHAR2(255)
,name VARCHAR2(36)
,name_localized VARCHAR2(36)
,description VARCHAR2(255)
,description_localized VARCHAR2(255)
,is_active VARCHAR2(10)
,is_ready VARCHAR2(10)
,created_at TIMESTAMP
,updated_at TIMESTAMP
,deleted_at TIMESTAMP
,sys_date date default sysdate
)
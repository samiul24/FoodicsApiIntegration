drop table Coupons;
CREATE TABLE Coupons (
 coupon_id VARCHAR2(36)
,name VARCHAR2(255)
,code VARCHAR2(36)
,maximum_uses VARCHAR2(36)
,is_active VARCHAR2(36)
,from_date TIMESTAMP
,to_date TIMESTAMP
,from_time VARCHAR2(36)
,to_time VARCHAR2(36)
,is_sat VARCHAR2(36)
,is_sun VARCHAR2(36)
,is_mon VARCHAR2(36)
,is_tue VARCHAR2(36)
,is_wed VARCHAR2(36)
,is_thu VARCHAR2(36)
,is_fri VARCHAR2(36)
,discount_id VARCHAR2(36)
,created_at TIMESTAMP
,updated_at TIMESTAMP
,deleted_at TIMESTAMP
,sys_date date default sysdate
)
drop table Orders;
CREATE TABLE Orders (
    order_id VARCHAR2(36),
    promotion_id VARCHAR2(36),
    discount_type VARCHAR2(10),
    reference VARCHAR2(36),
    type VARCHAR2(10),
    source VARCHAR2(10),
    status VARCHAR2(10),
    delivery_status VARCHAR2(10),
    guests VARCHAR2(10),
    kitchen_notes VARCHAR2(500),
    customer_notes VARCHAR2(500),
    business_date DATE,
    subtotal_price NUMBER,
    discount_amount NUMBER,
    rounding_amount NUMBER,
    total_price NUMBER,
    tax_exclusive_discount_amount NUMBER,
    delay_in_seconds NUMBER,
    opened_at TIMESTAMP,
    accepted_at TIMESTAMP,
    due_at TIMESTAMP,
    driver_assigned_at TIMESTAMP,
    dispatched_at TIMESTAMP,
    driver_collected_at TIMESTAMP,
    delivered_at TIMESTAMP,
    closed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    check_number VARCHAR2(36),
    branch_id VARCHAR2(36),
    branch_name VARCHAR2(36),
    customer_id VARCHAR2(36),
    customer_name VARCHAR2(36),
    product_id VARCHAR2(36),
    product_discount_type VARCHAR2(10),
    product_quantity NUMBER,
    product_returned_quantity NUMBER,
    product_unit_price NUMBER,
    product_discount_amount NUMBER,
    product_total_price NUMBER,
    product_total_cost NUMBER,
    product_tax_exclusive_discount_amount NUMBER,
    product_tax_exclusive_unit_price NUMBER,
    product_tax_exclusive_total_price NUMBER,
    payment_id VARCHAR2(36),
    payment_amount NUMBER,
    payment_tendered NUMBER,
    payment_tips NUMBER,
    payment_method_id VARCHAR2(36),
    payment_method_name VARCHAR2(36),
    payment_method_type VARCHAR2(5),
    combos_id VARCHAR2(36),
    combos_discount_type VARCHAR2(10),
    combos_discount_amount NUMBER,
    combos_quantity NUMBER,
    charges_charge_id VARCHAR2(36),
    charges_charge_name VARCHAR2(36),
    charges_tax_id VARCHAR2(36),
    charges_tax_name VARCHAR2(36),
    sys_date date default sysdate
    );

CREATE TABLE people (
    customer_id varchar(255),
    gender varchar(5),
    name_prefix varchar(10),
    name_first varchar(255),
    name_last varchar(255),
    email varchar(255),
    employment varchar(255),
    address varchar(255),
    city varchar(255),
    county varchar(255),
    state varchar(255),
    postal_code varchar(255),
    birth_dt date,
    job_type varchar(255),
    account_type varchar(255),
    phone_number varchar(255),
    ssn varchar(255),
    allergies varchar(255),
    blood_type varchar(10),
    last_ipaddress varchar(100)
    )

CREATE TABLE transactions (
    customer_id varchar(255),
    orderid varchar(255),
    purchasedatetime varchar(255),
    transactiontotal decimal,
    numberofitems int,
    productcode varchar(255),
    productcategory varchar(255),
    cc_number varchar(30)
    )

CREATE TABLE social (
    social_customer_id varchar(255),
    social_email varchar(255),
    social_last_uri varchar(255),
    social_timestamp varchar(255),
    social_ip varchar(255),
    social_sha256 varchar(255),
    social_uuid4 varchar(255)
    )


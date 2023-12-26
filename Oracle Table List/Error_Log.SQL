CREATE TABLE Error_Log
(
    API_Name VARCHAR2(255),
    Error_Description VARCHAR2(1000),
    System_Date DATE DEFAULT SYSDATE
);
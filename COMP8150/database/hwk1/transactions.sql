DROP TABLE IF EXISTS TRANSACTIONS;
CREATE TABLE TRANSACTIONS (
   TRANSACTION_ID      INT           NOT NULL,  -- Unique identifier for a transaction
   PATIENT_ID          INT           NOT NULL,  -- Unique identifier of the patient that initiated this transaction
   LOCATION_ID         SMALLINT      NOT NULL,  -- Unique identifier for claim location
   CLAIM_AMOUNT        DECIMAL(10,2) NOT NULL,  -- Dollar amount for this claim (in USD)
   CLAIM_REASON_CODE   VARCHAR(8)    NOT NULL,  -- A standardized reason code for this claim
   CLAIM_DATE          DATE          NOT NULL,  -- The date on which this claim occurred.
   CLAIM_STATUS        ENUM('PENDING', 'APPROVED', 'DENIED') NOT NULL,-- The last status of this claim
   PRIMARY KEY (TRANSACTION_ID)
);

INSERT INTO TRANSACTIONS VALUES(10001, 1, 101, 100.50, 'R', '2015-01-17', 'APPROVED');
INSERT INTO TRANSACTIONS VALUES(10002, 2, 102, 20100.99, 'E', '2016-12-01', 'DENIED');
INSERT INTO TRANSACTIONS VALUES(10003, 2, 102, 17461.10, 'K', '2016-12-02', 'DENIED');
INSERT INTO TRANSACTIONS VALUES(10004, 3, 101, 100.50, 'R', '2017-01-17', 'APPROVED');
INSERT INTO TRANSACTIONS VALUES(10005, 2, 103, 99999.99, 'A', '2018-09-16', 'PENDING');


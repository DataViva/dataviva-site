ALTER TABLE account_user
ADD confirmation_code CHAR(128);

ALTER TABLE account_user
ADD confirmed BOOL default 0;
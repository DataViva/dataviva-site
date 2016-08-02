-- ALTER TABLE account_user DROP image, DROP nickname, DROP bio, DROP website; 

ALTER TABLE account_user ADD COLUMN profile int(1);
ALTER TABLE account_user ADD COLUMN institution varchar(256);
ALTER TABLE account_user ADD COLUMN occupation varchar(150);
ALTER TABLE account_user ADD COLUMN birthday DATE;
ALTER TABLE account_user ADD COLUMN uf varchar(2);
ALTER TABLE account_user ADD COLUMN city varchar(256);

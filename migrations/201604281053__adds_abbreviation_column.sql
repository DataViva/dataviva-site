ALTER TABLE `attrs_bra`
ADD COLUMN `abbreviation` VARCHAR(2) NULL AFTER `color`;

UPDATE attrs_bra
SET abbreviation = (SELECT attrs_abbreviation.abbreviation
                    FROM (select upper(right(left(attrs_bra.id, 3), 2)) as abbreviation, attrs_bra.id
                          from attrs_bra where length(attrs_bra.id)>3) attrs_abbreviation
                    WHERE attrs_bra.id = attrs_abbreviation.id);

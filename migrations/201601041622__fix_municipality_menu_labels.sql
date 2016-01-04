#Update side bar titles for Stacked - Evolução
#Wages (rais) and Employment (rais)
UPDATE apps_build SET
slug2_en='Employment by Location',
slug2_pt='Emprego por Localidade'
WHERE
dataset = 'rais' AND
id = 21;

UPDATE apps_build SET
slug2_en='Employment in an Industry by Location',
slug2_pt='Emprego em uma Atividade Econômica por Localidade'
WHERE
dataset = 'rais' AND
id = 22;

UPDATE apps_build SET
slug2_en='Employment of an Occupation by Location',
slug2_pt='Emprego de uma Ocupação por Localidade'
WHERE
dataset = 'rais' AND
id = 23;

UPDATE apps_build SET
slug2_en='Employment of an Occupation in an Industry by Location',
slug2_pt='Emprego de uma Ocupação em uma Atividade Econômica por Localidade'
WHERE
dataset = 'rais' AND
id = 24;

#-------------------------------

#Education (hedu)
UPDATE apps_build SET
slug2_en='Enrollment by Location',
slug2_pt='Matrículas por Localidade'
WHERE
dataset = 'hedu' AND
id = 107;

UPDATE apps_build SET
slug2_en='Enrollment in a Major by Location',
slug2_pt='Matrículas em um Curso por Localidade'
WHERE
dataset = 'hedu' AND
id = 108;

#-------------------------------

#School Census (sc)
UPDATE apps_build SET
slug2_en='Enrollment by Location',
slug2_pt='Matrículas por Localidade'
WHERE
dataset = 'sc' AND
id = 121;

UPDATE apps_build SET
slug2_en='Enrollment in a Major by Location',
slug2_pt='Matrículas em um Curso por Localidade'
WHERE
dataset = 'sc' AND
id = 122;

#-------------------------------

#International Trade (secex)
UPDATE apps_build SET
slug2_en='Imports/Exports by Location',
slug2_pt='Importações/Exportações por Localidade'
WHERE
dataset = 'secex' AND
id = 29;

UPDATE apps_build SET
slug2_en='Imports/Exports of a Product by Location',
slug2_pt='Importações/Exportações de um Produto por Localidade'
WHERE
dataset = 'secex' AND
id = 30;

UPDATE apps_build SET
slug2_en='Imports/Exports with a Country by Location',
slug2_pt='Importações/Exportações com um País por Localidade'
WHERE
dataset = 'secex' AND
id = 31;

UPDATE apps_build SET
slug2_en='Imports/Exports with a Country for a Product by Location',
slug2_pt='Importações/Exportações com um País de um Produto por Localidade'
WHERE
dataset = 'secex' AND
id = 32;

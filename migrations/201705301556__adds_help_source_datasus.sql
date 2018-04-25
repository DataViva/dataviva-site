INSERT INTO `dataviva`.`help_subject_question`
(`description_en`, `description_pt`, `answer_en`, `answer_pt`, `subject_id`, `active`)
VALUES
('DATASUS', 'DATASUS',
'<p>SUS IT Department – DATASUS<br/>Ministry of Health – MH</p>
<p>DATASUS makes available information that may subsidize an objective analysis of the health situation, the decision-making based on evidences and the making of health action programs. One of the department’s competencies is to keep the database collection needed for the information system in health and to the internal systems of institutional management.</p><p>The database consists of data from SUS Ambulatory Information System; Mortality Information System; Hospital Information Communication System; Hospital and Ambulatory Information Communication System; Live birth Information System; Pre-Natal, Childbirth, Puerperium and Child Monitoring and Evaluation System; National Registry of Health Establishments; Files with territorial base – municipality, health regions, citizenship territories, etc. – in use for the Health Information Dissemination; as well as maps and conversion files for TabWin and Tabnet use. Files with the Brazilian population distribution according to demographic census, population counts and estimations since 1980 by municipality, sex and age, and according to estimations made for TCU – The Brazilian Federal Court of Accounts – since 1992, by municipality.</p><p>Using the CNES database of DATASUS, DataViva shows annual information of Brazilian health establishments from 2008 onwards. The main variables are Health Establishment National Code, Health region, SUS linking, Administrative sphere, type of hospital bed/specialty, equipment type, establishment type, among other variables. The aggregation level in geographical terms can be done by federal unit, mesoregion, microregion and municipality.</p>
Access in:
<a href="http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1" target="_blank">http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1</a>',
'<p>Departamento de Inform&aacute;tica do SUS &ndash; DATASUS<br/>Minist&eacute;rio da Sa&uacute;de - MS</p>
<p>O DATASUS disponibiliza informa&ccedil;&otilde;es que podem servir para subsidiar an&aacute;lises objetivas da situa&ccedil;&atilde;o sanit&aacute;ria, tomadas de decis&atilde;o baseadas em evid&ecirc;ncias e elabora&ccedil;&atilde;o de programas de a&ccedil;&otilde;es de sa&uacute;de. Uma das compet&ecirc;ncias do departamento &eacute; manter o acervo das bases de dados necess&aacute;rios ao sistema de informa&ccedil;&otilde;es em sa&uacute;de e aos sistemas internos de gest&atilde;o institucional.</p><p>As bases compreendem os dados Sistema de Informa&ccedil;&otilde;es Ambulatoriais do SUS, Sistema de informa&ccedil;&otilde;es de Mortalidade, Sistema de Comunica&ccedil;&atilde;o de Informa&ccedil;&atilde;o Hospitalar, Sistema de Comunica&ccedil;&atilde;o de Informa&ccedil;&atilde;o Hospitalar e Ambulatorial, Sistema de informa&ccedil;&atilde;o de Nascidos Vivos, Sistema de Monitoramento e Avalia&ccedil;&atilde;o do Pr&eacute;-Natal, Parto, Puerp&eacute;rio e Crian&ccedil;a, Cadastro Nacional de Estabelecimentos de Sa&uacute;de, Arquivos com a base territorial (munic&iacute;pios, regi&otilde;es de sa&uacute;de, territ&oacute;rios da cidadania etc.) em uso para a Dissemina&ccedil;&atilde;o de Informa&ccedil;&otilde;es de Sa&uacute;de, assim como mapas e arquivos de convers&atilde;o para uso pelo TabWin e Tabnet. Arquivos com a distribui&ccedil;&atilde;o da popula&ccedil;&atilde;o brasileira segundo censos demogr&aacute;ficos, contagens populacionais e estimativas, desde 1980, por munic&iacute;pio, sexo e idade, e segundo as estimativas realizadas para o TCU, desde 1992, por munic&iacute;pio.</p><p>A partir dos dados da base CNES do DATASUS, o DataViva apresenta informa&ccedil;&otilde;es anuais dos estabelecimentos de sa&uacute;de brasileiros, de 2008 em diante. As principais vari&aacute;veis s&atilde;o: c&oacute;digo nacional do estabelecimento de sa&uacute;de, regi&atilde;o de sa&uacute;de, v&iacute;nculo com o SUS, esfera Administrativa, tipo de leito/especialidade, tipo de equipamento, tipo de estabelecimentos e entre outros. O n&iacute;vel de agrega&ccedil;&atilde;o, em termos geogr&aacute;ficos, pode ser feito por unidades da federa&ccedil;&atilde;o, mesorregi&otilde;es, microrregi&otilde;es e munic&iacute;pios.</p>
Access in:
<a href="http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1" target="_blank">http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1</a>',
3, 1);

INSERT INTO `dataviva`.`help_subject_question`
(`description_en`, `description_pt`, `answer_en`, `answer_pt`, `subject_id`, `active`)
VALUES
('Existing Quantity (Equipment)',
'Quantidade Existente (Equipamentos)',
'Corresponds to the quantity of existing equipment in the locality.',
'Corresponde a quantidade de equipamentos existentes na Localidade',
6, 1);

INSERT INTO `dataviva`.`help_subject_question`
(`description_en`, `description_pt`, `answer_en`, `answer_pt`, `subject_id`, `active`)
VALUES
('Quantity in Use (Equipment)',
'Quantidade em Uso (Equipamentos)',
'Corresponds to the amount of existing equipment that is in use by the locality.',
'Corresponde a quantidade de equipamentos existentes que estão em uso pela localidade.',
6, 1);

INSERT INTO `dataviva`.`help_subject_question`
(`description_en`, `description_pt`, `answer_en`, `answer_pt`, `subject_id`, `active`)
VALUES
('SUS availability',
'Disponibilidade para o SUS',
'Indicates if the equipment/establishment is available for SUS use in the locality.',
'Indica se o equipamento/estabelecimento está disponível para o uso do SUS na localidade.',
6, 1);

INSERT INTO `dataviva`.`help_subject_question`
(`description_en`, `description_pt`, `answer_en`, `answer_pt`, `subject_id`, `active`)
VALUES
('Hierarchy Level',
'Nível de Hierarquia',
'<p><b>01 - PAB/PABA</b>: Outpatient Health Establishment that only performs Basic Attention Procedures – PAB and/or Extended Basic Attention Procedures defined by NOAS.</p>
<p><b>02 - Medium - M1</b>: Outpatient Health Establishment that performs procedures of Medium Complexity defined by NOAS as level 1 reference - M1.</p>
<p><b>03 - Medium - M2 and M3</b>: Ambulatory Health Establishment that performs Medium Complexity procedures defined by NOAS as level 2 reference - M2 and/or level 3 reference - M3.</p>
<p><b>04 - High AMB</b>: Outpatient Health Establishment qualified to perform High Complexity procedures defined by the Ministry of Health.</p>
<p><b>05 - Low - M1 and M2</b>: Health Establishment that in addition to the procedures foreseen in hierarchy levels 01 and 02 performs first hospital care in pediatrics and medical clinics, child-birth and other hospital procedures of lesser complexity in medical clinic, surgical, pediatrics and gynecology/obstetrics.</p>
<p><b>06 - Medium - M2 and M3</b>: Health Establishment that performs procedures foreseen in hierarchy levels 02 and 03, in addition to hospital procedures of medium complexity. By definition, specialized hospitals are placed in this hierarchy level.</p>
<p><b>07 - Medium - M3</b>: Health Establishment that performs hospital procedures of medium complexity. It performs procedures foreseen in the establishments of hierarchy levels 02 and 03, covering ambulatory SADT of high complexity.</p>
<p><b>08 - High HOSP/AMB</b>: Health Establishment that performs procedures of high complexity in hospital or outpatient care.</p>',
'<p><b>01 - PAB/PABA</b>: Estabelecimento de Saúde ambulatorial que realiza somente Procedimentos de Atenção Básica – PAB e ou Procedimentos de Atenção Básica Ampliada definidos pela NOAS.</p>
<p><b>02 - Média - M1</b>: Estabelecimento de Saúde ambulatorial que realiza procedimentos de Média Complexidade definidos pela NOAS como de 1ºnível de referência – M1.</p>
<p><b>03 - Média - M2 e M3</b>: Estabelecimento de Saúde ambulatorial que realiza procedimentos de Média Complexidade definidos pela NOAS como de 2º nível de referência - M2.e /ou de 3º nível de referência – M3.</p>
<p><b>04 - Alta AMB</b>: Estabelecimento de Saúde ambulatorial capacitado a realizar procedimentos de Alta Complexidade definidos pelo Ministério da Saúde.</p>
<p><b>05 - Baixa - M1 e M2</b>: Estabelecimento de Saúde que realiza além dos procedimentos previstos nos de níveis de hierarquia 01 e 02, efetua primeiro atendimento hospitalar, em pediatria e clínica médica, partos e outros procedimentos hospitalares de menor complexidade em clínica médica, cirúrgica, pediatria e ginecologia/obstetrícia.</p>
<p><b>06 - Média - M2 e M3</b>: Estabelecimento de Saúde que realiza procedimentos previstos nos de níveis de hierarquia 02 e 03, além de procedimentos hospitalares de média complexidade. Por definição enquadram-se neste nível os hospitais especializados.</p>
<p><b>07 - Média - M3</b>: Estabelecimento de Saúde que realiza procedimentos hospitalares de média complexidade. Realiza procedimentos previstos nos estabelecimentos de níveis de hierarquia 02 e 03, abrangendo SADT ambulatorial de alta complexidade.</p>
<p><b>08 - Alta HOSP/AMB</b>: Estabelecimento de Saúde que realiza procedimentos de alta complexidade no âmbito hospitalar e ou ambulatorial.</p>',
6, 1);

INSERT INTO `dataviva`.`help_subject_question`
(`description_en`, `description_pt`, `answer_en`, `answer_pt`, `subject_id`, `active`)
VALUES
('Attention Level',
'Nível de Atenção',
'Indicates whether the establishment provides outpatient care, hospital care or outpatient and hospital care.',
'Indica se o estabelecimento presta atendimento ambulatorial, atendimento hospitalar ou atendimento ambulatorial e hospitalar.',
6, 1);

INSERT INTO `dataviva`.`help_subject_question`
(`description_en`, `description_pt`, `answer_en`, `answer_pt`, `subject_id`, `active`)
VALUES
('Provider type',
'Tipo de Prestador',
'Type of service provider (public, private, philanthropic, trade union).',
'Tipo de prestador de serviço (público, privado, filantrópico, sindicato).',
6, 1);

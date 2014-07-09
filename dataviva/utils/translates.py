# coding: utf-8
import json
''' Translates the columns names 
'''
def translate_columns(column, lang): 
      
    #data = "{\"compare\":{\"en\":\"Compare\",\"pt\":\"Comparar\"}],\"occugrid\":{\"en\":\"Occugrid\",\"pt\":\"Ocupações\"}],\"geo_map\":{\"en\":\"Geo Map\",\"pt\":\"Mapa\"}],\"network\":{\"en\":\"Network\",\"pt\":\"Rede\"}],\"rings\":{\"en\":\"Rings\",\"pt\":\"Anéis\"}],\"scatter\":{\"en\":\"Scatter\",\"pt\":\"Dispersão\"}],\"stacked\":{\"en\":\"Stacked\",\"pt\":\"Evolução\"}],\"tree_map\":{\"en\":\"Tree Map\",\"pt\":\"Tree Map\"}],\"axes\":{\"en\":\"Axes\",\"pt\":\"Eixos\"}],\"axes_desc_compare\":{\"en\":\"Changes the X and Y variables used in the chart.\",\"pt\":\"Altera o variáveis X e Y utilizadas no gráfico.\"}],\"xaxis_var\":{\"en\":\"X Axis\",\"pt\":\"Eixo X\"}],\"xaxis_var_desc_scatter\":{\"en\":\"Changes the X axis variable.\",\"pt\":\"Alterar a variável do eixo X.\"}],\"yaxis_var\":{\"en\":\"Y Axis\",\"pt\":\"Eixo Y\"}],\"yaxis_var_desc_scatter\":{\"en\":\"Changes the Y axis variable.\",\"pt\":\"Alterar a variável do eixo Y.\"}],\"order\":{\"en\":\"Order\",\"pt\":\"Ordenação\"}],\"order_desc_stacked\":{\"en\":\"Changes the ordering of the visible areas based on the selected sorting.\",\"pt\":\"Mudar a ordem das áreas visíveis com base na ordenação selecionada.\"}],\"asc\":{\"en\":\"Ascending\",\"pt\":\"Ascendente\"}],\"desc\":{\"en\":\"Descending\",\"pt\":\"Descendente\"}],\"layout\":{\"en\":\"Layout\",\"pt\":\"Layout\"}],\"layout_desc_stacked\":{\"en\":\"Changes the X axis between value and market share.\",\"pt\":\"Mudar o eixo X entre o valor e participação de mercado.\"}],\"value\":{\"en\":\"Value\",\"pt\":\"Valor\"}],\"share\":{\"en\":\"Market Share\",\"pt\":\"Participação de Mercado\"}],\"rca_scope\":{\"en\":\"RCA Scope\",\"pt\":\"Escopo do RCA\"}],\"rca_scope_desc_network\":{\"en\":\"Changes which RCA variable is used when highlighting products in the app.\",\"pt\":\"Altera qual RCA será utilizado para destacar produtos no app.\"}],\"rca_scope_desc_rings\":{\"en\":\"Changes which RCA variable is used when highlighting products in the app.\",\"pt\":\"Altera qual RCA será utilizado para destacar produtos no app.\"}],\"rca_scope_desc_scatter\":{\"en\":\"Changes which RCA variable is used when highlighting products in the app.\",\"pt\":\"Altera qual RCA será utilizado para destacar produtos no app.\"}],\"bra_rca\":{\"en\":\"Domestic\",\"pt\":\"Doméstico\"}],\"wld_rca\":{\"en\":\"International\",\"pt\":\"Internacional\"}],\"scale\":{\"en\":\"Scale\",\"pt\":\"Escala\"}],\"scale_desc_compare\":{\"en\":\"Changes the mathematical scale used on both axes.\",\"pt\":\"Altera a escala matemática utilizada em ambos os eixos.\"}],\"log\":{\"en\":\"Log\",\"pt\":\"Log\"}],\"linear\":{\"en\":\"Linear\",\"pt\":\"Linear\"}],\"spotlight\":{\"en\":\"Highlight RCA\",\"pt\":\"Realçar RCA\"}],\"spotlight_desc_network\":{\"en\":\"Removes coloring from nodes which do not have RCA.\",\"pt\":\"Remover cor dos nós que não têm RCA.\"}],\"spotlight_scatter\":{\"en\":\"Hide RCA\",\"pt\":\"Esconder RCA\"}],\"spotlight_scatter_desc_scatter\":{\"en\":\"Hides nodes that have RCA.\",\"pt\":\"Ocultar nós que possuem RCA.\"}],\"true\":{\"en\":\"On\",\"pt\":\"Liga\"}],\"false\":{\"en\":\"Off\",\"pt\":\"Desliga\"}],\"sorting\":{\"en\":\"Sort\",\"pt\":\"Ordenar\"}],\"sort\":{\"en\":\"Sort\",\"pt\":\"Ordenar\"}],\"sort_desc_stacked\":{\"en\":\"Changes the variable used to order the areas.\",\"pt\":\"Alterar a variável usada para ordenar as áreas.\"}],\"sort_desc_occugrid\":{\"en\":\"Changes the variable used to order the donut charts.\",\"pt\":\"Alterar a variável usada para ordenar os gráficos de rosca.\"}],\"sizing\":{\"en\":\"Size\",\"pt\":\"Tamanho\"}],\"sizing_desc_tree_map\":{\"en\":\"Changes the variable used to size the rectangles.\",\"pt\":\"Alterar a variável usada para o tamanho dos retângulos.\"}],\"sizing_desc_stacked\":{\"en\":\"Changes the Y axis variable.\",\"pt\":\"Alterar a variável do eixo Y.\"}],\"sizing_desc_network\":{\"en\":\"Changes the variable used to size the circles.\",\"pt\":\"Alterar a variável usada para o tamanho dos círculos.\"}],\"sizing_desc_compare\":{\"en\":\"Changes the variable used to size the circles.\",\"pt\":\"Alterar a variável usada para o tamanho dos círculos.\"}],\"sizing_desc_occugrid\":{\"en\":\"Changes the variable used to size the circles.\",\"pt\":\"Alterar a variável usada para o tamanho dos círculos.\"}],\"sizing_desc_scatter\":{\"en\":\"Changes the variable used to size the circles.\",\"pt\":\"Alterar a variável usada para o tamanho dos círculos.\"}],\"color_var\":{\"en\":\"Color\",\"pt\":\"Cor\"}],\"color_var_desc_tree_map\":{\"en\":\"Changes the variable used to color the rectangles.\",\"pt\":\"Alterar a variável utilizada para colorir os retângulos.\"}],\"color_var_desc_stacked\":{\"en\":\"Changes the variable used to color the areas.\",\"pt\":\"Alterar a variável utilizada para colorir as áreas.\"}],\"color_var_desc_geo_map\":{\"en\":\"Changes the variable used to color the locations.\",\"pt\":\"Alterar a variável utilizada para colorir os locais.\"}],\"color_var_desc_network\":{\"en\":\"Changes the variable used to color the circles.\",\"pt\":\"Alterar a variável utilizada para colorir os círculos.\"}],\"color_var_desc_rings\":{\"en\":\"Changes the variable used to color the circles.\",\"pt\":\"Alterar a variável utilizada para colorir os círculos.\"}],\"color_var_desc_compare\":{\"en\":\"Changes the variable used to color the circles.\",\"pt\":\"Alterar a variável utilizada para colorir os círculos.\"}],\"color_var_desc_occugrid\":{\"en\":\"Changes the variable used to color the circles.\",\"pt\":\"Alterar a variável utilizada para colorir os círculos.\"}],\"color_var_desc_scatter\":{\"en\":\"Changes the variable used to color the circles.\",\"pt\":\"Alterar a variável utilizada para colorir os círculos.\"}],\"active\":{\"en\":\"Available\",\"pt\":\"Disponível\"}],\"available\":{\"en\":\"Available\",\"pt\":\"Disponível\"}],\"not_available\":{\"en\":\"Not available\",\"pt\":\"Não disponível\"}],\"grouping\":{\"en\":\"Group\",\"pt\":\"Grupo\"}],\"grouping_desc_occugrid\":{\"en\":\"Groups the donut charts into different categorizations.\",\"pt\":\"Agrupar os gráficos de rosca em diferentes categorizações.\"}],\"none\":{\"en\":\"None\",\"pt\":\"Nenhum\"}],\"year\":{\"en\":\"Year\",\"pt\":\"Ano\"}],\"depth\":{\"en\":\"Depth\",\"pt\":\"Agregação\"}],\"depth_desc_tree_map\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"depth_desc_stacked\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"depth_desc_geo_map\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"depth_desc_network\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"depth_desc_rings\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"depth_desc_compare\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"depth_desc_occugrid\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"depth_desc_scatter\":{\"en\":\"Changes the level of aggregation.\",\"pt\":\"Alterar o nível de agregação.\"}],\"bra_2\":{\"en\":\"State\",\"pt\":\"Estado\"}],\"bra_4\":{\"en\":\"Mesoregion\",\"pt\":\"Mesorregião\"}],\"bra_6\":{\"en\":\"Microregion\",\"pt\":\"Microrregião\"}],\"bra_7\":{\"en\":\"Planning Region\",\"pt\":\"Região de Planejamento\"}],\"bra_8\":{\"en\":\"Municipality\",\"pt\":\"Município\"}],\"cbo_1\":{\"en\":\"Main Group\",\"pt\":\"Grande Grupo\"}],\"cbo_2\":{\"en\":\"Principal Subgroup\",\"pt\":\"SubGrupo Principal\"}],\"cbo_3\":{\"en\":\"Subgroup\",\"pt\":\"SubGrupo\"}],\"cbo_4\":{\"en\":\"Family\",\"pt\":\"Família\"}],\"cbo_6\":{\"en\":\"Occupation\",\"pt\":\"Ocupação\"}],\"isic_1\":{\"en\":\"Section\",\"pt\":\"Seção\"}],\"isic_3\":{\"en\":\"Division\",\"pt\":\"Divisão\"}],\"isic_4\":{\"en\":\"Group\",\"pt\":\"Grupo\"}],\"isic_5\":{\"en\":\"Class\",\"pt\":\"Classe\"}],\"hs_2\":{\"en\":\"Section\",\"pt\":\"Seção\"}],\"hs_4\":{\"en\":\"Chapter\",\"pt\":\"Capítulo\"}],\"hs_6\":{\"en\":\"Position\",\"pt\":\"Posição\"}],\"hs_8\":{\"en\":\"Sub-Position\",\"pt\":\"Sub-Posição\"}],\"wld_2\":{\"en\":\"Continent\",\"pt\":\"Continente\"}],\"wld_5\":{\"en\":\"Country\",\"pt\":\"País\"}],\"bra_2_plural\":{\"en\":\"States\",\"pt\":\"Estados\"}],\"bra_4_plural\":{\"en\":\"Mesoregions\",\"pt\":\"Mesorregiões\"}],\"bra_6_plural\":{\"en\":\"Microregions\",\"pt\":\"Microrregiões\"}],\"bra_7_plural\":{\"en\":\"Planning Regions\",\"pt\":\"Regiões de Planejamento\"}],\"bra_8_plural\":{\"en\":\"Municipalities\",\"pt\":\"Municípios\"}],\"cbo_1_plural\":{\"en\":\"Main Groups\",\"pt\":\"Grandes Grupos\"}],\"cbo_2_plural\":{\"en\":\"Principal Subgroups\",\"pt\":\"SubGrupos Principais\"}],\"cbo_3_plural\":{\"en\":\"Subgroups\",\"pt\":\"SubGrupos\"}],\"cbo_4_plural\":{\"en\":\"Families\",\"pt\":\"Famílias\"}],\"cbo_6_plural\":{\"en\":\"Occupations\",\"pt\":\"Ocupações\"}],\"isic_1_plural\":{\"en\":\"Sections\",\"pt\":\"Seções\"}],\"isic_3_plural\":{\"en\":\"Divisions\",\"pt\":\"Divisões\"}],\"isic_4_plural\":{\"en\":\"Groups\",\"pt\":\"Grupos\"}],\"isic_5_plural\":{\"en\":\"Classes\",\"pt\":\"Classes\"}],\"hs_2_plural\":{\"en\":\"Sections\",\"pt\":\"Seções\"}],\"hs_4_plural\":{\"en\":\"Chapters\",\"pt\":\"Capítulos\"}],\"hs_6_plural\":{\"en\":\"Positions\",\"pt\":\"Posições\"}],\"hs_8_plural\":{\"en\":\"Sub-Positions\",\"pt\":\"Sub-Posições\"}],\"wld_2_plural\":{\"en\":\"Continents\",\"pt\":\"Continentes\"}],\"wld_5_plural\":{\"en\":\"Countries\",\"pt\":\"Países\"}],\"eci\":{\"en\":\"Economic Complexity\",\"pt\":\"Complexidade Econômica\"}],\"eci_desc\":{\"en\":\"Economic Complexity measures how diversified and complex a location’s export production is.\",\"pt\":\"Complexidade Econômica mede quão diversificada e complexa é a produção de exportação de uma localidade.\"}],\"pci\":{\"en\":\"Product Complexity\",\"pt\":\"Complexidade do Produto\"}],\"pci_desc\":{\"en\":\"Product Complexity is a measure of how complex a product is, based on how many countries export the product and how diversified those exporters are.\",\"pt\":\"A Complexidade do Produto é uma medida de quão complexo é um produto, baseada no número de países que exportam o produto e quão diversificados são estes exportadores.\"}],\"bra_diversity\":{\"en\":\"Location Diversity\",\"pt\":\"Diversidade de Localidades\"}],\"bra_diversity_desc\":{\"en\":\"The number of unique municipalities where a given variable is present.\",\"pt\":\"O número de municípios únicos nos quais uma dada variável está presente.\"}],\"bra_diversity_eff\":{\"en\":\"Effective Location Diversity\",\"pt\":\"Diversidade Efetiva de Localidades\"}],\"bra_diversity_eff_desc\":{\"en\":\"The diversity of a given variable corrected for the share that each unit represents.\",\"pt\":\"A diversidade de uma dada variável corrigida pela participação que cada unidade representa.\"}],\"isic_diversity\":{\"en\":\"Industry Diversity\",\"pt\":\"Diversidade de Atividades\"}],\"isic_diversity_desc\":{\"en\":\"The number of unique 5-digit ISIC industries that are present for a given variable.\",\"pt\":\"O número de atividades únicas de 5 dígitos ISIC que estão presentes para uma dada variável.\"}],\"isic_diversity_eff\":{\"en\":\"Effective Industry Diversity\",\"pt\":\"Diversidade Efetiva de Atividades\"}],\"isic_diversity_eff_desc\":{\"en\":\"The diversity of a given variable corrected for the share that each unit represents.\",\"pt\":\"A diversidade de uma dada variável corrigida pela participação que cada unidade representa.\"}],\"cbo_diversity\":{\"en\":\"Occupation Diversity\",\"pt\":\"Diversidade de Ocupações\"}],\"cbo_diversity_desc\":{\"en\":\"The number of unique 4-digit CBO occupations that are present for a given variable.\",\"pt\":\"O número de ocupações únicas de 4 dígitos CBO que estão presentes para uma dada variável.\"}],\"cbo_diversity_eff\":{\"en\":\"Effective Occupation Diversity\",\"pt\":\"Diversidade Efetiva de Ocupações\"}],\"cbo_diversity_eff_desc\":{\"en\":\"The diversity of a given variable corrected for the share that each unit represents.\",\"pt\":\"A diversidade de uma dada variável corrigida pela participação que cada unidade representa.\"}],\"hs_diversity\":{\"en\":\"Product Diversity\",\"pt\":\"Diversidade de Produtos\"}],\"hs_diversity_desc\":{\"en\":\"The number of unique HS4 products that are present for a given variable.\",\"pt\":\"O número de produtos únicos HS4 que estão presentes para uma dada variável.\"}],\"hs_diversity_eff\":{\"en\":\"Effective Product Diversity\",\"pt\":\"Diversidade Efetiva de Produtos\"}],\"hs_diversity_eff_desc\":{\"en\":\"The diversity of a given variable corrected for the share that each unit represents.\",\"pt\":\"A diversidade de uma dada variável corrigida pela participação que cada unidade representa.\"}],\"wld_diversity\":{\"en\":\"Export Destination Diversity\",\"pt\":\"Diversidade de Destino das Exportações\"}],\"wld_diversity_desc\":{\"en\":\"The number of unique import countries that are present for a given variable.\",\"pt\":\"O número de países importadores únicos que estão presentes para uma dada variável.\"}],\"wld_diversity_eff\":{\"en\":\"Effective Export Destination Diversity\",\"pt\":\"Diversidade Efetiva de Destino das Exportações\"}],\"wld_diversity_eff_desc\":{\"en\":\"The diversity of a given variable corrected for the share that each unit represents.\",\"pt\":\"A diversidade de uma dada variável corrigida pela participação que cada unidade representa.\"}],\"distance\":{\"en\":\"Distance\",\"pt\":\"Distância\"}],\"distance_desc\":{\"en\":\"Distance is a measure used to indicate how “far away” any given location is from a particular industry, occupation or product.\",\"pt\":\"Distância é uma medida utilizada para indicar o quão longe uma localidade específica está de um determinado setor, ocupação ou produto.\"}],\"distance_wld\":{\"en\":\"International Distance\",\"pt\":\"Distância Internacional\"}],\"employed\":{\"en\":\"Employed\",\"pt\":\"Empregado\"}],\"importance\":{\"en\":\"Importance\",\"pt\":\"Importância\"}],\"importance_desc\":{\"en\":\"Importance measures the ubiquity of a given occupation in a particular industry. Occupations with a high importance in an industry are commonly employed in said industry.\",\"pt\":\"Importância mede a ubiquidade de uma determinada ocupação em um setor específico. As ocupações com um alto grau de importância em um determinado Setor são geralmente empregadas no Setor mencionado.\"}],\"elsewhere\":{\"en\":\"Employees Available In Other Industries\",\"pt\":\"Empregados em Outras Indústrias\"}],\"required\":{\"en\":\"Estimated Employees\",\"pt\":\"Estimativa de Empregados\"}],\"required_desc\":{\"en\":\"The estimated number of employees per establishment needed in order to have a successful establishment in an industry in a particular location.\",\"pt\":\"O número estimado de empregados por estabelecimento necessário para que um estabelecimento seja bem sucedido em um setor, em uma determinada localidade.\"}],\"growth_val\":{\"en\":\"Wage Growth\",\"pt\":\"Crescimento dos Salários\"}],\"growth_val_total\":{\"en\":\"Cumulative Wage Growth\",\"pt\":\"Crescimento Salarial Acumulada\"}],\"proximity\":{\"en\":\"Proximity\",\"pt\":\"Proximidade\"}],\"rca\":{\"en\":\"Domestic RCA\",\"pt\":\"RCA Doméstico\"}],\"rca_desc\":{\"en\":\"Revealed Comparative Advantage is a numeric value used to connote whether a particular product or industry is especially prominent in a location.\",\"pt\":\"A Vantagem Comparativa Revelada é um valor numérico utilizado para denotar se um produto ou setor em particular é especialmente proeminente em uma localidade.\"}],\"rca_wld\":{\"en\":\"International RCA\",\"pt\":\"RCA Internacional\"}],\"opp_gain\":{\"en\":\"Opportunity Gain\",\"pt\":\"Ganho de Oportunidade Doméstico\"}],\"opp_gain_desc\":{\"en\":\"Opportunity gain is a measure that indicates how much diversity is offered by an industry or product should the given location develop it.\",\"pt\":\"O ganho de oportunidade é uma medida que indica quanta diversidade é oferecida por um determinado setor ou produto se uma determinada localidade fosse desenvolvê-lo.\"}],\"opp_gain_wld\":{\"en\":\"International Opportunity Gain\",\"pt\":\"Ganho de Oportunidade Internacional\"}],\"val_usd_growth_pct\":{\"en\":\"Nominal Annual Growth Rate (1 year)\",\"pt\":\"Taxa Nominal de Crescimento Anual (1 ano)\"}],\"val_usd_growth_pct_5\":{\"en\":\"Nominal Annual Growth Rate (5 year)\",\"pt\":\"Taxa Nominal de Crescimento Anual (5 anos)\"}],\"val_usd_growth_val\":{\"en\":\"Growth Value (1 year)\",\"pt\":\"Valor de Crescimento (1 ano)\"}],\"val_usd_growth_val_5\":{\"en\":\"Growth Value (5 year)\",\"pt\":\"Valor de Crescimento (5 anos)\"}],\"wage_growth_pct\":{\"en\":\"Nominal Annual Wage Growth Rate (1 year)\",\"pt\":\"Taxa Nominal de Crescimento dos Salários Anual (1 ano)\"}],\"wage_growth_pct_5\":{\"en\":\"Nominal Annual Wage Growth Rate (5 year)\",\"pt\":\"Taxa Nominal de Crescimento dos Salários Anual (5 anos)\"}],\"wage_growth_val\":{\"en\":\"Wage Growth Value (1 year)\",\"pt\":\"Valor de Crescimento dos Salários (1 ano)\"}],\"wage_growth_val_5\":{\"en\":\"Wage Growth Value (5 year)\",\"pt\":\"Valor de Crescimento dos Salários (5 anos)\"}],\"num_emp_growth_pct\":{\"en\":\"Nominal Annual Employee Growth Rate (1 year)\",\"pt\":\"Taxa Nominal de Crescimento de Empregados Anual (1 ano)\"}],\"num_emp_growth_pct_5\":{\"en\":\"Nominal Annual Employee Growth Rate (5 year)\",\"pt\":\"Taxa Nominal de Crescimento de Empregados Anual (5 anos)\"}],\"num_emp_growth_val\":{\"en\":\"Employee Growth (1 year)\",\"pt\":\"Crescimento do Número de Empregados (1 ano)\"}],\"num_emp_growth_val_5\":{\"en\":\"Employee Growth (5 year)\",\"pt\":\"Crescimento do Número de Empregados (5 anos)\"}],\"rais\":{\"en\":\"Establishments and Employment (RAIS)\",\"pt\":\"Estabelecimentos e Emprego (RAIS)\"}],\"num_emp\":{\"en\":\"Total Employees\",\"pt\":\"Total de Empregados\"}],\"num_est\":{\"en\":\"Total Establishments\",\"pt\":\"Total de Estabelecimentos\"}],\"num_emp_est\":{\"en\":\"Employees per Establishment\",\"pt\":\"Empregados por Estabelecimento\"}],\"wage\":{\"en\":\"Total Monthly Wages\",\"pt\":\"Renda Mensal Total\"}],\"total_wage\":{\"en\":\"Total Monthly Wage\",\"pt\":\"Renda Mensal Total\"}],\"wage_avg\":{\"en\":\"Average Monthly Wage\",\"pt\":\"Renda Mensal Média\"}],\"wage_avg_bra\":{\"en\":\"Brazilian Average Wage\",\"pt\":\"Salário Médio Brasileiro\"}],\"secex\":{\"en\":\"Product Exports (SECEX)\",\"pt\":\"Exportações de Produtos (SECEX)\"}],\"val_usd\":{\"en\":\"Exports\",\"pt\":\"Exportações\"}],\"total_val_usd\":{\"en\":\"Total Exports\",\"pt\":\"Total de Exportações\"}],\"brazil\":{\"en\":\"Brazil\",\"pt\":\"Brasil\"}],\"bra_id\":{\"en\":\"BRA ID\",\"pt\":\"ID BRA\"}],\"category\":{\"en\":\"Sector\",\"pt\":\"Setor\"}],\"cbo_id\":{\"en\":\"CBO ID\",\"pt\":\"ID CBO\"}],\"color\":{\"en\":\"Sector\",\"pt\":\"Setor\"}],\"display_id\":{\"en\":\"ID\",\"pt\":\"ID\"}],\"hs_id\":{\"en\":\"HS ID\",\"pt\":\"ID HS\"}],\"id_ibge\":{\"en\":\"IBGE ID\",\"pt\":\"ID IBGE\"}],\"id\":{\"en\":\"ID\",\"pt\":\"ID\"}],\"isic_id\":{\"en\":\"ISIC ID\",\"pt\":\"ID ISIC\"}],\"name\":{\"en\":\"Name\",\"pt\":\"Nome\"}],\"name_en\":{\"en\":\"Name (English)\",\"pt\":\"Nome (Inglês)\"}],\"name_pt\":{\"en\":\"Name (Portuguese)\",\"pt\":\"Nome (Português)\"}],\"population\":{\"en\":\"Population\",\"pt\":\"População\"}],\"top\":{\"en\":\"Top\",\"pt\":\"Superior\"}],\"wld_id\":{\"en\":\"WLD ID\",\"pt\":\"ID WLD\"}],\"id_mdic\":{\"en\":\"MDIC ID\",\"pt\":\"ID MDIC\"}],\"rank\":{\"en\":\" \",\"pt\":\" \"}],\"bra\":{\"en\":\"Location\",\"pt\":\"Localidade\"}],\"bra_plural\":{\"en\":\"Locations\",\"pt\":\"Localidades\"}],\"cbo\":{\"en\":\"Occupation\",\"pt\":\"Ocupação\"}],\"cbo_plural\":{\"en\":\"Occupations\",\"pt\":\"Ocupações\"}],\"hs\":{\"en\":\"Product Export\",\"pt\":\"Produto Exportado\"}],\"hs_plural\":{\"en\":\"Product Exports\",\"pt\":\"Produtos Exportados\"}],\"icon\":{\"en\":\"Icon\",\"pt\":\"Ícone\"}],\"isic\":{\"en\":\"Industry\",\"pt\":\"Atividade Econômica\"}],\"isic_plural\":{\"en\":\"Industries\",\"pt\":\"Atividades Econômicas\"}],\"wld\":{\"en\":\"Export Destination\",\"pt\":\"Destino das Exportações\"}],\"wld_plural\":{\"en\":\"Export Destinations\",\"pt\":\"Destinos das Exportações\"}],\"bra_add\":{\"en\":\"add a location\",\"pt\":\"adicionar uma localidade\"}],\"cbo_add\":{\"en\":\"add an occupation\",\"pt\":\"adicionar uma ocupação\"}],\"hs_add\":{\"en\":\"add a product\",\"pt\":\"adicionar um produto\"}],\"isic_add\":{\"en\":\"add an industry\",\"pt\":\"adicionar uma atividade econômica\"}],\"wld_add\":{\"en\":\"add an export destination\",\"pt\":\"adicionar um destino das exportações\"}],\"download\":{\"en\":\"Download\",\"pt\":\"Download\"}],\"download_desc\":{\"en\":\"Choose from the following file types:\",\"pt\":\"Escolha um dos seguintes tipos de arquivo:\"}],\"csv\":{\"en\":\"Save as CSV\",\"pt\":\"Salvar como CSV\"}],\"csv_desc\":{\"en\":\"A table format that can be imported into a database or opened with Microsoft Excel.\",\"pt\":\"Um formato de tabela que pode ser importado para um banco de dados ou aberto com o Microsoft Excel.\"}],\"pdf\":{\"en\":\"Save as PDF\",\"pt\":\"Salvar como PDF\"}],\"pdf_desc\":{\"en\":\"Similar to SVG files, PDF files are vector-based and can be dynamically scaled.\",\"pt\":\"Semelhante a arquivos SVG, arquivos PDF são baseados em vetores e podem ser dimensionados de forma dinâmica.\"}],\"png\":{\"en\":\"Save as PNG\",\"pt\":\"Salvar como PNG\"}],\"png_desc\":{\"en\":\"A standard image file, similar to JPG or BMP.\",\"pt\":\"Um arquivo de imagem padrão, similar ao JPG ou BMP.\"}],\"svg\":{\"en\":\"Save as SVG\",\"pt\":\"Salvar como SVG\"}],\"svg_desc\":{\"en\":\"A vector-based file that can be resized without worrying about pixel resolution.\",\"pt\":\"Um arquivo com base em vetor que pode ser redimensionado sem se preocupar com pixel de resolução.\"}],\"basics\":{\"en\":\"Basic Values\",\"pt\":\"Valores Básicos\"}],\"growth\":{\"en\":\"Growth\",\"pt\":\"Crescimento\"}],\"calculations\":{\"en\":\"Strategic Indicators\",\"pt\":\"Indicadores Estratégicos\"}],\"Data Provided by\":{\"en\":\"Data Provided by\",\"pt\":\"Dados Fornecidos por\"}],\"View more visualizations on the full DataViva.info website.\":{\"en\":\"View more visualizations on the full DataViva.info website.\",\"pt\":\"Veja mais visualizações na versão completa do site DataViva.info.\"}],\"related_apps\":{\"en\":\"Related Apps\",\"pt\":\"Apps Relacionados\"}],\"other_apps\":{\"en\":\"Other Apps\",\"pt\":\"Outros Apps\"}],\"Show All Years\":{\"en\":\"Show All Years\",\"pt\":\"Mostrar Todos os Anos\"}],\"Build Not Available\":{\"en\":\"Build Not Available\",\"pt\":\"Construção Não Disponível\"}],\"Building App\":{\"en\":\"Building App\",\"pt\":\"Construindo App\"}],\"Downloading Additional Years\":{\"en\":\"Downloading Additional Years\",\"pt\":\"Baixando Anos Adicionais\"}],\"and\":{\"en\":\"and\",\"pt\":\"e\"}],\"showing\":{\"en\":\"Showing only\",\"pt\":\"Mostrando somente\"}],\"excluding\":{\"en\":\"Excluding\",\"pt\":\"Excluindo\"}],\"of\":{\"en\":\"of\",\"pt\":\"de\"}],\"with\":{\"en\":\"with\",\"pt\":\"com\"}],\"fill\":{\"en\":\"Fill\",\"pt\":\"Preenchido\"}],\"embed_url\":{\"en\":\"Embed URL\",\"pt\":\"URL para Incorporar\"}],\"share_url\":{\"en\":\"Shortened URL\",\"pt\":\"URL Abreviada\"}],\"social_media\":{\"en\":\"Social Networks\",\"pt\":\"Redes Sociais\"}],\"secex_2\":{\"en\":\"Based on State Production\",\"pt\":\"Baseado nos Estados Produtores\"}],\"secex_8\":{\"en\":\"Based on the Exporting Municipality\",\"pt\":\"Baseado nos Municípios Exportadores\"}],\"Click for More Info\":{\"en\":\"Click for more data and related apps.\",\"pt\":\"Clique para dados adicionais e aplicativos relacionados.\"}],\"Click to Zoom\":{\"en\":\"Click to Zoom\",\"pt\":\"Clique para Ampliar\"}],\"filter\":{\"en\":\"Hide Group\",\"pt\":\"Ocultar Grupo\"}],\"solo\":{\"en\":\"Solo Group\",\"pt\":\"Só este Grupo\"}],\"reset\":{\"en\":\"Click to Reset all Filters\",\"pt\":\"Clique para Eliminar todos os Filtros\"}],\"Primary Connections\":{\"en\":\"Primary Connections\",\"pt\":\"Conexões Primárias\"}],\"No Data Available\":{\"en\":\"No Data Available\",\"pt\":\"Não há dados disponíveis\"}],\"No Connections Available\":{\"en\":\"No Connections Available\",\"pt\":\"Não há conexões disponíveis\"}],\"Asked\":{\"en\":\"Asked\",\"pt\":\"Perguntado\"}],\"by\":{\"en\":\"by\",\"pt\":\"por\"}],\"point\":{\"en\":\"Point\",\"pt\":\"Ponto\"}],\"points\":{\"en\":\"Points\",\"pt\":\"Pontos\"}],\"reply\":{\"en\":\"Reply\",\"pt\":\"Resposta\"}],\"replies\":{\"en\":\"Replies\",\"pt\":\"Respostas\"}],\"votes\":{\"en\":\"Most Active\",\"pt\":\"Mais Frequente\"}],\"newest\":{\"en\":\"Most Recent\",\"pt\":\"Mais Recente\"}],\"questions\":{\"en\":\"Questions\",\"pt\":\"Perguntas\"}],\"learnmore_plural\":{\"en\":\"Learn more\",\"pt\":\"Saiba mais\"}],\"flagged\":{\"en\":\"This reply has been flagged.\",\"pt\":\"Esta resposta foi marcada.\"}],\"unflagged\":{\"en\":\"This flag on this reply has been removed.\",\"pt\":\"A marca desta resposta foi retirada.\"}],\"voted\":{\"en\":\"Your vote has been added.\",\"pt\":\"Seu voto foi enviado.\"}],\"unvoted\":{\"en\":\"Your vote was removed.\",\"pt\":\"Seu voto foi removido.\"}],\"edit\":{\"en\":\"Edit\",\"pt\":\"Editar\"}],\"visible\":{\"en\":\"Visible\",\"pt\":\"Visível\"}],\"hidden\":{\"en\":\"Hidden\",\"pt\":\"Oculto\"}],\"user\":{\"en\":\"User\",\"pt\":\"Usuário\"}],\"admin\":{\"en\":\"Admin\",\"pt\":\"Administrador\"}],\"remove\":{\"en\":\"Remove\",\"pt\":\"Remover\"}],\"remove_confirmation\":{\"en\":\"Are you sure to delete this item?\",\"pt\":\"Tem certeza que deseja remover este item?\"}],\"search\":{\"en\":\"Search\",\"pt\":\"Pesquisar\"}],\"search_results\":{\"en\":\"Search Results\",\"pt\":\"Resultados da Pesquisa\"}],\"select\":{\"en\":\"Select\",\"pt\":\"Escolher\"}],\"show\":{\"en\":\"Show\",\"pt\":\"Mostrar\"}],\"loading_attrs\":{\"en\":\"Loading Attribute List\",\"pt\":\"Carregando Lista de Atributos\"}],\"loading_items\":{\"en\":\"Loading More Items\",\"pt\":\"Carregar Mais Itens\"}],\"wait\":{\"en\":\"Please Wait\",\"pt\":\"Por favor Aguarde\"}],\"back\":{\"en\":\"Back\",\"pt\":\"Voltar\"}],\"Municipalities within\":{\"en\":\"Municipalities within\",\"pt\":\"Municípios dentro de\"}],\"No municipalities within that distance.\":{\"en\":\"No municipalities within that distance.\",\"pt\":\"Não existem municípios dentro desta distância.\"}],\"Including\":{\"en\":\"Including\",\"pt\":\"Incluindo\"}}"
    
    jj = ''' {

      
      "compare": {"en": "Compare", "pt": "Comparar"},
      "occugrid": {"en": "Occugrid", "pt": "Ocupa\u00e7\u00f5es"},
      "geo_map": {"en": "Geo Map", "pt": "Mapa"},
      "network": {"en": "Network", "pt": "Rede"},
      "rings": {"en": "Rings", "pt": "An\u00e9is"},
      "scatter": {"en": "Scatter", "pt": "Dispers\u00e3o"},
      "stacked": {"en": "Stacked", "pt": "Evolu\u00e7\u00e3o"},
      "tree_map": {"en": "Tree Map", "pt": "Tree Map"},

      
      "axes": {"en": "Axes", "pt": "Eixos"},
      "axes_desc_compare": {"en": "Changes the X and Y variables used in the chart.", "pt": "Altera o vari\u00e1veis X e Y utilizadas no gr\u00e1fico."},
      "xaxis_var": {"en": "X Axis", "pt": "Eixo X"},
      "xaxis_var_desc_scatter": {"en": "Changes the X axis variable.", "pt": "Alterar a vari\u00e1vel do eixo X."},
      "yaxis_var": {"en": "Y Axis", "pt": "Eixo Y"},
      "yaxis_var_desc_scatter": {"en": "Changes the Y axis variable.", "pt": "Alterar a vari\u00e1vel do eixo Y."},

      
      "order": {"en": "Order", "pt": "Ordena\u00e7\u00e3o"},
      "order_desc_stacked": {"en": "Changes the ordering of the visible areas based on the selected sorting.", "pt": "Mudar a ordem das \u00e1reas vis\u00edveis com base na ordena\u00e7\u00e3o selecionada."},
      "asc": {"en": "Ascending", "pt": "Ascendente"},
      "desc": {"en": "Descending", "pt": "Descendente"},

      
      "layout": {"en": "Layout", "pt": "Layout"},
      "layout_desc_stacked": {"en": "Changes the X axis between value and market share.", "pt": "Mudar o eixo X entre o valor e participa\u00e7\u00e3o de mercado."},
      "value": {"en": "Value", "pt": "Valor"},
      "share": {"en": "Market Share", "pt": "Participa\u00e7\u00e3o de Mercado"},

      
      "rca_scope": {"en": "RCA Scope", "pt": "Escopo do RCA"},
      "rca_scope_desc_network": {"en": "Changes which RCA variable is used when highlighting products in the app.", "pt": "Altera qual RCA ser\u00e1 utilizado para destacar produtos no app."},
      "rca_scope_desc_rings": {"en": "Changes which RCA variable is used when highlighting products in the app.", "pt": "Altera qual RCA ser\u00e1 utilizado para destacar produtos no app."},
      "rca_scope_desc_scatter": {"en": "Changes which RCA variable is used when highlighting products in the app.", "pt": "Altera qual RCA ser\u00e1 utilizado para destacar produtos no app."},
      "bra_rca": {"en": "Domestic", "pt": "Dom\u00e9stico"},
      "wld_rca": {"en": "International", "pt": "Internacional"},

      
      "scale": {"en": "Scale", "pt": "Escala"},
      "scale_desc_compare": {"en": "Changes the mathematical scale used on both axes.", "pt": "Altera a escala matem\u00e1tica utilizada em ambos os eixos."},
      "log": {"en": "Log", "pt": "Log"},
      "linear": {"en": "Linear", "pt": "Linear"},

      
      "spotlight": {"en": "Highlight RCA", "pt": "Real\u00e7ar RCA"},
      "spotlight_desc_network": {"en": "Removes coloring from nodes which do not have RCA.", "pt": "Remover cor dos n\u00f3s que n\u00e3o t\u00eam RCA."},
      "spotlight_scatter": {"en": "Hide RCA", "pt": "Esconder RCA"},
      "spotlight_scatter_desc_scatter": {"en": "Hides nodes that have RCA.", "pt": "Ocultar n\u00f3s que possuem RCA."},
      "true": {"en": "On", "pt": "Liga"},
      "false": {"en": "Off", "pt": "Desliga"},

    
      "sorting": {"en": "Sort", "pt": "Ordenar"},
      "sort": {"en": "Sort", "pt": "Ordenar"},
      "sort_desc_stacked": {"en": "Changes the variable used to order the areas.", "pt": "Alterar a vari\u00e1vel usada para ordenar as \u00e1reas."},
      "sort_desc_occugrid": {"en": "Changes the variable used to order the donut charts.", "pt": "Alterar a vari\u00e1vel usada para ordenar os gr\u00e1ficos de rosca."},

      
      "sizing": {"en": "Size", "pt": "Tamanho"},
      "sizing_desc_tree_map": {"en": "Changes the variable used to size the rectangles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos ret\u00e2ngulos."},
      "sizing_desc_stacked": {"en": "Changes the Y axis variable.", "pt": "Alterar a vari\u00e1vel do eixo Y."},
      "sizing_desc_network": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},
      "sizing_desc_compare": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},
      "sizing_desc_occugrid": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},
      "sizing_desc_scatter": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},

      
      "color_var": {"en": "Color", "pt": "Cor"},
      "color_var_desc_tree_map": {"en": "Changes the variable used to color the rectangles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os ret\u00e2ngulos."},
      "color_var_desc_stacked": {"en": "Changes the variable used to color the areas.", "pt": "Alterar a vari\u00e1vel utilizada para colorir as \u00e1reas."},
      "color_var_desc_geo_map": {"en": "Changes the variable used to color the locations.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os locais."},
      "color_var_desc_network": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_rings": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_compare": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_occugrid": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_scatter": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},

      
      "active": {"en": "Available", "pt": "Dispon\u00edvel"},
      "available": {"en": "Available", "pt": "Dispon\u00edvel"},
      "not_available": {"en": "Not available", "pt": "N\u00e3o dispon\u00edvel"},
      "grouping": {"en": "Group", "pt": "Grupo"},
      "grouping_desc_occugrid": {"en": "Groups the donut charts into different categorizations.", "pt": "Agrupar os gr\u00e1ficos de rosca em diferentes categoriza\u00e7\u00f5es."},
      "none": {"en": "None", "pt": "Nenhum"},
      "year": {"en": "Year", "pt": "Ano"},

      
      "depth": {"en": "Depth", "pt": "Agrega\u00e7\u00e3o"},
      "depth_desc_tree_map": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "depth_desc_stacked": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "depth_desc_geo_map": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "depth_desc_network": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "depth_desc_rings": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "depth_desc_compare": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "depth_desc_occugrid": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "depth_desc_scatter": {"en": "Changes the level of aggregation.", "pt": "Alterar o n\u00edvel de agrega\u00e7\u00e3o."},
      "bra_2": {"en": "State", "pt": "Estado"},
      "bra_4": {"en": "Mesoregion", "pt": "Mesorregi\u00e3o"},
      "bra_6": {"en": "Microregion", "pt": "Microrregi\u00e3o"},
      "bra_7": {"en": "Planning Region", "pt": "Regi\u00e3o de Planejamento"},
      "bra_8": {"en": "Municipality", "pt": "Munic\u00edpio"},
      "cbo_1": {"en": "Main Group", "pt": "Grande Grupo"},
      "cbo_2": {"en": "Principal Subgroup", "pt": "SubGrupo Principal"},
      "cbo_3": {"en": "Subgroup", "pt": "SubGrupo"},
      "cbo_4": {"en": "Family", "pt": "Fam\u00edlia"},
      "cbo_6": {"en": "Occupation", "pt": "Ocupa\u00e7\u00e3o"},
      "isic_1": {"en": "Section", "pt": "Se\u00e7\u00e3o"},
      "isic_3": {"en": "Division", "pt": "Divis\u00e3o"},
      "isic_4": {"en": "Group", "pt": "Grupo"},
      "isic_5": {"en": "Class", "pt": "Classe"},
      "hs_2": {"en": "Section", "pt": "Se\u00e7\u00e3o"},
      "hs_4": {"en": "Chapter", "pt": "Cap\u00edtulo"},
      "hs_6": {"en": "Position", "pt": "Posi\u00e7\u00e3o"},
      "hs_8": {"en": "Sub-Position", "pt": "Sub-Posi\u00e7\u00e3o"},
      "wld_2": {"en": "Continent", "pt": "Continente"},
      "wld_5": {"en": "Country", "pt": "Pa\u00eds"},
      "bra_2_plural": {"en": "States", "pt": "Estados"},
      "bra_4_plural": {"en": "Mesoregions", "pt": "Mesorregi\u00f5es"},
      "bra_6_plural": {"en": "Microregions", "pt": "Microrregi\u00f5es"},
      "bra_7_plural": {"en": "Planning Regions", "pt": "Regi\u00f5es de Planejamento"},
      "bra_8_plural": {"en": "Municipalities", "pt": "Munic\u00edpios"},
      "cbo_1_plural": {"en": "Main Groups", "pt": "Grandes Grupos"},
      "cbo_2_plural": {"en": "Principal Subgroups", "pt": "SubGrupos Principais"},
      "cbo_3_plural": {"en": "Subgroups", "pt": "SubGrupos"},
      "cbo_4_plural": {"en": "Families", "pt": "Fam\u00edlias"},
      "cbo_6_plural": {"en": "Occupations", "pt": "Ocupa\u00e7\u00f5es"},
      "isic_1_plural": {"en": "Sections", "pt": "Se\u00e7\u00f5es"},
      "isic_3_plural": {"en": "Divisions", "pt": "Divis\u00f5es"},
      "isic_4_plural": {"en": "Groups", "pt": "Grupos"},
      "isic_5_plural": {"en": "Classes", "pt": "Classes"},
      "hs_2_plural": {"en": "Sections", "pt": "Se\u00e7\u00f5es"},
      "hs_4_plural": {"en": "Chapters", "pt": "Cap\u00edtulos"},
      "hs_6_plural": {"en": "Positions", "pt": "Posi\u00e7\u00f5es"},
      "hs_8_plural": {"en": "Sub-Positions", "pt": "Sub-Posi\u00e7\u00f5es"},
      "wld_2_plural": {"en": "Continents", "pt": "Continentes"},
      "wld_5_plural": {"en": "Countries", "pt": "Pa\u00edses"},

     
      "eci": {"en": "Economic Complexity", "pt": "Complexidade Econ\u00f4mica"},
      "eci_desc": {"en": "Economic Complexity measures how diversified and complex a location’s export production is.", "pt": "Complexidade Econ\u00f4mica mede qu\u00e3o diversificada e complexa \u00e9 a produ\u00e7\u00e3o de exporta\u00e7\u00e3o de uma localidade."},
      "pci": {"en": "Product Complexity", "pt": "Complexidade do Produto"},
      "pci_desc": {"en": "Product Complexity is a measure of how complex a product is, based on how many countries export the product and how diversified those exporters are.", "pt": "A Complexidade do Produto \u00e9 uma medida de qu\u00e3o complexo \u00e9 um produto, baseada no n\u00famero de pa\u00edses que exportam o produto e qu\u00e3o diversificados s\u00e3o estes exportadores."},

      "bra_diversity": {"en": "Location Diversity", "pt": "Diversidade de Localidades"},
      "bra_diversity_desc": {"en": "The number of unique municipalities where a given variable is present.", "pt": "O n\u00famero de munic\u00edpios \u00fanicos nos quais uma dada vari\u00e1vel est\u00e1 presente."},
      "bra_diversity_eff": {"en": "Effective Location Diversity", "pt": "Diversidade Efetiva de Localidades"},
      "bra_diversity_eff_desc": {"en": "The diversity of a given variable corrected for the share that each unit represents.", "pt": "A diversidade de uma dada vari\u00e1vel corrigida pela participa\u00e7\u00e3o que cada unidade representa."},

      "isic_diversity": {"en": "Industry Diversity", "pt": "Diversidade de Atividades"},
      "isic_diversity_desc": {"en": "The number of unique 5-digit ISIC industries that are present for a given variable.", "pt": "O n\u00famero de atividades \u00fanicas de 5 d\u00edgitos ISIC que est\u00e3o presentes para uma dada vari\u00e1vel."},
      "isic_diversity_eff": {"en": "Effective Industry Diversity", "pt": "Diversidade Efetiva de Atividades"},
      "isic_diversity_eff_desc": {"en": "The diversity of a given variable corrected for the share that each unit represents.", "pt": "A diversidade de uma dada vari\u00e1vel corrigida pela participa\u00e7\u00e3o que cada unidade representa."},

      "cbo_diversity": {"en": "Occupation Diversity", "pt": "Diversidade de Ocupa\u00e7\u00f5es"},
      "cbo_diversity_desc": {"en": "The number of unique 4-digit CBO occupations that are present for a given variable.", "pt": "O n\u00famero de ocupa\u00e7\u00f5es \u00fanicas de 4 d\u00edgitos CBO que est\u00e3o presentes para uma dada vari\u00e1vel."},
      "cbo_diversity_eff": {"en": "Effective Occupation Diversity", "pt": "Diversidade Efetiva de Ocupa\u00e7\u00f5es"},
      "cbo_diversity_eff_desc": {"en": "The diversity of a given variable corrected for the share that each unit represents.", "pt": "A diversidade de uma dada vari\u00e1vel corrigida pela participa\u00e7\u00e3o que cada unidade representa."},

      "hs_diversity": {"en": "Product Diversity", "pt": "Diversidade de Produtos"},
      "hs_diversity_desc": {"en": "The number of unique HS4 products that are present for a given variable.", "pt": "O n\u00famero de produtos \u00fanicos HS4 que est\u00e3o presentes para uma dada vari\u00e1vel."},
      "hs_diversity_eff": {"en": "Effective Product Diversity", "pt": "Diversidade Efetiva de Produtos"},
      "hs_diversity_eff_desc": {"en": "The diversity of a given variable corrected for the share that each unit represents.", "pt": "A diversidade de uma dada vari\u00e1vel corrigida pela participa\u00e7\u00e3o que cada unidade representa."},

      "wld_diversity": {"en": "Export Destination Diversity", "pt": "Diversidade de Destino das Exporta\u00e7\u00f5es"},
      "wld_diversity_desc": {"en": "The number of unique import countries that are present for a given variable.", "pt": "O n\u00famero de pa\u00edses importadores \u00fanicos que est\u00e3o presentes para uma dada vari\u00e1vel."},
      "wld_diversity_eff": {"en": "Effective Export Destination Diversity", "pt": "Diversidade Efetiva de Destino das Exporta\u00e7\u00f5es"},
      "wld_diversity_eff_desc": {"en": "The diversity of a given variable corrected for the share that each unit represents.", "pt": "A diversidade de uma dada vari\u00e1vel corrigida pela participa\u00e7\u00e3o que cada unidade representa."},

      "distance": {"en": "Distance", "pt": "Dist\u00e2ncia"},
      "distance_desc": {"en": "Distance is a measure used to indicate how “far away” any given location is from a particular industry, occupation or product.", "pt": "Dist\u00e2ncia \u00e9 uma medida utilizada para indicar o qu\u00e3o longe uma localidade espec\u00edfica est\u00e1 de um determinado setor, ocupa\u00e7\u00e3o ou produto."},
      "distance_wld": {"en": "International Distance", "pt": "Dist\u00e2ncia Internacional"},
      "employed": {"en": "Employed", "pt": "Empregado"},
      "importance": {"en": "Importance", "pt": "Import\u00e2ncia"},
      "importance_desc": {"en": "Importance measures the ubiquity of a given occupation in a particular industry. Occupations with a high importance in an industry are commonly employed in said industry.", "pt": "Import\u00e2ncia mede a ubiquidade de uma determinada ocupa\u00e7\u00e3o em um setor espec\u00edfico. As ocupa\u00e7\u00f5es com um alto grau de import\u00e2ncia em um determinado Setor s\u00e3o geralmente empregadas no Setor mencionado."},
      "elsewhere": {"en": "Employees Available In Other Industries", "pt": "Empregados em Outras Ind\u00fastrias"},
      "required": {"en": "Estimated Employees", "pt": "Estimativa de Empregados"},
      "required_desc": {"en": "The estimated number of employees per establishment needed in order to have a successful establishment in an industry in a particular location.", "pt": "O n\u00famero estimado de empregados por estabelecimento necess\u00e1rio para que um estabelecimento seja bem sucedido em um setor, em uma determinada localidade."},
      "growth_val": {"en": "Wage Growth", "pt": "Crescimento dos Sal\u00e1rios"},
      "growth_val_total": {"en": "Cumulative Wage Growth", "pt": "Crescimento Salarial Acumulada"},
      "proximity": {"en": "Proximity", "pt": "Proximidade"},
      "rca": {"en": "Domestic RCA", "pt": "RCA Dom\u00e9stico"},
      "rca_desc": {"en": "Revealed Comparative Advantage is a numeric value used to connote whether a particular product or industry is especially prominent in a location.", "pt": "A Vantagem Comparativa Revelada \u00e9 um valor num\u00e9rico utilizado para denotar se um produto ou setor em particular \u00e9 especialmente proeminente em uma localidade."},
      "rca_wld": {"en": "International RCA", "pt": "RCA Internacional"},

      "opp_gain": {"en": "Opportunity Gain", "pt": "Ganho de Oportunidade Dom\u00e9stico"},
      "opp_gain_desc": {"en": "Opportunity gain is a measure that indicates how much diversity is offered by an industry or product should the given location develop it.", "pt": "O ganho de oportunidade \u00e9 uma medida que indica quanta diversidade \u00e9 oferecida por um determinado setor ou produto se uma determinada localidade fosse desenvolv\u00ea-lo."},
      "opp_gain_wld": {"en": "International Opportunity Gain", "pt": "Ganho de Oportunidade Internacional"},

      "val_usd_growth_pct": {"en": "Nominal Annual Growth Rate (1 year)", "pt": "Taxa Nominal de Crescimento Anual (1 ano)"},
      "val_usd_growth_pct_5": {"en": "Nominal Annual Growth Rate (5 year)", "pt": "Taxa Nominal de Crescimento Anual (5 anos)"},
      "val_usd_growth_val": {"en": "Growth Value (1 year)", "pt": "Valor de Crescimento (1 ano)"},
      "val_usd_growth_val_5": {"en": "Growth Value (5 year)", "pt": "Valor de Crescimento (5 anos)"},

      "wage_growth_pct": {"en": "Nominal Annual Wage Growth Rate (1 year)", "pt": "Taxa Nominal de Crescimento dos Sal\u00e1rios Anual (1 ano)"},
      "wage_growth_pct_5": {"en": "Nominal Annual Wage Growth Rate (5 year)", "pt": "Taxa Nominal de Crescimento dos Sal\u00e1rios Anual (5 anos)"},
      "wage_growth_val": {"en": "Wage Growth Value (1 year)", "pt": "Valor de Crescimento dos Sal\u00e1rios (1 ano)"},
      "wage_growth_val_5": {"en": "Wage Growth Value (5 year)", "pt": "Valor de Crescimento dos Sal\u00e1rios (5 anos)"},
      "num_emp_growth_pct": {"en": "Nominal Annual Employee Growth Rate (1 year)", "pt": "Taxa Nominal de Crescimento de Empregados Anual (1 ano)"},
      "num_emp_growth_pct_5": {"en": "Nominal Annual Employee Growth Rate (5 year)", "pt": "Taxa Nominal de Crescimento de Empregados Anual (5 anos)"},
      "num_emp_growth_val": {"en": "Employee Growth (1 year)", "pt": "Crescimento do N\u00famero de Empregados (1 ano)"},
      "num_emp_growth_val_5": {"en": "Employee Growth (5 year)", "pt": "Crescimento do N\u00famero de Empregados (5 anos)"},

      
      "rais": {"en": "Establishments and Employment (RAIS)", "pt": "Estabelecimentos e Emprego (RAIS)"},
      "num_emp": {"en": "Total Employees", "pt": "Total de Empregados"},
      "num_est": {"en": "Total Establishments", "pt": "Total de Estabelecimentos"},
      "num_emp_est": {"en": "Employees per Establishment", "pt": "Empregados por Estabelecimento"},
      "wage": {"en": "Total Monthly Wages", "pt": "Renda Mensal Total"},
      "total_wage": {"en": "Total Monthly Wage", "pt": "Renda Mensal Total"},
      "wage_avg": {"en": "Average Monthly Wage", "pt": "Renda Mensal M\u00e9dia"},
      "wage_avg_bra": {"en": "Brazilian Average Wage", "pt": "Sal\u00e1rio M\u00e9dio Brasileiro"},

     
      "secex": {"en": "Product Exports (SECEX)", "pt": "Exporta\u00e7\u00f5es de Produtos (SECEX)"},
      "val_usd": {"en": "Exports", "pt": "Exporta\u00e7\u00f5es"},
      "total_val_usd": {"en": "Total Exports", "pt": "Total de Exporta\u00e7\u00f5es"},

      
      "brazil": {"en": "Brazil", "pt": "Brasil"},
      "bra_id": {"en": "BRA ID", "pt": "ID BRA"},
      "category": {"en": "Sector", "pt": "Setor"},
      "cbo_id": {"en": "CBO ID", "pt": "ID CBO"},
      "color": {"en": "Sector", "pt": "Setor"},
      "display_id": {"en": "ID", "pt": "ID"},
      "hs_id": {"en": "HS ID", "pt": "ID HS"},
      "id_ibge": {"en": "IBGE ID", "pt": "ID IBGE"},
      "id": {"en": "ID", "pt": "ID"},
      "isic_id": {"en": "ISIC ID", "pt": "ID ISIC"},
      "name": {"en": "Name", "pt": "Nome"},
      "name_en": {"en": "Name (English)", "pt": "Nome (Ingl\u00eas)"},
      "name_pt": {"en": "Name (Portuguese)", "pt": "Nome (Portugu\u00eas)"},
      "population": {"en": "Population", "pt": "Popula\u00e7\u00e3o"},
      "top": {"en": "Top", "pt": "Superior"},
      "wld_id": {"en": "WLD ID", "pt": "ID WLD"},
      "id_mdic": {"en": "MDIC ID", "pt": "ID MDIC"},
      "rank": {"en": " ", "pt": " "},

     
      "bra": {"en": "Location", "pt": "Localidade"},
      "bra_plural": {"en": "Locations", "pt": "Localidades"},
      "cbo": {"en": "Occupation", "pt": "Ocupa\u00e7\u00e3o"},
      "cbo_plural": {"en": "Occupations", "pt": "Ocupa\u00e7\u00f5es"},
      "hs": {"en": "Product Export", "pt": "Produto Exportado"},
      "hs_plural": {"en": "Product Exports", "pt": "Produtos Exportados"},
      "icon": {"en": "Icon", "pt": "\u00cdcone"},
      "isic": {"en": "Industry", "pt": "Atividade Econ\u00f4mica"},
      "isic_plural": {"en": "Industries", "pt": "Atividades Econ\u00f4micas"},
      "wld": {"en": "Export Destination", "pt": "Destino das Exporta\u00e7\u00f5es"},
      "wld_plural": {"en": "Export Destinations", "pt": "Destinos das Exporta\u00e7\u00f5es"},

      "bra_add": {"en": "add a location", "pt": "adicionar uma localidade"},
      "cbo_add": {"en": "add an occupation", "pt": "adicionar uma ocupa\u00e7\u00e3o"},
      "hs_add": {"en": "add a product", "pt": "adicionar um produto"},
      "isic_add": {"en": "add an industry", "pt": "adicionar uma atividade econ\u00f4mica"},
      "wld_add": {"en": "add an export destination", "pt": "adicionar um destino das exporta\u00e7\u00f5es"},

      
      "download": {"en": "Download", "pt": "Download"},
      "download_desc": {"en": "Choose from the following file types:", "pt": "Escolha um dos seguintes tipos de arquivo:"},
      "csv": {"en": "Save as CSV", "pt": "Salvar como CSV"},
      "csv_desc": {"en": "A table format that can be imported into a database or opened with Microsoft Excel.", "pt": "Um formato de tabela que pode ser importado para um banco de dados ou aberto com o Microsoft Excel."},
      "pdf": {"en": "Save as PDF", "pt": "Salvar como PDF"},
      "pdf_desc": {"en": "Similar to SVG files, PDF files are vector-based and can be dynamically scaled.", "pt": "Semelhante a arquivos SVG, arquivos PDF s\u00e3o baseados em vetores e podem ser dimensionados de forma din\u00e2mica."},
      "png": {"en": "Save as PNG", "pt": "Salvar como PNG"},
      "png_desc": {"en": "A standard image file, similar to JPG or BMP.", "pt": "Um arquivo de imagem padr\u00e3o, similar ao JPG ou BMP."},
      "svg": {"en": "Save as SVG", "pt": "Salvar como SVG"},
      "svg_desc": {"en": "A vector-based file that can be resized without worrying about pixel resolution.", "pt": "Um arquivo com base em vetor que pode ser redimensionado sem se preocupar com pixel de resolu\u00e7\u00e3o."},

      
      "basics": {"en": "Basic Values", "pt": "Valores B\u00e1sicos"},
      "growth": {"en": "Growth", "pt": "Crescimento"},
      "calculations": {"en": "Strategic Indicators", "pt": "Indicadores Estrat\u00e9gicos"},
      "Data Provided by": {"en": "Data Provided by", "pt": "Dados Fornecidos por"},
      "View more visualizations on the full DataViva.info website.": {"en": "View more visualizations on the full DataViva.info website.", "pt": "Veja mais visualiza\u00e7\u00f5es na vers\u00e3o completa do site DataViva.info."},
      "related_apps": {"en": "Related Apps", "pt": "Apps Relacionados"},
      "other_apps": {"en": "Other Apps", "pt": "Outros Apps"},
      "Show All Years": {"en": "Show All Years", "pt": "Mostrar Todos os Anos"},
      "Build Not Available": {"en": "Build Not Available", "pt": "Constru\u00e7\u00e3o N\u00e3o Dispon\u00edvel"},
      "Building App": {"en": "Building App", "pt": "Construindo App"},
      "Downloading Additional Years": {"en": "Downloading Additional Years", "pt": "Baixando Anos Adicionais"},
      "and": {"en": "and", "pt": "e"},
      "showing": {"en": "Showing only", "pt": "Mostrando somente"},
      "excluding": {"en": "Excluding", "pt": "Excluindo"},
      "of": {"en": "of", "pt": "de"},
      "with": {"en": "with", "pt": "com"},
      "and": {"en": "and", "pt": "e"},
      "fill": {"en": "Fill", "pt": "Preenchido"},
      "embed_url": {"en": "Embed URL", "pt": "URL para Incorporar"},
      "share_url": {"en": "Shortened URL", "pt": "URL Abreviada"},
      "social_media": {"en": "Social Networks", "pt": "Redes Sociais"},
      "secex_2": {"en": "Based on State Production", "pt": "Baseado nos Estados Produtores"},
      "secex_8": {"en": "Based on the Exporting Municipality", "pt": "Baseado nos Municípios Exportadores"},

     
      "Click for More Info": {"en": "Click for more data and related apps.", "pt": "Clique para dados adicionais e aplicativos relacionados."},
      "Click to Zoom": {"en": "Click to Zoom", "pt": "Clique para Ampliar"},
      "filter": {"en": "Hide Group", "pt": "Ocultar Grupo"},
      "solo": {"en": "Solo Group", "pt": "S\u00f3 este Grupo"},
      "reset": {"en": "Click to Reset all Filters", "pt": "Clique para Eliminar todos os Filtros"},
      "Primary Connections": {"en": "Primary Connections", "pt": "Conex\u00f5es Prim\u00e1rias"},
      "No Data Available": {"en": "No Data Available", "pt": "N\u00e3o h\u00e1 dados dispon\u00edveis"},
      "No Connections Available": {"en": "No Connections Available", "pt": "N\u00e3o h\u00e1 conex\u00f5es dispon\u00edveis"},

    
      "Asked": {"en": "Asked", "pt": "Perguntado"},
      "by": {"en": "by", "pt": "por"},
      "point": {"en": "Point", "pt": "Ponto"},
      "points": {"en": "Points", "pt": "Pontos"},
      "reply": {"en": "Reply", "pt": "Resposta"},
      "replies": {"en": "Replies", "pt": "Respostas"},
      "votes": {"en": "Most Active", "pt": "Mais Frequente"},
      "newest": {"en": "Most Recent", "pt": "Mais Recente"},
      "questions": {"en": "Questions", "pt": "Perguntas"},
      "learnmore_plural": {"en": "Learn more", "pt": "Saiba mais"},
      "flagged": {"en": "This reply has been flagged.", "pt": "Esta resposta foi marcada."},
      "unflagged": {"en": "This flag on this reply has been removed.", "pt": "A marca desta resposta foi retirada."},
      "voted": {"en": "Your vote has been added.", "pt": "Seu voto foi enviado."},
      "unvoted": {"en": "Your vote was removed.", "pt": "Seu voto foi removido."},

      
      "edit": {"en": "Edit", "pt": "Editar"},
      "visible": {"en": "Visible", "pt": "Vis\u00edvel"},
      "hidden": {"en": "Hidden", "pt": "Oculto"},
      "user": {"en": "User", "pt": "Usu\u00e1rio"},
      "admin": {"en": "Admin", "pt": "Administrador"},
      "remove": {"en": "Remove", "pt": "Remover"},
      "remove_confirmation": {"en": "Are you sure to delete this item?", "pt": "Tem certeza que deseja remover este item?"},


      "search": {"en": "Search", "pt": "Pesquisar"},
      "search_results": {"en": "Search Results", "pt": "Resultados da Pesquisa"},
      "select": {"en": "Select", "pt": "Escolher"},
      "show": {"en": "Show", "pt": "Mostrar"},
      "loading_attrs": {"en": "Loading Attribute List", "pt": "Carregando Lista de Atributos"},
      "loading_items": {"en": "Loading More Items", "pt": "Carregar Mais Itens"},
      "wait": {"en": "Please Wait", "pt": "Por favor Aguarde"},
      "back": {"en": "Back", "pt": "Voltar"},
      "Municipalities within": {"en": "Municipalities within", "pt": "Munic\u00edpios dentro de"},
      "No municipalities within that distance.": {"en": "No municipalities within that distance.", "pt": "N\u00e3o existem munic\u00edpios dentro desta dist\u00e2ncia."},
      "Including": {"en": "Including", "pt": "Incluindo"}

    } '''


    js = json.loads(jj)
    
    print js['diversity']
    return "ie"

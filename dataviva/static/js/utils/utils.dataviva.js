var dataviva = {};
dataviva.slide = {};
dataviva.popover = {};
dataviva.slide.timing = 0.75, // timing of page slides, in seconds

dataviva.obj2csv = function(obj) {
  var str = ''

  for (var key in obj) {
    str += key
    str += ","
    var o = obj[key]
    for (l in o) {
      str += o[l]
      str += ","
    }
    str = str.substr(0, str.length - 1)
    str += "\n"
  }
  
  return str;
  
}

dataviva.format = {};
dataviva.format.text = function(text,name,l) {
  
  if (!l) var l = dataviva.language
  
  if (text.indexOf("top_") == 0) {
    var x = text.substring(4)
    if (l == "pt") return format_name(x) + " " + format_name("top")
    else return format_name("top") + " " + format_name(x)
  }
  
  var exceptions = ["id","cbo_id","isic_id","wld_id","hs_id","bra_id","id_ibge"]
  
  if (exceptions.indexOf(name) >= 0) return text.toUpperCase()
  else if (text.indexOf("cp_bra_") == 0 && app) {
    var arr = text.split("_")
    arr.shift()
    arr.shift()
    var index = arr.shift()
    text = arr.join("_")
    return app.build.bra[index]["name_"+l] + " ("+format_name(text)+")"
  }
  else if (!name || (name.indexOf("_display") < 0 && name.indexOf("_id") < 0)) {
    return format_name(text)
  }
  else return text
  
  function format_name(name) {
  
    var labels = {
    
      // App Titles
      "compare": {"en": "Compare", "pt": "Comparar"},
      "occugrid": {"en": "Occugrid", "pt": "Ocupa\u00e7\u00f5es"},
      "geo_map": {"en": "Geo Map", "pt": "Mapa"},
      "network": {"en": "Network", "pt": "Rede"},
      "rings": {"en": "Rings", "pt": "An\u00e9is"},
      "scatter": {"en": "Scatter", "pt": "Dispers\u00e3o"},
      "stacked": {"en": "Stacked", "pt": "Evolu\u00e7\u00e3o"},
      "tree_map": {"en": "Tree Map", "pt": "Tree Map"},

      // Axes
      "axes": {"en": "Axes", "pt": "Eixos"},
      "axes_desc_compare": {"en": "Changes the X and Y variables used in the chart.", "pt": "Altera o vari\u00e1veis X e Y utilizadas no gr\u00e1fico."},
      "xaxis_var": {"en": "X Axis", "pt": "Eixo X"},
      "xaxis_var_desc_scatter": {"en": "Changes the X axis variable.", "pt": "Alterar a vari\u00e1vel do eixo X."},
      "yaxis_var": {"en": "Y Axis", "pt": "Eixo Y"},
      "yaxis_var_desc_scatter": {"en": "Changes the Y axis variable.", "pt": "Alterar a vari\u00e1vel do eixo Y."},

      // Stacked Area Sorting/Order
      "order": {"en": "Order", "pt": "Ordena\u00e7\u00e3o"},
      "order_desc_stacked": {"en": "Changes the ordering of the visible areas based on the selected sorting.", "pt": "Mudar a ordem das \u00e1reas vis\u00edveis com base na ordena\u00e7\u00e3o selecionada."},
      "asc": {"en": "Ascending", "pt": "Ascendente"},
      "desc": {"en": "Descending", "pt": "Descendente"},
    
      // Stacked Area Layout Type
      "layout": {"en": "Layout", "pt": "Layout"},
      "layout_desc_stacked": {"en": "Changes the X axis between value and market share.", "pt": "Mudar o eixo X entre o valor e participa\u00e7\u00e3o de mercado."},
      "value": {"en": "Value", "pt": "Valor"},
      "share": {"en": "Market Share", "pt": "Participa\u00e7\u00e3o de Mercado"},
    
      // RCA Scope Toggle
      "rca_scope": {"en": "RCA Scope", "pt": "Escopo do RCA"},
      "rca_scope_desc_network": {"en": "Changes which RCA variable is used when highlighting products in the app.", "pt": "Altera qual RCA ser\u00e1 utilizado para destacar produtos no app."},
      "rca_scope_desc_rings": {"en": "Changes which RCA variable is used when highlighting products in the app.", "pt": "Altera qual RCA ser\u00e1 utilizado para destacar produtos no app."},
      "rca_scope_desc_scatter": {"en": "Changes which RCA variable is used when highlighting products in the app.", "pt": "Altera qual RCA ser\u00e1 utilizado para destacar produtos no app."},
      "bra_rca": {"en": "Domestic", "pt": "Dom\u00e9stico"},
      "wld_rca": {"en": "International", "pt": "Internacional"},

      // Scale Toggle
      "scale": {"en": "Scale", "pt": "Escala"},
      "scale_desc_compare": {"en": "Changes the mathematical scale used on both axes.", "pt": "Altera a escala matem\u00e1tica utilizada em ambos os eixos."},
      "log": {"en": "Log", "pt": "Log"},
      "linear": {"en": "Linear", "pt": "Linear"},

      // Spotlight Toggle
      "spotlight": {"en": "Highlight RCA", "pt": "Real\u00e7ar RCA"},
      "spotlight_desc_network": {"en": "Removes coloring from nodes which do not have RCA.", "pt": "Remover cor dos n\u00f3s que n\u00e3o t\u00eam RCA."},
      "spotlight_scatter": {"en": "Hide RCA", "pt": "Esconder RCA"},
      "spotlight_scatter_desc_scatter": {"en": "Hides nodes that have RCA.", "pt": "Ocultar n\u00f3s que possuem RCA."},
      "true": {"en": "On", "pt": "Liga"},
      "false": {"en": "Off", "pt": "Desliga"},
      
      // Sorting Toggle
      "sorting": {"en": "Sort", "pt": "Ordenar"},
      "sort": {"en": "Sort", "pt": "Ordenar"},
      "sort_desc_stacked": {"en": "Changes the variable used to order the areas.", "pt": "Alterar a vari\u00e1vel usada para ordenar as \u00e1reas."},
      "sort_desc_occugrid": {"en": "Changes the variable used to order the donut charts.", "pt": "Alterar a vari\u00e1vel usada para ordenar os gr\u00e1ficos de rosca."},
      
      // Sizing Labels
      "sizing": {"en": "Size", "pt": "Tamanho"},
      "sizing_desc_tree_map": {"en": "Changes the variable used to size the rectangles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos ret\u00e2ngulos."},
      "sizing_desc_stacked": {"en": "Changes the Y axis variable.", "pt": "Alterar a vari\u00e1vel do eixo Y."},
      "sizing_desc_network": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},
      "sizing_desc_compare": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},
      "sizing_desc_occugrid": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},
      "sizing_desc_scatter": {"en": "Changes the variable used to size the circles.", "pt": "Alterar a vari\u00e1vel usada para o tamanho dos c\u00edrculos."},
    
      // Color Labels
      "color_var": {"en": "Color", "pt": "Cor"},
      "color_var_desc_tree_map": {"en": "Changes the variable used to color the rectangles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os ret\u00e2ngulos."},
      "color_var_desc_stacked": {"en": "Changes the variable used to color the areas.", "pt": "Alterar a vari\u00e1vel utilizada para colorir as \u00e1reas."},
      "color_var_desc_geo_map": {"en": "Changes the variable used to color the locations.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os locais."},
      "color_var_desc_network": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_rings": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_compare": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_occugrid": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
      "color_var_desc_scatter": {"en": "Changes the variable used to color the circles.", "pt": "Alterar a vari\u00e1vel utilizada para colorir os c\u00edrculos."},
    
      // Other Control Labels
      "active": {"en": "Available", "pt": "Dispon\u00edvel"},
      "available": {"en": "Available", "pt": "Dispon\u00edvel"},
      "grouping": {"en": "Group", "pt": "Grupo"},
      "grouping_desc_occugrid": {"en": "Groups the donut charts into different categorizations.", "pt": "Agrupar os gr\u00e1ficos de rosca em diferentes categoriza\u00e7\u00f5es."},
      "none": {"en": "None", "pt": "Nenhum"},
      "year": {"en": "Year", "pt": "Ano"},

      // Filter Depths
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
    
      // Calculation Labels
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
      
      "val_usd_growth_pct": {"en": "Annual Growth Rate (1 year)", "pt": "Taxa de Crescimento Anual (1 ano)"},
      "val_usd_growth_pct_5": {"en": "Annual Growth Rate (5 year)", "pt": "Taxa de Crescimento Anual (5 anos)"},
      "val_usd_growth_val": {"en": "Growth Value (1 year)", "pt": "Valor de Crescimento (1 ano)"},
      "val_usd_growth_val_5": {"en": "Growth Value (5 year)", "pt": "Valor de Crescimento (5 anos)"},
      
      "wage_growth_pct": {"en": "Annual Wage Growth Rate (1 year)", "pt": "Taxa de Crescimento dos Sal\u00e1rios Anual (1 ano)"},
      "wage_growth_pct_5": {"en": "Annual Wage Growth Rate (5 year)", "pt": "Taxa de Crescimento dos Sal\u00e1rios Anual (5 anos)"},
      "wage_growth_val": {"en": "Wage Growth Value (1 year)", "pt": "Valor de Crescimento dos Sal\u00e1rios (1 ano)"},
      "wage_growth_val_5": {"en": "Wage Growth Value (5 year)", "pt": "Valor de Crescimento dos Sal\u00e1rios (5 anos)"},
      "num_emp_growth_pct": {"en": "Annual Employee Growth Rate (1 year)", "pt": "Taxa de Crescimento de Empregados Anual (1 ano)"},
      "num_emp_growth_pct_5": {"en": "Annual Employee Growth Rate (5 year)", "pt": "Taxa de Crescimento de Empregados Anual (5 anos)"},
      "num_emp_growth_val": {"en": "Employee Growth (1 year)", "pt": "Crescimento do N\u00famero de Empregados (1 ano)"},
      "num_emp_growth_val_5": {"en": "Employee Growth (5 year)", "pt": "Crescimento do N\u00famero de Empregados (5 anos)"},
    
      // RAIS Labels
      "rais": {"en": "Establishments and Employment (RAIS)", "pt": "Estabelecimentos e Emprego (RAIS)"},
      "num_emp": {"en": "Total Employees", "pt": "Total de Empregados"},
      "num_est": {"en": "Total Establishments", "pt": "Total de Estabelecimentos"},
      "num_emp_est": {"en": "Employees per Establishment", "pt": "Empregados por Estabelecimento"},
      "wage": {"en": "Total Monthly Wages", "pt": "Renda Mensal Total"},
      "total_wage": {"en": "Total Monthly Wage", "pt": "Renda Mensal Total"},
      "wage_avg": {"en": "Average Monthly Wage", "pt": "Renda Mensal M\u00e9dia"},
      "wage_avg_bra": {"en": "Brazilian Average Wage", "pt": "Sal\u00e1rio M\u00e9dio Brasileiro"},
    
      // SECEX Labels
      "secex": {"en": "Product Exports (SECEX)", "pt": "Exporta\u00e7\u00f5es de Produtos (SECEX)"},
      "val_usd": {"en": "Exports", "pt": "Exporta\u00e7\u00f5es"},
      "total_val_usd": {"en": "Total Exports", "pt": "Total de Exporta\u00e7\u00f5es"},
    
      // Key Labels
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

      // Filter Titles
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
    
      // File Types
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
    
      // App Builder
      "basics": {"en": "Basic Values", "pt": "Valores B\u00e1sicos"},
      "growth": {"en": "Growth", "pt": "Crescimento"},
      "calculations": {"en": "Strategic Indicators", "pt": "Indicadores Estrat\u00e9gicos"},
      "Data Provided by": {"en": "Data Provided by", "pt": "Dados Fornecidos por"},
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
    
      // Viz-Whiz Text
      "Click for More Info": {"en": "Click for more data and related apps.", "pt": "Clique para dados adicionais e aplicativos relacionados."},
      "Click to Zoom": {"en": "Click to Zoom", "pt": "Clique para Ampliar"},
      "filter": {"en": "Hide Group", "pt": "Ocultar Grupo"},
      "solo": {"en": "Solo Group", "pt": "S\u00f3 este Grupo"},
      "reset": {"en": "Click to Reset all Filters", "pt": "Clique para Eliminar todos os Filtros"},
      "Primary Connections": {"en": "Primary Connections", "pt": "Conex\u00f5es Prim\u00e1rias"},
    
      // Ask Sabrina
      "Asked": {"en": "Asked", "pt": "Perguntado"},
      "by": {"en": "by", "pt": "por"},
      "point": {"en": "Point", "pt": "Ponto"},
      "points": {"en": "Points", "pt": "Pontos"},
      "reply": {"en": "Reply", "pt": "Resposta"},
      "replies": {"en": "Replies", "pt": "Respostas"},
      "votes": {"en": "Most Active", "pt": "Mais Frequente"},
      "newest": {"en": "Most Recent", "pt": "Mais Recente"},
      "questions": {"en": "Questions", "pt": "Perguntas"},
      "flagged": {"en": "This reply has been flagged.", "pt": "Esta resposta foi marcada."},
      "unflagged": {"en": "This flag on this reply has been removed.", "pt": "A marca desta resposta foi retirada."},
      "voted": {"en": "Your vote has been added.", "pt": "Seu voto foi enviado."},
      "unvoted": {"en": "Your vote was removed.", "pt": "Seu voto foi removido."},
      
      // Admin
      "edit": {"en": "Edit", "pt": "Editar"},
      "visible": {"en": "Visible", "pt": "Vis\u00edvel"},
      "hidden": {"en": "Hidden", "pt": "Oculto"},
      "user": {"en": "User", "pt": "Usu\u00e1rio"},
      "admin": {"en": "Admin", "pt": "Administrador"},
      
      // Selector
      "search": {"en": "Search", "pt": "Pesquisar"},
      "search_results": {"en": "Search Results", "pt": "Resultados da Pesquisa"},
      "select": {"en": "Select", "pt": "Escolher"},
      "show": {"en": "Show", "pt": "Mostrar"},
      "loading_attrs": {"en": "Loading Attribute List", "pt": "Carregando Lista de Atributos"},
      "loading_items": {"en": "Loading More Items", "pt": "Carregar Mais Itens"},
      "wait": {"en": "Please Wait", "pt": "Por favor Aguarde"},
      "back": {"en": "Back", "pt": "Voltar"}
    
    }
    
    if (name.indexOf("_display") >= 0) {
      name = name.split("_")[0]+"_id"
    }
    
    if (!name) return name
    else if (name.indexOf("_stats_") > 0) {
      var n = name.split("_")
      var s = {"en": "Stats", "pt": "Estat\u00edsticas"}
      return n[2]+" "+s[l]+" ("+n[0].toUpperCase()+")"
    }
    else if(labels[name]){
      if (labels[name][l]) return labels[name][l]
      else return name.toTitleCase()
    }
    else if (name.indexOf("total_") == 0) {
      label_name = name.substr(6)
      if (labels[label_name][l]) return labels[label_name][l]
      else return name.toTitleCase()
    }
    else if (name.indexOf("population_") == 0) {
      year = name.split("_")[1]
      if (labels["population"][l]) return labels["population"][l] + " ("+year+")"
      else return name.toTitleCase() + " ("+year+")"
    }
    else return name.toTitleCase()
  
  }
  
}

dataviva.format.number = function(value,name,l) {
  
  if (!l) var l = dataviva.language
  
  var negative = value < 0
  value = Math.abs(value)
  
  if (name.indexOf("_growth_pct") >= 0) value = value * 100
  
  var smalls = ["rca","rca_bra","rca_wld","distance","eci","pci","bra_diversity_eff","isic_diversity_eff","cbo_diversity_eff","hs_diversity_eff","wld_diversity_eff"]

  var ids = ["cbo_id","isic_id","wld_id","hs_id","bra_id","id_ibge"]
  if (ids.indexOf(name) >= 0) return value.toString().toUpperCase()
  else if (name == "year") {
    var return_value = value
  }
  else if (smalls.indexOf(name) >= 0 || value < 1) {
    var r = value.toString().split(""), l = false
    r.forEach(function(n,i){
      if (n != "0" && n != "." && !l) l = i
    })
    if (l > 5) l = 5
    var return_value = d3.round(value,l)
    
  }
  else if (value.toString().split(".")[0].length > 4) {
    
    var symbol = d3.formatPrefix(value).symbol
    symbol = symbol.replace("G", "B") // d3 uses G for giga
    
    // Format number to precision level using proper scale
    value = d3.formatPrefix(value).scale(value)
    value = parseFloat(d3.format(".3g")(value))
    
    if (symbol && l == "pt") {
      var digit = parseFloat(value.toString().split(".")[0])
      if (symbol == "T") {
        if (digit < 2) symbol = "Trilh\u00e3o"
        else symbol = "Trilh\u00f5es"
      }
      else if (symbol == "B") {
        if (digit < 2) symbol = "Bilh\u00e3o"
        else symbol = "Bilh\u00f5es"
      }
      else if (symbol == "M") {
        if (digit < 2) symbol = "Milh\u00e3o"
        else symbol = "Milh\u00f5es"
      }
      else if (symbol == "k") {
        if (digit < 2) symbol = "Milhares"
        else symbol = "Mil"
      }
    }
    if (symbol) symbol = " "+symbol
    
    var return_value = value + symbol;
  }
  else if (name == "share") {
    var return_value = d3.format(".2f")(value)
  }
  else {
    var return_value = d3.format(",f")(value)
  }
  
  var total_labels = {
        "val_usd": ["$"," USD"],
        "wage": ["$"," BRL"],
        "wage_avg": ["$"," BRL"],
        "wage_avg_bra": ["$"," BRL"],
        "wage_growth_val": ["$"," BRL"],
        "wage_growth_val_5": ["$"," BRL"],
        "val_usd_growth_pct": ["","%"],
        "val_usd_growth_pct_5": ["","%"],
        "val_usd_growth_val": ["$"," USD"],
        "val_usd_growth_val_5": ["$"," USD"],
        "num_emp_growth_pct": ["","%"],
        "num_emp_growth_pct_5": ["","%"],
        "wage_growth_pct": ["","%"],
        "wage_growth_pct_5": ["","%"]
      }
      
  if (name.indexOf("total_") == 0) {
    var label_name = name.substr(6)
  }
  else if (name.indexOf("cp_bra_") == 0) {
    var label_name = name.substr(9)
  }
  else var label_name = name
  
  if (total_labels[label_name]) {
    var labels = total_labels[label_name]
    return_value = labels[0] + return_value + labels[1]
  }
  
  return_value = String(return_value)
  
  if (l == "pt") {
    var n = return_value.split(".")
    n[0] = n[0].replace(",",".")
    return_value = n.join(",")
  }
  
  if (negative) return_value = "-"+return_value
  
  return return_value
  
}

dataviva.ui = {}

dataviva.ui.background = function() {
  var fs = d3.select("#fullscreen")
  if (fs.node()) {
    // var hour = new Date().getHours()
    // if (hour >= 5 && hour <= 20) {
    //   var filename = "day"
    // }
    // else {
    //   var filename = "night"
    // }
    var filename = "city"
    fs.style("background-image","url('/static/img/bgs/"+filename+".jpg')")
    
    resizebg = function() {
      var w = window.innerWidth, 
          h = window.innerHeight,
          aspect = w/h
          
      if (aspect > 1.5) {
        fs.style("background-size",w+"px "+(w/1.5)+"px")
      }
      else {
        fs.style("background-size",(h*1.5)+"px "+h+"px")
      }
    }
    
    resizebg()
    
    window.onresize = resizebg
    
  }
}

dataviva.ui.tooltip = function(id,obj,align) {
  if (obj) {
    
    var size = obj.getBoundingClientRect(),
        text = obj.getAttribute("alt") ? obj.getAttribute("alt") : id
        
    if (!align) var align = "bottom center"
    
    var t = align.split(" ")[0]
    if (t == "center") var offset = size.width/2
    else var offset = size.height/2
        
    d3plus.tooltip.remove(id);
    d3plus.tooltip.create({
      "x": size.left+size.width/2,
      "y": size.top+size.height/2,
      "offset": offset,
      "arrow": true,
      "description": text,
      "width": "auto",
      "id": id,
      "align": align,
      "max_width": 180
    })
    
  }
  else {
    d3plus.tooltip.remove(id);
  }
}

dataviva.ui.loading = function(parent) {
  
  var self = this
  
  this.div = d3.select(parent).append("div")
    .attr("class","loading")
    
  this.icon = self.div.append("i")
    .attr("class","fa fa-certificate")
    
  this.words = self.div.append("div")
    .attr("class","text")
    
  this.timing = parseFloat(self.div.style("transition-duration"),10)*1000
    
  this.show = function(callback) {
    
    self.div.style("display","block")
    
    setTimeout(function(){
      
      self.div.style("opacity",1)
      
      if (callback) {
        setTimeout(callback,self.timing)
      }
      
    },5)
      
    return self
  }
    
  this.hide = function() {
    
    self.div.style("opacity",0)
    
    setTimeout(function(){
      self.div.style("display","none")
    },self.timing)
    
    return self
      
  }
    
  this.text = function(text) {
    self.words.html(text)
    return self
  }
    
  this.color = function(color) {
    self.div.style("background-color",color)
    return self
  }
  
  if (!Modernizr.cssanimations) {
    var elem = this.icon.node(), degree = 0, timer;
    function rotate() { 
      if (degree == 360) degree = 0
      elem.style.msTransform = 'rotate(' + degree + 'deg)'
      elem.style.transform = 'rotate(' + degree + 'deg)'
      // timeout increase degrees:
      timer = setTimeout(function() {
        degree = degree + 4;
        rotate(); // loop it
      },20);
    }

    rotate();
  }

  return this
  
}

// Returns a random number between the min and max passed to the function
dataviva.random = function(min,max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

dataviva.displayID = function(id,type) {
  
  function romanize (num) {
      if (!+num)
          return false;
      var digits = String(+num).split(""),
          key = ["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM",
                 "","X","XX","XXX","XL","L","LX","LXX","LXXX","XC",
                 "","I","II","III","IV","V","VI","VII","VIII","IX"],
          roman = "",
          i = 3;
      while (i--)
          roman = (key[+digits.pop() + (i * 10)] || "") + roman;
      return Array(+digits.join("") + 1).join("M") + roman;
  }

  if (id) {
    if (["hs","wld"].indexOf(type) >= 0 && id.length > 2) {
      return id.slice(2).toUpperCase();
    }
    else if (["hs"].indexOf(type) >= 0) {
      return romanize(parseFloat(id));
    }
    else if (["isic"].indexOf(type) >= 0 && id.length > 1) return id.slice(1);
    else return id.toUpperCase();
  }
  else {
    return id;
  }
  
}

dataviva.icon = function(id,type,color) {
  
  if (["isic","cbo","hs","bra"].indexOf(type) >= 0 && id != "all"){
    var depth = dataviva.depths(type)[0],
        id = id.slice(0,depth);
  }
  else {
    var id = id;
  }
  
  if (type != "bra" && id == "all" && color == "#ffffff") {
    id = id+"_black"
  }
  
  return "/static/img/icons/"+type+"/"+type+"_"+id+".png";
  
}

dataviva.depths = function(type,flatten) {
  if (type == "isic") var array = [1,3,5];
  else if (type == "cbo") var array = [1,2,4];
  else if (type == "hs") var array = [2,4,6];
  else if (type == "bra") var array = [2,4,8];
  else if (type == "wld") var array = [2,5];
  else var array = [0];
  
  if (flatten && array.length > 1) {
    return [array[0],array[array.length-1]];
  }
  else {
    return array;
  }
  
}

dataviva.popover.create = function(params) {
  
  var id = params.id ? params.id : "popover",
      pop_width = params.width ? params.width : "50%",
      pop_height = params.height ? params.height : "50%",
      close = params.close ? params.close : true,
      color = params.color ? params.color : "#af1f24"
  
  document.onkeyup = function(e) {
    if (e.keyCode == 27) { dataviva.popover.hide(); }   // esc
  };
  
  if (typeof pop_width == "string") {
    if (pop_width.indexOf("%") > 0) {
      var w_px = (parseFloat(pop_width,10)/100)*window.innerWidth
    }
    else {
      var w_px = parseFloat(pop_width,10)
    }
  }
  else {
    var w_px = pop_width;
  }
  
  if (typeof pop_height == "string") {
    if (pop_height.indexOf("%") > 0) {
      var h_px = (parseFloat(pop_height,10)/100)*window.innerHeight
    }
    else {
      var h_px = parseFloat(pop_height,10)
    }
  }
  else {
    var h_px = pop_height;
  }
  
  var body = d3.select("body").append("div")
    .attr("id",id)
    .attr("class","popover")
    .style("width",w_px+"px")
    .style("height",h_px+"px")
    .style("margin-left",-w_px/2+"px")
    .style("margin-top",-h_px/2+"px")
    
  if (close) {
    body.append("div")
      .attr("class","d3plus_tooltip_close")
      .html("\&times;")
      .style("background-color",color)
      .on(d3plus.evt.click,function(){
        dataviva.popover.hide("#"+id);
      })
  }
  
}

dataviva.popover.show = function(id) {
  
  if (d3.select("#popover_mask").empty()) {
    d3.select("body").append("div")
      .attr("id","popover_mask")
      .on(d3plus.evt.click,function(){
        dataviva.popover.hide();
      })
  }
  
  d3.select("#popover_mask")
    .style("display","block")
    
  d3.select(id)
    .style("display","block")
  
  if (Modernizr.cssanimations) {
    setTimeout(function(){
      show()
    },5)
  }
  else {
    show()
  }
  
  function show() {
    d3.select("#popover_mask")
      .style("opacity",0.8)
    
    d3.select(id)
      .style("opacity",1)
  }
  
}

dataviva.popover.hide = function(id) {
  
  if (id) var popover = d3.select(id)
  else var popover = d3.selectAll(".popover")

  popover.each(function(){
    
      if (d3.select(this).style("display") != "none") {
        
        var p = d3.select(this)

        d3.select("#popover_mask").style("opacity",0);
        p.style("opacity",0);
        
        if (Modernizr.cssanimations) {
          var timing = parseFloat(p.style("transition-duration"),10)*1000
        
          setTimeout(function(){
            hide()
          },timing)
        }
        else {
          hide()
        }
  
        function hide() {
          p.style("display","none")
          d3.select("#popover_mask").style("display","none")
        }
        
      }
      
    })

}

dataviva.flash = function(text) {
	
	d3.selectAll("#server_message").remove();
	
	flash_cont = d3.select("#container").insert("div", ":first-child")
	
	flash_inner = flash_cont.attr("id", "server_message")
					.append("div")
					.attr("class", "decision")
					.text(text)
	
	flash_inner.append("i")
		.attr("id", "close_message")
		.attr("class", "fa fa-times-circle")
		.on(d3plus.evt.click, function(d){
	        var div = d3.select("#server_message")
	        var timing = parseFloat(div.style("transition-duration"),10)*1000;
	        div.style("opacity",0);
	        setTimeout(function(){
	          div.remove();
	        },timing)
		})
}

dataviva.url = function(url,args,title) {
  
  var replace = window.location.pathname.indexOf(url.split("?")[0]) >= 0
  var iframe = window != window.parent
  var app_embed = window.location.pathname.indexOf("apps/embed") >= 0
  var app_builder = window.parent.location.pathname.indexOf("apps/builder") >= 0
  var data_table = window.location.pathname.indexOf("data/table") >= 0
  var rankings = window.location.pathname.indexOf("rankings") >= 0
  
  if (title) document.title = "DataViva : "+title

  var params = ""
  if (args && typeof args === "string") {
    params = args
  }
  else if (args && Object.keys(args).length > 0) {
    var url_vars = []
    for (v in args) {
      if (args[v] != "" && (!app_embed || (app_embed && (v != "controls" || (v == "controls" && args.builder != "false"))))) {
        url_vars.push(v + "=" + args[v])
      }
    }
    params += url_vars.join("&");
    if (params.length) params = "?"+params
  }
  var full_url = url+params
  
  if (Modernizr.history) {
    if (replace || iframe) {
      window.history.replaceState({'prev_request': full_url}, title, full_url)
    }
    else {
      window.history.pushState({'prev_request': full_url}, title, full_url)
    }
    
    if (iframe) {
      
      if (title) window.parent.document.title = "DataViva : "+title
  
      if (app_builder) {
        var parent_url = full_url.replace("embed","builder")
      }
      else if (data_table || rankings) {
        var parent_url = full_url.replace("table/","")
      }
      if (replace) {
        window.parent.history.replaceState({'prev_request': parent_url}, title, parent_url)
      }
      else {
        window.parent.history.pushState({'prev_request': parent_url}, title, parent_url)
      }
    }
  } 
  else if (!replace) {
    if (app_builder) {
      full_url = full_url.replace("embed","builder")
      window.parent.location = full_url
    }
    else {
      window.location = full_url
    }
    
  }
}
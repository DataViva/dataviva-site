//////////////////////////////////////////////////////////////
// GLOBAL LOADING BAR                                       //
// Call .update(counter) to update the width and percentage //
//////////////////////////////////////////////////////////////

function loader() {
  
  var load_div, load_text = "Querying Database"

  function draw(selection) {
    selection.each(function() {
      load_div = d3.select(this).append("div").attr("id","loader")
      load_div.append("div").attr("id","bar_bg")
        .append("div").attr("id","bar_percent").style("width","0%")
      load_div.append("div").attr("id","load_percent").text(load_text)
    })
  }
  
  draw.percentage = function(value) {
    load_div.select("#bar_percent").style("width",value+"%")
    load_div.select("#load_percent").text(load_text+" "+ value+"%")
  }
  
  draw.text = function(value) {
    load_text = value
  }
  
  return draw
}

////////////////////////////////////////////////////////////////////////////////
// GLOBAL NAME FORMATTER                                                      
// Inputs: the name to be formatted
////////////////////////////////////////////////////////////////////////////////

function format_name(name) {
  
  var labels = {
    
    // App Titles
    "compare": {"en": "Compare", "pt": "Comparar"},
    "occugrid": {"en": "Occugrid", "pt": "Occugrid"},
    "geo_map": {"en": "Geo Map", "pt": "Mapa"},
    "network": {"en": "Network", "pt": "Rede"},
    "rings": {"en": "Rings", "pt": "An\u00e9is"},
    "scatter": {"en": "Scatter", "pt": "Espalhar"},
    "stacked": {"en": "Stacked", "pt": "Empilhados"},
    "tree_map": {"en": "Tree Map", "pt": "\u00c1rvore Mapa"},

    // Stacked Area Sorting/Order
    "order": {"en": "Order", "pt": "Ordem"},
    "asc": {"en": "Ascending", "pt": "Ascendente"},
    "desc": {"en": "Descending", "pt": "Descendente"},
    
    // Stacked Area Layout Type
    "layout": {"en": "Layout", "pt": "Tra\u00e7ado"},
    "value": {"en": "Value", "pt": "Valor"},
    "share": {"en": "Market Share", "pt": "Fatia de Mercado"},
    
    // RCA Scope Toggle
    "rca_scope": {"en": "RCA Scope", "pt": "\u00c2mbito RCA"},
    "bra_rca": {"en": "Domestic", "pt": "Dom\u0089stico"},
    "wld_rca": {"en": "International", "pt": "Internacional"},

    // Spotlight Toggle
    "spotlight": {"en": "Spotlight", "pt": "Holofote"},
    "true": {"en": "On", "pt": "Em"},
    "false": {"en": "Off", "pt": "Fora"},
    
    // Other Control Labels
    "active": {"en": "Available", "pt": "Dispon\u00edvel"},
    "available": {"en": "Available", "pt": "Dispon\u00edvel"},
    "color_var": {"en": "Color", "pt": "Cor"},
    "grouping": {"en": "Group", "pt": "Grupo"},
    "none": {"en": "None", "pt": "Nenhum"},
    "sizing": {"en": "Size", "pt": "Tamanho"},
    "sorting": {"en": "Sort", "pt": "Tipo"},
    "total": {"en": "Required", "pt": "Exigido"},
    "year": {"en": "Year", "pt": "Ano"},

    // Filter Depths
    "depth": {"en": "Depth", "pt": "Fundo"},
    "bra_2": {"en": "State", "pt": "Estado"},
    "bra_4": {"en": "Mesoregion", "pt": "Mesorregi\u00e3o"},
    "bra_6": {"en": "Microregion", "pt": "Microregi\u00e3o"},
    "bra_8": {"en": "Municipality", "pt": "Municipalidade"},
    "cbo_1": {"en": "Category", "pt": "Categoria"},
    "cbo_2": {"en": "2 Digit", "pt": "2 D\u00edgito"},
    "cbo_3": {"en": "3 Digit", "pt": "3 D\u00edgito"},
    "cbo_4": {"en": "4 Digit", "pt": "4 D\u00edgito"},
    "cbo_6": {"en": "6 Digit", "pt": "4 D\u00edgito"},
    "isic_1": {"en": "Category", "pt": "Categoria"},
    "isic_3": {"en": "2 Digit", "pt": "2 D\u00edgito"},
    "isic_4": {"en": "3 Digit", "pt": "3 D\u00edgito"},
    "isic_5": {"en": "4 Digit", "pt": "4 D\u00edgito"},
    "hs_2": {"en": "Category", "pt": "Categoria"},
    "hs_4": {"en": "HS2", "pt": "HS2"},
    "hs_6": {"en": "HS4", "pt": "HS4"},
    "hs_8": {"en": "HS6", "pt": "HS6"},
    "wld_2": {"en": "Continent", "pt": "Continente"},
    "wld_5": {"en": "Country", "pt": "Pa\u00eds"},
    "bra_2_plural": {"en": "States", "pt": "Estado"},
    "bra_4_plural": {"en": "Mesoregions", "pt": "Mesorregi\u00e3o"},
    "bra_6_plural": {"en": "Microregions", "pt": "Microregi\u00e3o"},
    "bra_8_plural": {"en": "Municipalities", "pt": "Municipalidade"},
    "cbo_1_plural": {"en": "Categories", "pt": "Categoria"},
    "cbo_2_plural": {"en": "2 Digit", "pt": "2 D\u00edgito"},
    "cbo_3_plural": {"en": "3 Digit", "pt": "3 D\u00edgito"},
    "cbo_4_plural": {"en": "4 Digit", "pt": "4 D\u00edgito"},
    "cbo_6_plural": {"en": "6 Digit", "pt": "4 D\u00edgito"},
    "isic_1_plural": {"en": "Categories", "pt": "Categoria"},
    "isic_3_plural": {"en": "2 Digit", "pt": "2 D\u00edgito"},
    "isic_4_plural": {"en": "3 Digit", "pt": "3 D\u00edgito"},
    "isic_5_plural": {"en": "4 Digit", "pt": "4 D\u00edgito"},
    "hs_2_plural": {"en": "Categories", "pt": "Categoria"},
    "hs_4_plural": {"en": "HS2", "pt": "HS2"},
    "hs_6_plural": {"en": "HS4", "pt": "HS4"},
    "hs_8_plural": {"en": "HS6", "pt": "HS6"},
    "wld_2_plural": {"en": "Continents", "pt": "Continente"},
    "wld_5_plural": {"en": "Countries", "pt": "Pa\u00eds"},
    
    // Calculation Labels
    "complexity": {"en": "Complexity", "pt": "Complexidade"},
    "distance": {"en": "Distance", "pt": "Dist\u00e2ncia"},
    "employed": {"en": "Employed", "pt": "Empregada"},
    "importance": {"en": "Exclusivity", "pt": "Exclusividade"},
    "growth_val": {"en": "Wage Growth", "pt": "Crescimento dos Sal\u00e1rios"},
    "growth_val_total": {"en": "Cumulative Wage Growth", "pt": "Crescimento Salarial Acumulada"},
    "opp_gain": {"en": "Opportunity Gain", "pt": "Ganho Oportunidade"},
    "proximity": {"en": "Proximity", "pt": "Proximidade"},
    "rca": {"en": "Domestic RCA", "pt": "Interno RCA"},
    "rca_wld": {"en": "International RCA", "pt": "Internacional RCA"},
    
    // RAIS Labels
    "rais": {"en": "Establishments and Employment (RAIS)", "pt": "Estabelecimentos e Emprego (RAIS)"},
    "num_emp": {"en": "Employees", "pt": "Funcion\u00e1rios"},
    "num_est": {"en": "Establishments", "pt": "Estabelecimentos"},
    "required_wage_avg": {"en": "Average Monthly Wage", "pt": "Sal\u00e1rio M\u00e9dio Mensal"},
    "wage": {"en": "Monthly Wage", "pt": "Sal\u00e1rios Mensal"},
    "wage_avg": {"en": "Average Monthly Wage", "pt": "Sal\u00e1rio M\u00e9dio Mensal"},
    
    // SECEX Labels
    "secex": {"en": "Product Exports (SECEX)", "pt": "Exporta\u00e7\u00e3es de Produtos (SECEX)"},
    "val_usd": {"en": "Export Value", "pt": "O valor das exporta\u00e7\u00e3es"},
    
    // Key Labels
    "brazil": {"en": "Brazil", "pt": "Brasil"},
    "bra_id": {"en": "BRA ID", "pt": "BRA ID"},
    "category": {"en": "Category", "pt": "Categoria"},
    "cbo_id": {"en": "CBO ID", "pt": "CBO ID"},
    "color": {"en": "Color", "pt": "Cor"},
    "display_id": {"en": "ID", "pt": "ID"},
    "hs_id": {"en": "HS ID", "pt": "HS ID"},
    "id_ibge": {"en": "IBGE ID", "pt": "IBGE ID"},
    "id": {"en": "ID", "pt": "ID"},
    "isic_id": {"en": "ISIC ID", "pt": "ISIC ID"},
    "name": {"en": "Name", "pt": "Nome"},
    "name_en": {"en": "Name (English)", "pt": "Nome"},
    "name_pt": {"en": "Name (Portuguese)", "pt": "Nome"},
    "wld_id": {"en": "WLD ID", "pt": "WLD ID"},

    // Filter Titles
    "bra": {"en": "Location", "pt": "Localiza\u00e7\u00e3o"},
    "bra_plural": {"en": "Locations", "pt": "Locais"},
    "cbo": {"en": "Occupation", "pt": "Ocupa\u00e7\u00e3o"},
    "cbo_plural": {"en": "Occupations", "pt": "Ocupa\u00e7\u00e3o"},
    "hs": {"en": "Product Export", "pt": "Produto"},
    "hs_plural": {"en": "Product Exports", "pt": "Produto"},
    "icon": {"en": "Icon", "pt": "Imagem"},
    "isic": {"en": "Industry", "pt": "Atividade Econ\u00f4mica"},
    "isic_plural": {"en": "Industries", "pt": "Actividades Econ\u00f3micas"},
    "wld": {"en": "Trade Partner", "pt": "Parceiro Comercial"},
    "wld_plural": {"en": "Trade Partners", "pt": "Parceiro Comercial"},
    
    // File Types
    "download": {"en": "Download", "pt": "Baixar"},
    "csv": {"en": "Save as CSV", "pt": "Salvar como CSV"},
    "pdf": {"en": "Save as PDF", "pt": "Salvar como PDF"},
    "png": {"en": "Save as PNG", "pt": "Salvar como PNG"},
    "svg": {"en": "Save as SVG", "pt": "Salvar como SVG"},
    
    // App Builder Footer
    "Data Provided by": {"en": "Data Provided by", "pt": "Dados fornecidos pela"},
    
    // Viz-Whiz Text
    "Click for More Info": {"en": "Click for more data and related apps.", "pt": "Clique para obter mais dados e aplicativos relacionados."},
    "Click to Zoom": {"en": "Click to Zoom", "pt": "Clique para Ampliar"},
    
    // Ask Sabrina
    "Asked by": {"en": "Asked by", "pt": "Perguntado por"},
    "points": {"en": "Points", "pt": "Pontos"}
    
  }
  
  if (!name) return name;
  else if(labels[name]){
    if (labels[name][visual.language]) return labels[name][visual.language];
    else return name.toTitleCase();
  } 
  else return name.toTitleCase();
  
};

String.prototype.toTitleCase = function () {
  var smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|of|on|or|that|the|to|which|with|vs?\.?|via)$/i;

  return this.replace(/([^\W_]+[^\s-]*) */g, function (match, p1, index, title) {
    if (index > 0 && index + p1.length !== title.length &&
      p1.search(smallWords) > -1 && title.charAt(index - 2) !== ":" && 
      title.charAt(index - 1).search(/[^\s-]/) < 0) {
      return match.toLowerCase();
    }

    return match.charAt(0).toUpperCase() + match.substr(1).toLowerCase();
  });
};

String.prototype.removeAccents = function() {
  var diacritics = [
      [/[\300-\306]/g, 'A'],
      [/[\340-\346]/g, 'a'],
      [/[\310-\313]/g, 'E'],
      [/[\350-\353]/g, 'e'],
      [/[\314-\317]/g, 'I'],
      [/[\354-\357]/g, 'i'],
      [/[\322-\330]/g, 'O'],
      [/[\362-\370]/g, 'o'],
      [/[\331-\334]/g, 'U'],
      [/[\371-\374]/g, 'u'],
      [/[\321]/g, 'N'],
      [/[\361]/g, 'n'],
      [/[\307]/g, 'C'],
      [/[\347]/g, 'c'],
  ];
  var s = this;
  for (var i = 0; i < diacritics.length; i++) {
      s = s.replace(diacritics[i][0], diacritics[i][1]);
  }
  return s;
};

String.prototype.truncate = function(n){
  var tooLong = this.length > n,
      string = tooLong ? this.substr(0,n-1) : this;
  string = tooLong ? string.substr(0,string.lastIndexOf(' ')) : string;
  return  tooLong ? string + '...' : string;
};
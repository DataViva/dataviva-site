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

//////////////////////////////////////////////////////////////
// GLOBAL NO DATA THING
//
//////////////////////////////////////////////////////////////

function no_data() {

  function draw(selection) {
    selection.each(function(title) {
      
      var error = d3.select(this).append("div")
        .attr("id","error")
        
      error.append("div")
        .attr("id","title")
        .html(title)
        
      error.append("div")
        .attr("id","sub_title")
        .html("Please modify your search filters")
        
    })
  }
  
  return draw
  
}

////////////////////////////////////////////////////////////////////////////////
// GLOBAL NAME FORMATTER                                                      
// Inputs: the name to be formatted
////////////////////////////////////////////////////////////////////////////////

function format_name(name, l) {
  
  var labels = {
    "active": {"en": "Available", "pt": "Dispon\u00edvel"},
    "asc": {"en": "Ascending", "pt": "Ascendente"},
    "available": {"en": "Available", "pt": "Dispon\u00edvel"},
    "bra": {"en": "Location", "pt": "Localiza\u00e7\u00e3o"},
    "bra_id": {"en": "Location", "pt": "Localiza\u00e7\u00e3o"},
    "bra_plural": {"en": "Locations", "pt": "Locais"},
    "bra_rca": {"en": "Domestic", "pt": "Dom\u0089stico"},
    "brazil": {"en": "Brazil", "pt": "Brasil"},
    "category": {"en": "Category", "pt": "Categoria"},
    "color": {"en": "Color", "pt": "Cor"},
    "cbo": {"en": "Occupation", "pt": "Ocupa\u00e7\u00e3o"},
    "cbo_id": {"en": "Occupation", "pt": "Ocupa\u00e7\u00e3o"},
    "cbo_plural": {"en": "Occupations", "pt": "Ocupa\u00e7\u00e3o"},
    "complexity": {"en": "Complexity", "pt": "Complexidade"},
    "csv": {"en": "Save as CSV", "pt": "Salvar como CSV"},
    "desc": {"en": "Descending", "pt": "Descendente"},
    "display_id": {"en": "ID", "pt": "ID"},
    "distance": {"en": "Distance", "pt": "Dist\u00e2ncia"},
    "download": {"en": "Download", "pt": "Baixar"},
    "employed": {"en": "Employed", "pt": "Empregada"},
    "false": {"en": "Off", "pt": "Fora"},
    "grouping": {"en": "Group", "pt": "Grupo"},
    "growth_pct_total": {"en": "Growth %", "pt": "% de Crescimento"},
    "hs": {"en": "Product Export", "pt": "Produto"},
    "hs_id": {"en": "Product Export", "pt": "Produto"},
    "hs_plural": {"en": "Product Exports", "pt": "Produto"},
    "importance": {"en": "Exclusivity", "pt": "Exclusividade"},
    "isic": {"en": "Local Industry", "pt": "Ind\u00fastria"},
    "isic_id": {"en": "Local Industry", "pt": "Ind\u00fastria"},
    "isic_plural": {"en": "Local Industries", "pt": "Ind\u00fastria"},
    "layout": {"en": "Layout", "pt": "Tra\u00e7ado"},
    "secex": {"en": "Product Exports", "pt": "Exporta\u00e7\u00e3es"},
    "rais": {"en": "Local Industries", "pt": "Ind\u00fastrias"},
    "name": {"en": "Name", "pt": "Nome"},
    "nesting": {"en": "Depth", "pt": "Profundidade"},
    "none": {"en": "None", "pt": "Nenhum"},
    "num_emp": {"en": "Employees", "pt": "Funcion\u00e1rios"},
    "num_est": {"en": "Establishments", "pt": "Estabelecimentos"},
    "opp_gain": {"en": "Opportunity Gain", "pt": "Ganho oportunidade"},
    "order": {"en": "Order", "pt": "Ordem"},
    "pdf": {"en": "Save as PDF", "pt": "Salvar como PDF"},
    "png": {"en": "Save as PNG", "pt": "Salvar como PNG"},
    "proximity": {"en": "Proximity", "pt": "Proximidade"},
    "total": {"en": "Required", "pt": "Exigido"},
    "rca": {"en": "Domestic RCA", "pt": "Interno RCA"},
    "rca_max": {"en": "RCA >= 1", "pt": "RCA >= 1"},
    "rca_min": {"en": "RCA < 1", "pt": "RCA < 1"},
    "rca_scope": {"en": "RCA Scope", "pt": "\u00c2mbito RCA"},
    "rca_wld": {"en": "International RCA", "pt": "Internacional RCA"},
    "required_wage_avg": {"en": "Average Monthly Wage", "pt": "Sal\u00e1rio M\u00e9dio Mensal"},
    "share": {"en": "Market Share", "pt": "Fatia de mercado"},
    "sizing": {"en": "Size", "pt": "Tamanho"},
    "sorting": {"en": "Sort", "pt": "Tipo"},
    "spotlight": {"en": "Spotlight", "pt": "Holofote"},
    "svg": {"en": "Save as SVG", "pt": "Salvar como SVG"},
    "total_num_emp": {"en": "Employees", "pt": "Funcion\u00e1rios"},
    "total_num_est": {"en": "Establishments", "pt": "Estabelecimentos"},
    "total_val_kg": {"en": "Weight", "pt": "Peso"},
    "total_val_quantity": {"en": "Units", "pt": "Unidades"},
    "total_val_usd": {"en": "Value", "pt": "Valor"},
    "total_wage": {"en": "Monthly Wage", "pt": "Sal\u00e1rios Mensal"},
    "true": {"en": "On", "pt": "Em"},
    "val_kg": {"en": "Weight", "pt": "Peso"},
    "val_quantity": {"en": "Units", "pt": "Unidades"},
    "val_usd": {"en": "Export Value", "pt": "O valor das exporta\u00e7\u00e3es"},
    "value": {"en": "Value", "pt": "Valor"},
    "wage": {"en": "Monthly Wage", "pt": "Sal\u00e1rios Mensal"},
    "wage_avg": {"en": "Average Monthly Wage", "pt": "Sal\u00e1rio M\u00e9dio Mensal"},
    "wld": {"en": "Trade Partner", "pt": "Parceiro Comercial"},
    "wld_id": {"en": "Trade Partner", "pt": "Parceiro Comercial"},
    "wld_plural": {"en": "Trade Partners", "pt": "Parceiro Comercial"},
    "wld_rca": {"en": "International", "pt": "Internacional"},
    "year": {"en": "Year", "pt": "Ano"},
    
    "bubbles": {"en": "Occugrid", "pt": "Occugrid"},
    "geo_map": {"en": "Geo Map", "pt": "Mapa"},
    "network": {"en": "Network", "pt": "Network"},
    "pie_scatter": {"en": "Scatter Plot", "pt": "Dispers\u00e3o"},
    "rings": {"en": "Rings", "pt": "An\u00e9is"},
    "stacked": {"en": "Stacked", "pt": "Stacked"},
    "tree_map": {"en": "Tree Map", "pt": "Tree Map"},

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
    
    
    "network-rais-isic": {"en": "Industry Space", "pt": "Industry Space"},
    "network-rais-cbo": {"en": "Occupation Space", "pt": "Occupation Space"},
    "network-secex-hs": {"en": "Product Space", "pt": "Product Space"},
    
    "rings-rais-isic-isic": {"en": "Industry Connections", "pt": "Industry Connections"},
    "rings-rais-cbo-cbo": {"en": "Occupation Connections", "pt": "Occupation Connections"},
    "rings-secex-hs-hs": {"en": "Product Connections", "pt": "Product Connections"},
    
    "bubbles-rais-cbo-isic": {"en": "Occupations Required for an Industry", "pt": "Occupations Required for an Industry"},
    
    "pie_scatter-secex-hs": {"en": "Product Distance and Complexity", "pt": "Product Distance and Complexity"},
    "pie_scatter-secex-hs-wld": {"en": "Product Distance and Complexity with Trade Partner", "pt": "Product Distance and Complexity with Trade Partner"},
    "pie_scatter-rais-isic": {"en": "Industry Distance and Complexity", "pt": "Industry Distance and Complexity"},
    "pie_scatter-rais-isic-cbo": {"en": "Industry Distance and Complexity with Occupation", "pt": "Industry Distance and Complexity with Occupation"},
    
    "stacked-secex-hs": {"en": "Exports", "pt": "Exports"},
    "stacked-secex-hs-wld": {"en": "Exports with Trade Partner", "pt": "Exports with Trade Partner"},
    "stacked-secex-wld": {"en": "Trade Partners", "pt": "Trade Partners"},
    "stacked-secex-wld-hs": {"en": "Trade Partners with Product", "pt": "Trade Partners with Product"},
    "stacked-secex-bra": {"en": "Export Origins", "pt": "Export Origins"},
    "stacked-secex-bra-hs": {"en": "Export Origin of Product", "pt": "Export Origin of Product"},
    "stacked-secex-bra-hs-wld": {"en": "Export Origin of Product with Trade Partner", "pt": "Export Origin of Product with Trade Partner"},
    "stacked-rais-isic": {"en": "Industries", "pt": "Industries"},
    "stacked-rais-isic-cbo": {"en": "Industries with Occupation", "pt": "Industries with Occupation"},
    "stacked-rais-cbo": {"en": "Occupations", "pt": "Occupations"},
    "stacked-rais-cbo-isic": {"en": "Industry Employees", "pt": "Industry Employees"},
    "stacked-rais-bra": {"en": "Industry Locations", "pt": "Industry Locations"},
    "stacked-rais-bra-isic": {"en": "Locations with specific Industry", "pt": "Locations with specific Industry"},
    "stacked-rais-bra-cbo": {"en": "Locations with specific Occupation", "pt": "Locations with specific Occupation"},
    "stacked-rais-bra-isic-cbo": {"en": "Locations with specific Occupation in Industry", "pt": "Locations with specific Occupation in Industry"},
    
    "tree_map-secex-hs": {"en": "Exports", "pt": "Exports"},
    "tree_map-secex-hs-wld": {"en": "Exports with Trade Partner", "pt": "Exports with Trade Partner"},
    "tree_map-secex-wld": {"en": "Trade Partners", "pt": "Trade Partners"},
    "tree_map-secex-wld-hs": {"en": "Trade Partners with Product", "pt": "Trade Partners with Product"},
    "tree_map-secex-bra": {"en": "Export Origins", "pt": "Export Origins"},
    "tree_map-secex-bra-hs": {"en": "Export Origin of Product", "pt": "Export Origin of Product"},
    "tree_map-secex-bra-hs-wld": {"en": "Export Origin of Product with Trade Partner", "pt": "Export Origin of Product with Trade Partner"},
    "tree_map-rais-isic": {"en": "Industries", "pt": "Industries"},
    "tree_map-rais-isic-cbo": {"en": "Industries with Occupation", "pt": "Industries with Occupation"},
    "tree_map-rais-cbo": {"en": "Occupations", "pt": "Occupations"},
    "tree_map-rais-cbo-isic": {"en": "Industry Employees", "pt": "Industry Employees"},
    "tree_map-rais-bra": {"en": "Industry Locations", "pt": "Industry Locations"},
    "tree_map-rais-bra-isic": {"en": "Locations with specific Industry", "pt": "Locations with specific Industry"},
    "tree_map-rais-bra-cbo": {"en": "Locations with specific Occupation", "pt": "Locations with specific Occupation"},
    "tree_map-rais-bra-isic-cbo": {"en": "Locations with specific Occupation in Industry", "pt": "Locations with specific Occupation in Industry"},
    
    "geo_map-secex-bra": {"en": "Export Origins", "pt": "Export Origins"},
    "geo_map-secex-bra-hs": {"en": "Export Origin of Product", "pt": "Export Origin of Product"},
    "geo_map-secex-bra-hs-wld": {"en": "Export Origin of Product with Trade Partner", "pt": "Export Origin of Product with Trade Partner"},
    "geo_map-rais-bra": {"en": "Industry Locations", "pt": "Industry Locations"},
    "geo_map-rais-bra-isic": {"en": "Locations with specific Industry", "pt": "Locations with specific Industry"},
    "geo_map-rais-bra-cbo": {"en": "Locations with specific Occupation", "pt": "Locations with specific Occupation"},
    "geo_map-rais-bra-isic-cbo": {"en": "Locations with specific Occupation in Industry", "pt": "Locations with specific Occupation in Industry"}
    
  }
  
  if (!name) return name;
  else if(labels[name]){
    if (labels[name][l]) return labels[name][l];
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
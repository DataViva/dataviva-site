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
  
  var exceptions = ["cbo_id","isic_id","wld_id","hs_id","bra_id","id_ibge"]
  
  if (exceptions.indexOf(name) >= 0) return text.toUpperCase()
  else if (text.indexOf("cp_bra_") == 0 && app) {
    var arr = text.split("_")
    arr.shift()
    arr.shift()
    var index = arr.shift()
    text = arr.join("_")
    return app.build.bra[index]["name_"+l] + " ("+format_name(text)+")"
  }
  else {
    return format_name(text)
  }
  
  function format_name(name) {
  
    var labels = {
    
      // App Titles
      "compare": {"en": "Compare", "pt": "Comparar"},
      "occugrid": {"en": "Occugrid", "pt": "Occugrid"},
      "geo_map": {"en": "Geo Map", "pt": "Geo Map"},
      "network": {"en": "Network", "pt": "Network"},
      "rings": {"en": "Rings", "pt": "Círculos"},
      "scatter": {"en": "Scatter", "pt": "Disseminar"},
      "stacked": {"en": "Stacked", "pt": "Empilhado"},
      "tree_map": {"en": "Tree Map", "pt": "Tree Map"},

      // Stacked Area Sorting/Order
      "order": {"en": "Order", "pt": "Pedir"},
      "asc": {"en": "Ascending", "pt": "Ascendente"},
      "desc": {"en": "Descending", "pt": "Descendente"},
    
      // Stacked Area Layout Type
      "layout": {"en": "Layout", "pt": "Layout"},
      "value": {"en": "Value", "pt": "Valor"},
      "share": {"en": "Market Share", "pt": "Participa\u00e7\u00e3o de Mercado"},
    
      // RCA Scope Toggle
      "rca_scope": {"en": "RCA Scope", "pt": "Escopo do RCA"},
      "bra_rca": {"en": "Domestic", "pt": "Dom\u00e9stico"},
      "wld_rca": {"en": "International", "pt": "Internacional"},

      // Spotlight Toggle
      "spotlight": {"en": "Highlight RCA", "pt": "Real\u00e7ar RCA"},
      "spotlight_scatter": {"en": "Hide RCA", "pt": "Esconder RCA"},
      "true": {"en": "On", "pt": "Liga"},
      "false": {"en": "Off", "pt": "Desliga"},
    
      // Other Control Labels
      "active": {"en": "Available", "pt": "Dispon\u00edvel"},
      "available": {"en": "Available", "pt": "Dispon\u00edvel"},
      "color_var": {"en": "Color", "pt": "Cor"},
      "grouping": {"en": "Group", "pt": "Grupo"},
      "none": {"en": "None", "pt": "Nenhum"},
      "sizing": {"en": "Size", "pt": "Tamanho"},
      "sort": {"en": "Sort", "pt": "Ordenar"},
      "sorting": {"en": "Sort", "pt": "Ordenar"},
      "total": {"en": "Required", "pt": "Requerido"},
      "year": {"en": "Year", "pt": "Ano"},

      // Filter Depths
      "depth": {"en": "Depth", "pt": "Profundidade"},
      "bra_2": {"en": "State", "pt": "Estado"},
      "bra_4": {"en": "Mesoregion", "pt": "Mesorregi\u00e3o"},
      "bra_6": {"en": "Microregion", "pt": "Microrregi\u00e3o"},
      "bra_7": {"en": "Planning Region", "pt": "Regi\u00e3o de Planejamento"},
      "bra_8": {"en": "Municipality", "pt": "Municipalidade"},
      "cbo_1": {"en": "Sector", "pt": "Setor"},
      "cbo_2": {"en": "2 Digit", "pt": "2 D\u00edgitos"},
      "cbo_3": {"en": "3 Digit", "pt": "3 D\u00edgitos"},
      "cbo_4": {"en": "4 Digit", "pt": "4 D\u00edgitos"},
      "cbo_6": {"en": "6 Digit", "pt": "4 D\u00edgitos"},
      "isic_1": {"en": "Sector", "pt": "Setor"},
      "isic_3": {"en": "2 Digit", "pt": "2 D\u00edgitos"},
      "isic_4": {"en": "3 Digit", "pt": "3 D\u00edgitos"},
      "isic_5": {"en": "4 Digit", "pt": "4 D\u00edgitos"},
      "hs_2": {"en": "Sector", "pt": "Setor"},
      "hs_4": {"en": "HS2", "pt": "HS2"},
      "hs_6": {"en": "HS4", "pt": "HS4"},
      "hs_8": {"en": "HS6", "pt": "HS6"},
      "wld_2": {"en": "Continent", "pt": "Continente"},
      "wld_5": {"en": "Country", "pt": "Pa\u00eds"},
      "bra_2_plural": {"en": "States", "pt": "Estados"},
      "bra_4_plural": {"en": "Mesoregions", "pt": "Mesorregi\u00f5es"},
      "bra_6_plural": {"en": "Microregions", "pt": "Microrregi\u00f5es"},
      "bra_7_plural": {"en": "Planning Regions", "pt": "Regi\u00f5es de Planejamento"},
      "bra_8_plural": {"en": "Municipalities", "pt": "Municipalidades"},
      "cbo_1_plural": {"en": "Sectors", "pt": "Setores"},
      "cbo_2_plural": {"en": "2 Digit", "pt": "2 D\u00edgitos"},
      "cbo_3_plural": {"en": "3 Digit", "pt": "3 D\u00edgitos"},
      "cbo_4_plural": {"en": "4 Digit", "pt": "4 D\u00edgitos"},
      "cbo_6_plural": {"en": "6 Digit", "pt": "4 D\u00edgitos"},
      "isic_1_plural": {"en": "Sectors", "pt": "Setores"},
      "isic_3_plural": {"en": "2 Digit", "pt": "2 D\u00edgitos"},
      "isic_4_plural": {"en": "3 Digit", "pt": "3 D\u00edgitos"},
      "isic_5_plural": {"en": "4 Digit", "pt": "4 D\u00edgitos"},
      "hs_2_plural": {"en": "Sectors", "pt": "Setores"},
      "hs_4_plural": {"en": "HS2", "pt": "HS2"},
      "hs_6_plural": {"en": "HS4", "pt": "HS4"},
      "hs_8_plural": {"en": "HS6", "pt": "HS6"},
      "wld_2_plural": {"en": "Continents", "pt": "Continentes"},
      "wld_5_plural": {"en": "Countries", "pt": "Pa\u00edses"},
    
      // Calculation Labels
      "eci": {"en": "Domestic Complexity", "pt": "Complexidade Dom\u00e9stica"},
      "eci_wld": {"en": "International Complexity", "pt": "Complexidade Internacional"},
      "pci": {"en": "Product Complexity", "pt": "Complexidade do Produto"},
      "ici": {"en": "Industry Complexity", "pt": "Complexidade da Ind\u00fdstria"},
      "oci": {"en": "Occupation Complexity", "pt": "Complexidade da Ocupa\u00e7\u00e3o"},
      "distance": {"en": "Distance", "pt": "Dist\u00e2ncia"},
      "employed": {"en": "Employed", "pt": "Empregado"},
      "importance": {"en": "Importance", "pt": "Import\u00e2ncia"},
      "elsewhere": {"en": "Employees Available In Other Industries", "pt": "Empregados em Outras Ind\u00fdstrias"},
      "growth_val": {"en": "Wage Growth", "pt": "Crescimento dos Sal\u00e1rios"},
      "growth_val_total": {"en": "Cumulative Wage Growth", "pt": "Crescimento Salarial Acumulada"},
      "proximity": {"en": "Proximity", "pt": "Proximidade"},
      "rca": {"en": "Domestic RCA", "pt": "RCA Dom\u00e9stico"},
      "rca_wld": {"en": "International RCA", "pt": "RCA Internacional"},
      
      "opp_gain": {"en": "Opportunity Gain", "pt": "Ganho de Oportunidade Dom\u00e9stico"},
      "opp_gain_wld": {"en": "International Opportunity Gain", "pt": "Ganho de Oportunidade Internacional"},
      
      "val_usd_growth_pct": {"en": "Growth Rate (1 year)", "pt": "Taxa de Crescimento (1 ano)"},
      "val_usd_growth_pct_5": {"en": "Growth Rate (5 year)", "pt": "Taxa de Crescimento (5 anos)"},
      "val_usd_growth_val": {"en": "Growth Value (1 year)", "pt": "Valor de Crescimento (1 ano)"},
      "val_usd_growth_val_5": {"en": "Growth Value (5 year)", "pt": "Valor de Crescimento (5 anos)"},
      
      "wage_growth_pct": {"en": "Wage Growth Rate (1 year)", "pt": "Taxa de Crescimento dos Sal\u00e1rios (1 ano)"},
      "wage_growth_pct_5": {"en": "Wage Growth Rate (5 year)", "pt": "Taxa de Crescimento dos Sal\u00e1rios (5 anos)"},
      "wage_growth_val": {"en": "Wage Growth Value (1 year)", "pt": "Valor de Crescimento dos Sal\u00e1rios (1 ano)"},
      "wage_growth_val_5": {"en": "Wage Growth Value (5 year)", "pt": "Valor de Crescimento dos Sal\u00e1rios (5 anos)"},
      "num_emp_growth_pct": {"en": "Employee Growth Rate (1 year)", "pt": "Taxa de Crescimento de Empregados (1 ano)"},
      "num_emp_growth_pct_5": {"en": "Employee Growth Rate (5 year)", "pt": "Taxa de Crescimento de Empregados (5 anos)"},
      "num_emp_growth_val": {"en": "Employee Growth (1 year)", "pt": "Crescimento do N\u00famero de Empregados (1 ano)"},
      "num_emp_growth_val_5": {"en": "Employee Growth (5 year)", "pt": "Crescimento do N\u00famero de Empregados (5 anos)"},
    
      // RAIS Labels
      "rais": {"en": "Establishments and Employment (RAIS)", "pt": "Estabelecimentos e Emprego (RAIS)"},
      "num_emp": {"en": "Employees", "pt": "Empregados"},
      "num_est": {"en": "Establishments", "pt": "Estabelecimentos"},
      "wage": {"en": "Monthly Wage", "pt": "Renda Mensal"},
      "wage_avg": {"en": "Average Monthly Wage", "pt": "Renda Mensal M\u00e9dia"},
      "wage_avg_bra": {"en": "Brazilian Average Wage", "pt": "Sal\u00e1rio M\u00e9dio Brasileiro"},
    
      // SECEX Labels
      "secex": {"en": "Product Exports (SECEX)", "pt": "Exporta\u00e7\u00f5es de Produtos (SECEX)"},
      "val_usd": {"en": "Export Value", "pt": "Valor de Exporta\u00e7\u00e3o"},
    
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

      // Filter Titles
      "bra": {"en": "Location", "pt": "Localidade"},
      "bra_plural": {"en": "Locations", "pt": "Localidades"},
      "cbo": {"en": "Occupation", "pt": "Ocupa\u00e7\u00e3o"},
      "cbo_plural": {"en": "Occupations", "pt": "Ocupa\u00e7\u00f5es"},
      "hs": {"en": "Product Export", "pt": "Exporta\u00e7\u00e3o de Produtos"},
      "hs_plural": {"en": "Product Exports", "pt": "Exporta\u00e7\u00f5es de Produtos"},
      "icon": {"en": "Icon", "pt": "\u00cdcone"},
      "isic": {"en": "Industry", "pt": "Ind\u00fastria"},
      "isic_plural": {"en": "Industries", "pt": "Ind\u00fastrias"},
      "wld": {"en": "Trade Partner", "pt": "Parceiro Comercial"},
      "wld_plural": {"en": "Trade Partners", "pt": "Parceiros Comerciais"},
    
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
      "Data Provided by": {"en": "Data Provided by", "pt": "Dados Fornecidos por"},
      "related_apps": {"en": "Related Apps", "pt": "Apps Relacionados"},
      "other_apps": {"en": "Other Apps", "pt": "Outros Apps"},
      "Show All Years": {"en": "Show All Years", "pt": "Mostrar Todos os Anos"},
      "Build Not Available": {"en": "Build Not Available", "pt": "Construir N\u00e3o Dispon\u00edvel"},
      "Building App": {"en": "Building App", "pt": "Constru\u00e7\u00e3o App"},
      "Downloading Additional Years": {"en": "Downloading Additional Years", "pt": "Baixando Anos Adicionais"},
    
      // Viz-Whiz Text
      "Click for More Info": {"en": "Click for more data and related apps.", "pt": "Clique para dados adicionais e aplicativos relacionados."},
      "Click to Zoom": {"en": "Click to Zoom", "pt": "Clique para Ampliar"},
    
      // Ask Sabrina
      "Asked by": {"en": "Asked by", "pt": "Solicitado por"},
      "points": {"en": "Points", "pt": "Pontos"},
      "votes": {"en": "Top Voted", "pt": "Mais Votados"},
      "newest": {"en": "Newest", "pt": "O Mais Novo"},
      
      // Selector
      "search": {"en": "Search", "pt": "Pesquisar"},
      "search_results": {"en": "Search Results", "pt": "Resultados da Pesquisa"},
      "select": {"en": "Select", "pt": "Escolher"},
      "show": {"en": "Show", "pt": "Mostrar"}
    
    }
    
    if (!name) return name;
    else if(labels[name]){
      if (labels[name][l]) return labels[name][l]
      else return name.toTitleCase()
    } 
    else return name.toTitleCase()
  
  }
  
}

dataviva.format.number = function(value,name,l) {
  
  if (!l) var l = dataviva.language
  
  var smalls = ["rca","rca_bra","rca_wld","distance","eci","pci","ici","oci"]
  
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
    var return_value = d3.round(value,l)
  }
  else if (value.toString().split(".")[0].length > 4) {
    
    var symbol = d3.formatPrefix(value).symbol
    symbol = symbol.replace("G", "B") // d3 uses G for giga
    
    // Format number to precision level using proper scale
    value = d3.formatPrefix(value).scale(value)
    value = parseFloat(d3.format(".3g")(value))
    
    if (symbol && dataviva.language == "pt") {
      var digit = parseFloat(value.toString().split(".")[0])
      if (symbol == "T") {
        if (digit < 2) symbol = " Trilh\u00e3o"
        else symbol = " Trilh\u00f5es"
      }
      else if (symbol == "B") {
        if (digit < 2) symbol = " Bilh\u00e3o"
        else symbol = " Bilh\u00f5es"
      }
      else if (symbol == "M") {
        if (digit < 2) symbol = " Milh\u00e3o"
        else symbol = " Milh\u00f5es"
      }
      else if (symbol == "k") {
        if (digit < 2) symbol = " Milhares"
        else symbol = " Mil"
      }
    }
    
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
        "val_usd_growth_val": ["$"," USD"],
        "val_usd_growth_val_5": ["$"," USD"]
      }

  if (total_labels[name]) {
    var labels = total_labels[name]
    return_value = labels[0] + return_value + labels[1]
  }
  
  return_value = String(return_value)
  
  if (l == "pt") {
    var n = return_value.split(".")
    n[0] = n[0].replace(",",".")
    return_value = n.join(",")
  }
  
  if (name == "total") return_value = "~"+return_value
  
  return return_value
  
}

dataviva.ui = {}

dataviva.ui.header = function() {
  var dyn = d3.select("#dynamic_header").node()
  if (dyn) {
    var header_height = d3.select("#header_container").node().offsetHeight
    var dyn_height = dyn.offsetHeight
    var dyn_top = dyn.offsetTop-header_height
    d3.select("#container").style("margin-top",dyn_height+dyn_top+"px")
    document.onscroll = function() {
      var top = document.body.scrollTop
      if (top > 10) {
        d3.select("#header_container")
          .style("height",header_height+dyn_height+dyn_top+"px")
      }
      else {
        d3.select("#header_container")
          .style("height",header_height+"px")
      }
    }
  }
}

dataviva.ui.background = function() {
  var fs = d3.select("#fullscreen")
  if (fs.node()) {
    var hour = new Date().getHours()
    if (hour >= 5 && hour <= 9) {
      var filename = "dawn"
    }
    else if (hour >= 10 && hour <= 17) {
      var filename = "day"
    }
    else if (hour >= 18 && hour <= 22) {
      var filename = "dusk"
    }
    else {
      var filename = "night"
    }
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
    
    window.onresize = resizebg
    resizebg()
    
  }
}

dataviva.ui.tooltip = function(id,state) {
  if (state) {
    
    var item = document.getElementById(id),
        size = item.getBoundingClientRect(),
        text = item.getAttribute("alt") ? item.getAttribute("alt") : id
        
    vizwhiz.tooltip.remove(id);
    vizwhiz.tooltip.create({
      "x": size.left+size.width/2,
      "y": size.top+size.height/2,
      "offset": size.height/2,
      "arrow": true,
      "description": text,
      "width": "auto",
      "id": id
    })
    
  }
  else {
    vizwhiz.tooltip.remove(id);
  }
}

dataviva.ui.loading = function(parent) {
  
  var self = this
  
  this.div = d3.select(parent).append("div")
    .attr("class","loading")
    
  this.icon = self.div.append("i")
    .attr("class","icon-certificate icon-4x")
    
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

  return this
  
}

// Returns a random number between the min and max passed to the function
dataviva.random = function(min,max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

dataviva.displayID = function(id,type) {

  if (id) {
    if (["hs","wld"].indexOf(type) >= 0 && id.length > 2) {
      return id.slice(2).toUpperCase();
    }
    else if (["isic"].indexOf(type) >= 0) return id.slice(1);
    else return id;
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
  else if (type == "cbo") var array = [1,2,3,4];
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
      .attr("class","vizwhiz_tooltip_close")
      .html("\&times;")
      .style("background-color",color)
      .on(vizwhiz.evt.click,function(){
        dataviva.popover.hide("#"+id);
      })
  }
  
}

dataviva.popover.show = function(id) {
  
  if (d3.select("#popover_mask").empty()) {
    d3.select("body").append("div")
      .attr("id","popover_mask")
      .on(vizwhiz.evt.click,function(){
        dataviva.popover.hide();
      })
  }
  
  d3.select("#popover_mask")
    .style("display","block")
    
  d3.select(id)
    .style("display","block")
    
  setTimeout(function(){
  
    d3.select("#popover_mask")
      .style("opacity",0.8)
    
    d3.select(id)
      .style("opacity",1)
    
  },5)
  
}

dataviva.popover.hide = function(id) {
  
  if (id) var popover = d3.select(id)
  else var popover = d3.selectAll(".popover")

  popover.each(function(){
    
      if (d3.select(this).style("display") != "none") {
        
        var p = d3.select(this)

        d3.select("#popover_mask").style("opacity",0);
        p.style("opacity",0);
        
        var timing = parseFloat(p.style("transition-duration"),10)*1000
        
        setTimeout(function(){
          p.style("display","none")
          d3.select("#popover_mask").style("display","none")
        },timing)
        
      }
      
    })

}
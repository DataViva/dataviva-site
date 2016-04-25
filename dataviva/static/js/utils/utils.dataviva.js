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
dataviva.format.text = function(text, opts) {

  if (!opts) opts = {};
  var name = opts.key || "";
  if (typeof name !== "string") name = "";

  if (text.indexOf("xx") === 0 && name === "course_sc_5" && app && app.attrs && app.attrs.course_sc) {
    return app.attrs.course_sc.course_sc_5[text].name;
  }

  var l = dataviva.language;

  if (text.indexOf("top_") == 0) {
    var x = text.substring(4)
    if (l == "pt") return format_name(x) + " " + format_name("top")
    else return format_name("top") + " " + format_name(x)
  }

  var exceptions = ["id", "bra_id", "id_ibge", "cnae_id", "cbo_id",
                    "hs_id", "wld_id", "university_id", "course_hedu_id",
                    "school_id", "course_sc_id"];

  if (exceptions.indexOf(name) >= 0) return text.toUpperCase()
  else if (text.indexOf("cp_bra_") == 0 && app) {
    var arr = text.split("_")
    arr.shift()
    arr.shift()
    var index = arr.shift()
    text = arr.join("_")
    if (index >= app.build.bra.length)
      index = index % app.build.bra.length;

    return app.build.bra[index]["name_"+l] + " - "+format_name(text);
  }
  else if (!name || (name.indexOf("_display") < 0 && name.indexOf("_id") < 0)) {
    return format_name(text)
  }
  else return text

  function format_name(name) {

    var labels = dataviva.dictionary;

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
      if (labels[name]) return labels[name]
      else return name.toTitleCase()
    }
    else if (name.indexOf("total_") == 0) {
      label_name = name.substr(6)
      if (labels[label_name]) return labels[label_name]
      else return name.toTitleCase()
    }
    // else if (name.indexOf("population_") == 0) {
    //   year = name.split("_")[1]
    //   if (labels["population"]) return labels["population"] + " ("+year+")"
    //   else return name.toTitleCase() + " ("+year+")"
    // }
    else if (name.indexOf("_") > -1) {
      year = name.split("_")[1]
      label = name.split("_")[0]
      if (labels[label]) return labels[label] + " ("+year+")"
      return label.toTitleCase() + " ("+year+")"
    }
    else return name.toTitleCase()

  }

}

dataviva.format.affixes = {
  "val_usd": ["USD ",""],
  "export_val": ["USD ",""],
  "import_val": ["USD ",""],
  "export_kg": [""," kg"],
  "import_kg": [""," kg"],
  "export_val_kg": ["USD ",""],
  "import_val_kg": ["USD ",""],
  "purchase_value": ["R$ ",""],
  "transfer_value": ["R$ ",""],
  "wage": ["R$ ",""],
  "wage_avg": ["R$ ",""],
  "wage_month": ["R$ ",""],
  "wage_avg_bra": ["R$ ",""]
};

for (var a in dataviva.format.affixes) {
  dataviva.format.affixes["cp_bra_0_" + a] = dataviva.format.affixes[a];
  dataviva.format.affixes["cp_bra_1_" + a] = dataviva.format.affixes[a];
}

dataviva.format.number = function(value, opts) {

  if (!opts) opts = {};
  var name = opts.key || "";
  var labels = "labels" in opts ? opts.labels : true;
  if (typeof name !== "string") name = "";

  var negative = value < 0;
  value = Math.abs(value);

  if (name.indexOf("_growth") >= 0) value = value * 100;

  var smalls = ["rca", "rca_bra", "rca_wld", "rcd", "distance", "distance_wld",
                "eci", "pci", "opp_gain", "opp_gain_wld",
                "bra_diversity_eff", "cnae_diversity_eff", "cbo_diversity_eff",
                "hs_diversity_eff", "wld_diversity_eff"];

  var exceptions = ["id", "bra_id", "id_ibge", "cnae_id", "cbo_id",
                    "hs_id", "wld_id", "university_id", "course_hedu_id",
                    "school_id", "course_sc_id"];

  if (exceptions.indexOf(name) >= 0) return value.toString().toUpperCase();

  var return_value;
  if (name === "year") {
    return_value = value;
  }
  else if (name === "share") {
    if (value === 0) return_value = 0;
    else if (value >= 100) return_value = d3.format(",f")(value);
    else if (value > 99) return_value = d3.format(".3g")(value);
    else return_value = d3.format(".2g")(value);
    return_value += "%";
  }
  else if (smalls.indexOf(name) >= 0 || value < 1) {
    var r = value.toString().split(""), len = false;
    r.forEach(function(n,i){
      if (n != "0" && n != "." && !len) len = i;
    });
    if (len > 5) len = 5;
    return_value = d3.round(value, len + 1);
  }
  else if (value.toString().split(".")[0].length > 3) {

    var symbol = d3.formatPrefix(value).symbol;
    symbol = symbol.replace("G", "B"); // d3 uses G for giga

    // Format number to precision level using proper scale
    value = d3.formatPrefix(value).scale(value);
    value = parseFloat(d3.format(".3g")(value));

    if (symbol && dataviva.language === "pt") {
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
      symbol = " "+symbol
    }

    return_value = value + symbol;
  }
  else if (name === "age") {
    return_value = d3.format(".3g")(value);
  }
  else if (value === 0) {
    return_value = 0;
  }
  else {
    return_value = d3.format(",f")(value);
  }

  if (name.indexOf("total_") == 0) {
    var label_name = name.substr(6)
  }
  else if (name.indexOf("cp_bra_") == 0) {
    var label_name = name.substr(9)
  }
  else var label_name = name

  var growth = label_name.indexOf("_growth") > 0;

  if (labels && dataviva.format.affixes[label_name]) {
    var labels = dataviva.format.affixes[label_name]
    return_value = labels[0] + return_value + labels[1]
  }
  else if (growth) {
    return_value += "%";
    var arrow = negative ? "down" : "up";
    return_value = "<span class='text-"+arrow+"'>" + return_value + "&nbsp;<i class='growth-arrow "+arrow+" fa fa-arrow-circle-"+arrow+"'></i>" + "</span>";
  }

  return_value = String(return_value)

  if (dataviva.language === "pt") {
    var n = return_value.split(".")
    n[0] = n[0].replace(",",".")
    return_value = n.join(",")
  }

  if (negative && !growth) return_value = "-"+return_value

  return return_value

}

dataviva.ui = {}

dataviva.ui.background = function() {
  var fs = d3.select("#fullscreen")
  if (fs.node()) {
    // var filename = "clouds"
    var filename = "city_small"
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

dataviva.ui.tooltip = function(id, obj, align, parent) {
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
      "parent": parent,
      "max_width": 180
    })

  }
  else {
    d3plus.tooltip.remove(id);
  }
}

// <div class="page-loader">
//    <div class="loader"></div>
//    <span>Carregando...</span>
// </div>


dataviva.ui.loading = function(parent) {

  var self = this

  d3.select(parent).classed('loading',true);

  this.div = d3.select(parent).insert("div", ":first-child")
    .attr("class","page-loader")

  this.icon = self.div.append("div")
    .attr("class","loader-icon")

  this.words = self.div.append("span")
    .attr("class","text")

  this.timing = parseFloat(self.div.style("transition-duration"),10)*1000

  this.show = function(callback) {

    self.div.style("display","block")

    setTimeout(function(){

      self.div.style("opacity",1)
      d3.select(parent).classed('loading', true);

      if (callback) {
        setTimeout(callback,self.timing)
      }

    },5)

    return self
  }

  this.hide = function() {

    self.div.style("opacity",0)
    d3.select(parent).classed('loading', false);

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
    else if (["cnae"].indexOf(type) >= 0 && id.length > 1) return id.slice(1);
    else return id.toUpperCase();
  }
  else {
    return id;
  }

}

dataviva.icon = function(id,type,color) {

  if (["university","school"].indexOf(type) >= 0 && id !== "all") return false;
  if (type === "bra" && id.length === 1) return false;

  if (type !== "file" && type !== "wld" && id !== "all"){
    var i = type === "bra" ? 1 : 0,
        depth = dataviva.depths(type)[i],
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

dataviva.cleanData = function(data, dataset, output) {

  var zerofills = {
    "secex": ["export_val","import_val", "import_kg", "export_kg"],
    "rais": ["wage","wage_avg","num_jobs","num_est"],
    "hedu": ["enrolled"],
    "sc": ["enrolled"],
    "ei": ["purchase_value", "transfer_value"]
  }

  var output_attr = output === "bra_r" ? "bra" :
                    ["age", "basic"].indexOf(output) >= 0 ? "course_sc" :
                    output === "adm" ? "school" : output;

  var depths = dataviva.depths(output_attr);

  var extras = {}

  if ("diversity" in data) {
    data.diversity.data.forEach(function(d){
      extras[d[1]] = {}
      d.forEach(function(v, i){
        if (data.diversity.headers[i].indexOf("diversity") >= 0) {
          extras[d[1]][data.diversity.headers[i]] = v
        }
      })
    })
  }

  if ("pci" in data) {
    data.pci.data.forEach(function(d){
      extras[d[1]] = {"pci": d[2]}
    })
  }

  var dataObj = data.data.map(function(d){

    var temp = d.reduce(function(obj, value, i){
      var header = data.headers[i];
      obj[header] = value;
      return obj
    }, {})

    if (JSON.stringify(depths) !== "[0]") {

      var id;
      if (dataset === "ei") {

        if (output === "bra_r") {
          id = temp.bra_id_r;
        }
        else {
          id = temp.bra_id_s;
        }

      }
      else {
        id = temp[output_attr+"_id"];
      }

      depths.forEach(function(depth){
        temp[output_attr+"_"+depth] = id.slice(0,depth);
      });

      if (id in extras) {
        temp = d3plus.object.merge(temp, extras[id]);
      }

    }

    if (temp.month) {
      temp.month = new Date(temp.month+"/1/"+temp.year);
    }

    zerofills[dataset].forEach(function(z){
      if (!(z in temp)) {
        temp[z] = 0
      }
    })

    if (dataset === "secex") {
      temp.export_val_kg = temp.export_kg ? temp.export_val/temp.export_kg : 0;
      temp.import_val_kg = temp.import_kg ? temp.import_val/temp.import_kg : 0;
    }
    else if (dataset === "rais") {
      if (temp.num_est) temp.num_jobs_est = Math.ceil(temp.num_jobs/temp.num_est);
      else temp.num_jobs_est = 0;
    }

    if ("classes" in temp && "enrolled" in temp) {
      temp.enrolled_classes = temp.enrolled/temp.classes
    }

    return temp

  })

  return dataObj;

}

dataviva.depths = function(type) {

  if (type == "cnae") return [1,3,6];
  else if (type == "cbo") return [1,4];
  else if (type == "hs") return [2,6];
  else if (type == "bra") return [1,3,5,7,9];
  else if (type == "wld") return [2,5];
  else if (type == "course_hedu") return [2,6];
  else if (type == "university") return [5];
  else if (type == "course_sc") return [2,5];
  else if (type == "school") return [8];
  else return [0];

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
    .style("margin-left",w_px/2+"px")
    .style("margin-top",h_px/2+"px")

  if (close) {
    body.append("div")
      .attr("class","selector_close")
      .html("\&times;")
      .style("background-color",color)
      .on(d3plus.client.pointer.click,function(){
        dataviva.popover.hide("#"+id);
        d3.select("body").style("overflow", "auto")
      })
  }

}

dataviva.popover.show = function(id) {

  if (d3.select("#popover_mask").empty()) {
    d3.select("body").append("div")
      .attr("id","popover_mask")
      .on(d3plus.client.pointer.click,function(){
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

	d3.select("body").append("div")
    .attr("id", "server_message").html(text)
    .append("i")
        .attr("id", "close_message")
        .attr("class", "fa fa-times-circle")
        .on(d3plus.client.pointer.click, function(d){
        var div = d3.select("#server_message")
        var timing = parseFloat(div.style("transition-duration"),10)*1000;
        div.style("opacity",0);
        setTimeout(function(){
          div.remove();
        }, timing)
      });
};

dataviva.url = function(url,args,title) {

  try {
    var same_origin = window.parent.location.host == window.location.host;
  }
  catch (e) {
    var same_origin = false
  }

  var replace = window.location.pathname.indexOf(url.split("?")[0]) >= 0
  var iframe = window != window.parent
  var app_embed = window.location.pathname.indexOf("apps/embed") >= 0
  var app_builder = same_origin && window.parent.location.pathname.indexOf("apps/builder") >= 0
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

    if (iframe && same_origin) {

      if (title && app_builder) window.parent.document.title = "DataViva : "+title

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

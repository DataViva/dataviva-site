function Selector() {
  
  var callback,
      type = "bra",
      name = "bra",
      initial_value = "all",
      distance = 0,
      limit = null,
      lists = {},
      popover = false;
      
  lists.file = {
    "all": {
      "color": "#768593",
      "id": "all",
      "name": visual.format.text("download")
    },
    "svg": {
      "color": "#e87600",
      "id": "svg",
      "name": visual.format.text("svg")
    },
    "png": {
      "color": "#0b1097",
      "id": "png",
      "name": visual.format.text("png")
    },
    "pdf": {
      "color": "#c8140a",
      "id": "pdf",
      "name": visual.format.text("pdf")
    },
    "csv": {
      "color": "#00923f",
      "id": "csv",
      "name": visual.format.text("csv")
    }
  }
      
  function util(selection) {
    
    selection.each(function(data) {
              
      update_distance = function(dist,id) {
        
        data[id].distance = dist
        
        var div = d3.select("#withins"+id)
        
        if (dist > 0) {
          
          div.style("display","block")
          
          var u = distance_url
            .replace("munic",id)
            .replace("value",dist)
            
          d3.json(u,function(raw_distances){

            var distances = [];
            raw_distances.data.forEach(function(d,i){
              if (i != 0) {
                var string = data[d.bra_id_dest].name
                string += " ("+d.distance+"km)";
                distances.push(string)
              }
            })
      
            if (distances.length > 0) {
              div.html("Including "+distances.join(", "))
            } else {
              div.html("No municipalities within that distance.")
            }
          }).on("progress",function(){
            div.html("Loading...")
          })
      
        }
        else {
          div.style("display","none")
        }
      }
      
      select_value = function(x) {
        
        search.node().value = ""
        
        if (depths.indexOf(x.id.length) == depths.length-1) {
          x = data[x.parent]
        }
        
        selected = x;
        
        if (popover) close.style("background-color",vizwhiz.utils.darker_color(x.color))

        if (depths.length > 1) {
          
          bread.select("a").remove()
          if (x.id != "all") {
            bread.append("a")
              .attr("class","site_crumb")
              .html("&laquo; Back")
              .on(vizwhiz.evt.click,function(){
                search.node().value = ""
                select_value(data[selected.parent]);
              })
              .on(vizwhiz.evt.over,function(){
                this.style.color = vizwhiz.utils.darker_color(x.color)
              })
              .on(vizwhiz.evt.out,function(){
                this.style.color = "#888"
              })
          }
          
        }
        
        populate_list(x);
        
      }
      
      var close, header, header_select, bread, icon, title, search, body, sort_toggles;
      
      create_elements = function() {
      
        if (popover) {
          close = container.append("div")
            .attr("class","vizwhiz_tooltip_close")
            .html("\&times;")
            .on(vizwhiz.evt.click,function(){
              visual.popover.hide("#popover");
            })
        }

        header = container.append("div").attr("class","selector_header")
        
        icon = header.append("div").attr("class","selector_header_icon")
        
        title_div = header.append("div").attr("class","selector_title_div")
                
        title = title_div.append("div").attr("class","selector_title")
      
        bread = title_div.append("div").attr("class","breadcrumb")
      
        sort_toggles = header.append("div").attr("class","selector_toggles")
      
        if (sorts.length > 1) {
        
          sort_toggles.append("legend")
            .attr("id","selector_sort")
            .html(visual.format.text("sort"))
      
          sorts.forEach(function(s){
            var input = sort_toggles.append("input")
              .attr("type","radio")
              .attr("id",s)
              .attr("value",s)
              .attr("name","selector_sort")
              .attr("onclick","populate_list(selected,this.value)")
            if (s == sorting) input.attr("checked","checked")
            sort_toggles.append("label")
              .attr("for",s)
              .html(visual.format.text(s))
          })
        
          leon.start("$selector_sort")
        }
        

        header_select = sort_toggles.append("div")
          .attr("class","leon button")
          .html("Select")
      
        search = header.append("input")
          .attr("type","text")
          .attr("id",name+"_search")
          .attr("class","leon text")
          .attr("placeholder","Search");
                
        search.node().oninput = function() { populate_list(selected) };
          
        if (type == "help") {
          body = container.append("iframe")
            .attr("class","selector_body")
            .attr("width","100%")
            .style("height","auto");
        }
        else {
          body = container.append("div")
            .attr("class","selector_body")
            .style("height","auto");
        }
        
      }
      
      var distance_url = "/attrs/bra/munic.value/",
          depths = visual.depths(type,true),
          list = [],
          search_term = ""
          selected = null,
          proximities = [0,30,60,90],
          sort_types = {
            "bra": "population",
            "hs": "val_usd",
            "wld": "val_usd",
            "cbo": "num_emp",
            "isic": "num_emp",
          },
          value = sort_types[name] ? sort_types[name] : null,
          sorts = ["name"]
          
      if (value) {
        sorts.push(value)
        var sorting = value
      }
      else {
        var sorting = "name"
      }
          
      var container = d3.select(this)
        .html("")
        .append("div")
          .attr("class","selector")
      
      if (type == "help") {
        create_elements();
        update_header(data[0]);
        body.attr("src","/about/apps/"+data[0].id+"/?ajax=true")
      }
      else if (data) {
        clean_data();
      }
      else if (lists[type]) {
        data = lists[type];
        create_elements();
        select_value(data[initial_value]);
      }
      else {
        
        d3.json("/attrs/"+type+"/",function(attrs) {
          data = attrs.data
          clean_data();
        })
        
      }
      
      function clean_data() {

        if (data instanceof Array) {
          data = data.filter(function(d){
            return d.available;
          })
        
          var temp_dict = {};
          data.forEach(function(d){
            temp_dict[d.id] = d;
          })
          data = temp_dict;
        }
        else {
          var temp_dict = {};
          for (var d in data) {
            if (d.available) temp_dict[d] = data[d]
          }
          data = temp_dict;
        }
        
        if (!data.all) {
          if (type == "bra") var c = "#009b3a";
          else var c = "#768593";
          var title = type == "bra" ? "brazil" : type
          data.all = {
            "color": c,
            "id": "all",
            "display_id": "All",
            "name": visual.format.text(title)
          };
        }
      
        for (d in data) {
          
          if (!data[d].display_id) {
            data[d].display_id = visual.displayID(d,type);
          }
          
          var depth = depths.indexOf(data[d].id.length)
          
          if (data[d].id == "all") {
            data[d].parent = "none"
          }
          else if (depth == 0) {
            data[d].parent = "all"
          }
          else {
            data[d].parent = d.slice(0,depths[depth-1]);
          }
          
          if (!data[d].icon) data[d].icon = visual.icon(d,type)
        }
        
        lists[type] = data
        create_elements();
        select_value(data[initial_value]);
        
      }
      
      function update_header(x) {
        
        if (typeof x == "string") {
          header_select.style("display","none")
          icon.style("display","none")
          title.text("Searching for \""+x+"\"")
        }
        else {
          icon
            .style("display","inline-block")
            .style("background-image","url('"+x.icon+"')")
            .style("background-color",x.color)
          
          if ((x.id != "all" && (!limit || x.id.length >= limit)) || (!limit && x.id == "all")) {
            header_select
              .style("display","inline-block")
              .on(vizwhiz.evt.click,function(){
                window[callback](data[x.id],name);
              })
          }
          else {
            header_select.style("display","none")
          }
          
          if (name == "bra") {
            var d = depths.indexOf(x.id.length)
            var length = depths[d+1]
            var prefix = visual.format.text("bra_"+length+"_plural")
          }
          else var prefix = visual.format.text(name+"_plural")
          if (x.id == "all" && name != "bra") {
            title.text(prefix)
          }
          else {
            title.text(prefix+" in "+x.name.toTitleCase())
          }
          
        }
        
        var hw = header.node().offsetWidth
        hw -= icon.node().offsetWidth
        hw -= sort_toggles.node().offsetWidth
        hw -= 36
        
        title.style("max-width",hw+"px")

        // Set height, now that the header is completely updated
        set_height();
        
      }
      
      // Used whenever a filter list needs to be re-populated
      populate_list = function(parent,sort) {
        
        if (sort) sorting = sort

        // Remove all current list elements
        body.selectAll("div").remove();
        
        // Get current search box value
        search_term = search.node().value.toLowerCase().removeAccents();
        
        // User is searching, so do this stuff!
        if (search_term.length > 0) {
          
          update_header(search_term);
        
          // Create master list by matching both name and id
          var strings = ["name","id","desc","keywords"]
          list = d3.values(data).filter(function(v){

            var match = false
            strings.forEach(function(s){
              if (v[s]) {
                var str = v[s].toLowerCase().removeAccents()
                if (str.indexOf(search_term) >= 0) {
                  match = true
                }
              }
            })
            
            return match
            
          })
            
        }
        else {
          
          update_header(selected);
          
          // Create list by matching parent ids
          list = d3.values(data).filter(function(v){
            return v.parent == parent.id && v.id != "all";
          })
          
        }
        
        // Sort final generated list
        list.sort(function(a, b){
          
          var lengthdiff = b.id.length - a.id.length
          if (lengthdiff) return lengthdiff
          
          if (a[sorting] && b[sorting]) {
            var a_first = a[sorting]
            var b_first = b[sorting]
          }
          else {
            var a_first = d3.rgb(a.color).hsl().h
            var b_first = d3.rgb(b.color).hsl().h
            if (d3.rgb(a.color).hsl().s == 0) a_first = 361
            if (d3.rgb(b.color).hsl().s == 0) b_first = 361
          }
          
          if (a_first != b_first) {
            if (typeof a_first === "string") return (a_first.localeCompare(b_first));
            else return (b_first - a_first);
          } 
          else {
            var a_second = a.name.toTitleCase()
            var b_second = b.name.toTitleCase()
            return (a_second.localeCompare(b_second))
          }
        })
        
        // Initially add some results
        add_results(20);
        
        // Add more results on scroll
        body.on("scroll",function(){
          if(body.node().scrollTop + body.node().clientHeight + 10 >= body.node().scrollHeight) {
            if (list.length > 0) add_results(20);
          }
        })
        
        body.node().scrollTop = 0;
       
      }
      
      function add_results(amount) {
      
        var results = []
        for (var i = 0; i < amount; i++) {
          results.push(list.shift())
        }
        
        results.forEach(function(v,i){
          
          if (v) {
            
            var item = body.append("div")
              .attr("id","result_"+v.id)
              .attr("class","search_result")
              .on(vizwhiz.evt.click,function(){
                if (v.id.length < depths[depths.length-1]) {
                  select_value(v);
                }
                else {
                  window[callback](data[v.id],name);
                }
              })
              
            if (v.icon != selected.icon || search_term != "") {
              item.append("div")
                .attr("class","search_icon")
                .style("background-color",v.color)
                .style("background-image","url("+v.icon+")")
            }
          
            var title = v.name.toTitleCase().truncate(65)
            if (search.length >= 3) {
              title = title.replace(search,"<b>"+search+"</b>")
              title = title.replace(search.toTitleCase(),"<b>"+search.toTitleCase()+"</b>")
            }
          
            var text = item.append("div")
              .attr("class","search_text")
          
            text.append("div")
              .attr("class","search_title")
              .style("color",vizwhiz.utils.darker_color(v.color))
              .html(title)
          
            text.append("div")
              .attr("class","search_sub")
              .html(visual.format.text(name+"_"+v.id.length))
               
            if (v[value]) {
              text.append("div")
                .attr("class","search_data")
                .text(visual.format.text(value)+": "+visual.format.number({"value": v[value], "name": value}))
            }
            
            var buttons = item.append("div")
              .attr("class","search_buttons")
              
            if (v.id.length < depths[depths.length-1]) {
              
              var d = depths.indexOf(v.id.length)
              var length = depths[d+1]
              var suffix = visual.format.text(name+"_"+length+"_plural")
              
              buttons.append("div")
                .attr("class","leon button")
                .html("Show "+suffix)
                .on(vizwhiz.evt.click,function(){
                  select_value(v);
                });
            }
            else if (name == "bra" && v.id.length == depths[depths.length-1]) {

              text.append("div")
                .attr("id","withins"+v.id)
                .attr("class","search_withins")
                .style("display","none")
                
              if (v.distance) update_distance(v.distance,v.id)

              var prox_toggles = buttons.append("div")
                .attr("class","proximity_toggles")
                
              prox_toggles.append("label")
                .attr("for","distance"+v.id)
                .html(visual.format.text("Municipalities within"))
                
              var select = prox_toggles.append("select")
                .attr("id","distance"+v.id)
                .attr("onchange","update_distance(this.value,'"+v.id+"')")
    
              proximities.forEach(function(p,i){
                var option = select.append("option")
                  .attr("id",p)
                  .attr("value",p)
                  .html(p+"km")
                if (v.distance && p == v.distance) {
                  option.attr("selected","selected")
                }
                else if (i == 0) {
                  option.attr("selected","selected")
                }
              })
      
              leon.start("#distance"+v.id)
              
            }
              
            if (!limit || v.id.length >= limit) {
              buttons.append("div")
                .attr("class","leon button")
                .html("Select")
                .on(vizwhiz.evt.click,function(){
                  window[callback](data[v.id],name);
                });
            }
          
            if (results[i+1] || i == results.length-1) {
              body.append("div")
                .attr("class","vizwhiz_tooltip_data_seperator")
            }
              
          }
        
        })
    
      }
  
      function set_height() {
        // Set height for selector_body, based off of the title height
        var display = container.style("display")
        if (display == "none") container.style("visibility","hidden").style("display","block")
        
        var max_height = container.node().offsetHeight
        max_height -= body.node().offsetTop
        max_height -= parseFloat(body.style("padding-top"),10)
        max_height -= parseFloat(body.style("padding-bottom"),10)
        max_height = Math.floor(max_height)
        if (display == "none") container.style("visibility","visible").style("display","none")
        body.style("height",max_height+"px")
      }
      
      
    })
  }

  util.callback = function(value) {
    if (!arguments.length) return callback;
    callback = value;
    return util;
  }
  
  util.distance = function(value) {
    if (!arguments.length) return distance;
    distance = value;
    return util;
  }
  
  util.initial_value = function(value) {
    if (!arguments.length) return initial_value;
    initial_value = value;
    return util;
  }
  
  util.limit = function(value) {
    if (!arguments.length) return limit;
    limit = value;
    return util;
  }
  
  util.popover = function(value) {
    if (!arguments.length) return popover;
    popover = value
    return util;
  }
  
  util.type = function(value) {
    if (!arguments.length) return name;
    name = value
    type = name == "bra2" ? "bra" : name;
    return util;
  }
  
  return util;
}
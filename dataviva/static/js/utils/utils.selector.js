function Selector() {
  
  var callback,
      type = "bra",
      name = "bra",
      initial_value = "all",
      distance = 0,
      limit = null,
      lists = {}
      
  lists.file = {
    "all": {
      "color": "#ffffff",
      "id": "all",
      "name": dataviva.format.text("download"),
      "parents": [],
      "icon": dataviva.icon("all","file","#ffffff"),
      "desc": dataviva.format.text("download_desc")
    },
    "svg": {
      "color": "#e87600",
      "id": "svg",
      "name": dataviva.format.text("svg"),
      "parents": ["all"],
      "icon": dataviva.icon("svg","file"),
      "desc": dataviva.format.text("svg_desc")
    },
    "png": {
      "color": "#0b1097",
      "id": "png",
      "name": dataviva.format.text("png"),
      "parents": ["all"],
      "icon": dataviva.icon("png","file"),
      "desc": dataviva.format.text("png_desc")
    },
    "pdf": {
      "color": "#c8140a",
      "id": "pdf",
      "name": dataviva.format.text("pdf"),
      "parents": ["all"],
      "icon": dataviva.icon("pdf","file"),
      "desc": dataviva.format.text("pdf_desc")
    },
    "csv": {
      "color": "#00923f",
      "id": "csv",
      "name": dataviva.format.text("csv"),
      "parents": ["all"],
      "icon": dataviva.icon("csv","file"),
      "desc": dataviva.format.text("csv_desc")
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
            
          d3.json(u)
            .header("X-Requested-With", "XMLHttpRequest")
            .get(function(error,raw_distances){

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
              
            })
      
        }
        else {
          div.style("display","none")
        }
      }
      
      populate_list = function(parent,sort) {
        
        if (sort) sorting = sort

        // Remove all current list elements
        body.selectAll("div").remove();
        
        // Get current search box value
        search_term = search.node().value.toLowerCase().removeAccents()
        searching = search_term.length > 0;
        
        // User is searching, so do this stuff!
        if (searching) {
          
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
          
          if (type == "file") {
            list = d3.values(data).filter(function(v){
              return v.id != "all";
            })
          }
          else {
            // Create list by matching parent ids
            list = d3.values(data).filter(function(v){
              if (parent.id != "all") {
                var child = v.parents.indexOf(parent.id) >= 0
              }
              else {
                var child = true
              }
              return v.id.length == current_depth && v.id != "all" && child;
            })
          }
          
        }
        
        // Sort final generated list
        list.sort(function(a, b){
          
          var lengthdiff = b.id.length - a.id.length
          if (lengthdiff) return lengthdiff
          
          if (type == "bra") {
            var a_state = a.id.substr(0,2)
            var b_state = b.id.substr(0,2)
          }
          else {
            var a_state = a.id
            var b_state = b.id
          }
          
          if (a_state == "mg" && a_state != b_state) {
            return -1
          }
          else if (b_state == "mg" && a_state != b_state) {
            return 1
          }
          else if (a[sorting] && b[sorting]) {
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

        
        var parent = container.node().parentNode,
            display = d3.select(parent).style("display")
            
        if (display == "none") {
          parent.style.visibility = "hidden"
          parent.style.display = "block"
        }
        
        // Initially add some results
        add_results(20);
        
        if (display == "none") {
          parent.style.visibility = "visible"
          parent.style.display = "none"
        }
        
        // Add more results on scroll
        body.on("scroll",function(){
          if(body.node().scrollTop + body.node().clientHeight + 10 >= body.node().scrollHeight) {
            if (list.length > 0) add_results(20);
          }
        })
        
        body.node().scrollTop = 0;
       
      }
      
      select_value = function(x,depth) {
        
        search.node().value = ""
        
        if (depths.indexOf(x.id.length) == depths.length-1) {
          x = data[x.parents[0]]
        }
        
        selected = x
        
        if (depth_path.indexOf(depth) > 0) depth_path.pop()
        else if ((!depth_path.length || depth_path[depth_path.length-1] < current_depth) && x.id != "all" && current_depth) depth_path.push(current_depth)
        
        current_depth = depth
        
        if (depths.length > 1) {
          
          bread.select("a").remove()
          if (x.id != "all") {
            bread.append("a")
              .attr("class","site_crumb")
              .html("&laquo; Back")
              .on(vizwhiz.evt.click,function(){
                search.node().value = ""
                select_value(data[selected.parents[0]],depth_path[depth_path.length-1]);
              })
              .on(vizwhiz.evt.over,function(){
                this.style.color = vizwhiz.utils.darker_color(x.color)
              })
              .on(vizwhiz.evt.out,function(){
                this.style.color = "#888"
              })
          }
          
        }
        populate_list(x,sorting);
        
      }
      
      create_elements = function() {

        header = container.append("div").attr("class","selector_header")
        
        icon = header.append("div").attr("class","selector_header_icon")
        
        title_div = header.append("div").attr("class","selector_title_div")
                
        title = title_div.append("div").attr("class","selector_title")
                
        description = title_div.append("div").attr("class","selector_description")
      
        bread = title_div.append("div").attr("class","breadcrumb")
      
        sort_toggles = header.append("div").attr("class","selector_toggles")
      
        if (sorts.length > 1) {
        
          sort_toggles.append("legend")
            .attr("id","selector_sort_div")
            .html(dataviva.format.text("sort"))
      
          sorts.forEach(function(s){
            var input = sort_toggles.append("input")
              .attr("type","radio")
              .attr("id","selector_sort_"+s)
              .attr("value",s)
              .attr("name","selector_sort")
              .attr("onclick","populate_list(selected,this.value)")
            if (s == sorting) input.attr("checked","checked")
            sort_toggles.append("label")
              .attr("for","selector_sort_"+s)
              .html(dataviva.format.text(s))
          })
          
          sorter = leon("$selector_sort").color(dataviva.color)
        }
        
        header_select_div = sort_toggles.append("div").attr("id","header_select_div")
          
        var b = header_select_div.append("input")
          .attr("type","button")
          .attr("id","header_select")
          .attr("value",dataviva.format.text("select"))
          
        header_select = leon("#header_select")
        
        search = header.append("input")
          .attr("type","text")
          .attr("id",name+"_search")
          .attr("class","leon text")
          .attr("placeholder",dataviva.format.text("search"))
          
        leon("#"+name+"_search").color(dataviva.color).size("medium")
              
        search.node().oninput = function() { populate_list(selected) };
        
        if (type == "file") {
          search.style("display","none")
        }
          
        body = container.append("div")
          .attr("class","selector_body")
          .style("height","auto")
        
        selector_load.hide()
        
        if (initial_value != "all") {
          if (type == "bra" && initial_value == "mg") {
            var depth = 7
          }
          else if (type == "bra" && initial_value.length == 7) {
            var depth = 8
          }
          else {
            var d = depths.indexOf(initial_value.length)
            if (d+1 == depths.length) var depth = depths[d]
            else var depth = depths[d+1]
          }
        }
        else {
          var depth = depths[0]
        }
        
        if (initial_value != "all") {
          if (type == "bra" && initial_value.length >= 7) {
            if (initial_value.substr(0,2) == "mg") {
              depth_path = [2,7]
            }
            else {
              depth_path = [2,4]
            }
          }
          else {
            depth_path = []
            depths.forEach(function(d){
              if (d <= initial_value.length) depth_path.push(d)
            })
          }
        }
        else {
          depth_path = []
        }
        
        select_value(data[initial_value],depth);
        
      }

      clean_data = function() {
        
        if (data instanceof Array) {
          data = data.filter(function(d){
            return d.available || (type == "bra" && d.id.length == 7);
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
          else var c = "#ffffff";
          var title = type == "bra" ? "brazil" : type
          data.all = {
            "color": c,
            "id": "all",
            "display_id": "All",
            "name": dataviva.format.text(title)
          };
        }
      
        for (d in data) {
          
          if (!data[d].display_id) {
            data[d].display_id = dataviva.displayID(d,type);
          }
          
          var depth = depths.indexOf(d.length)
          
          if (d == "all") {
            data[d].parents = ["none"]
          }
          else if (depth == 0) {
            data[d].parents = ["all"]
          }
          else if (type == "bra" && d.length == 8){
            data[d].parents = [d.slice(0,depths[depth-1])]
            if (data[d].plr) {
              data[d].parents.push(data[d].plr)
            }
          }
          else if (type == "bra" && d.length == 7){
            data[d].parents = [d.slice(0,2)]
          }
          else {
            data[d].parents = [d.slice(0,depths[depth-1])]
          }
          
          if (!data[d].icon) data[d].icon = dataviva.icon(d,type,data[d].color)
        }
        
        lists[type] = data
        create_elements()
        
      }
      
      update_header = function(x) {
        
        if (typeof x == "string") {
          header_select_div.style("display","none")
          icon.style("display","none")
          title.text(dataviva.format.text("search_results"))
          var header_color = "#333333"
        }
        else {
          
          var header_color = x.color
          
          icon.style("background-image","url('"+x.icon+"')")
          
          if (["wld","bra"].indexOf(type) < 0 || (type == "wld" && x.id.length != 5)) {
            icon.style("background-color",x.color)
          }
          
          if (type != "file" && ((x.id != "all" && (!limit || x.id.length >= limit)) || (!limit && x.id == "all"))) {
            header_select_div.style("display","inline-block")
            header_select.leons.header_select.item.onclick = function(){
              callback(data[x.id],name)
            }
            header_select.color(x.color)
          }
          else {
            header_select_div.style("display","none")
          }
          
          if (type == "file") var prefix = x.name
          else if (type == "bra") {
            var prefix = dataviva.format.text("bra_"+current_depth+"_plural")
          }
          else var prefix = dataviva.format.text(type+"_plural")
          
          if (x.id == "all" && type != "bra") {
            title.text(prefix)
          }
          else {
            title.text(prefix+" in "+x.name.toTitleCase())
          }
          
          if (x.desc && type == "file") {
            description.text(x.desc)
          }
          else {
            description.text("")
          }
          
        }
        
        if (header_color == "#ffffff") header_color = "#333333"
        
        var close = d3.select(container.node().parentNode).select(".vizwhiz_tooltip_close")
        if (close.node()) {
          close.style("background-color",header_color)
        }
        
        if (sorter) {
          sorter.color(header_color)
        }
        
        var hw = header.node().offsetWidth
        hw -= icon.node().offsetWidth
        hw -= sort_toggles.node().offsetWidth
        hw -= 36
        
        title.style("max-width",hw+"px")

        // Set height, now that the header is completely updated
        set_height();
        
      }
      
      add_results = function(amount) {
      
        var results = []
        for (var i = 0; i < amount; i++) {
          results.push(list.shift())
        }
        
        results.forEach(function(v,i){
          
          if (v) {
            
            var item = body.append("div")
              .attr("id","result_"+v.id)
              .attr("class","search_result")
              // .on(vizwhiz.evt.click,function(){
              //   if (v.id.length < depths[depths.length-1]) {
              //     if (type == "bra" && v.id.substr(0,2) == "mg") {
              //       if (v.id.length == 2) {
              //         var depth = 7
              //       }
              //       else {
              //         var depth = 8
              //       }
              //     }
              //     else {
              //       var depth = depths[depths.indexOf(v.id.length)+1]
              //     }
              //     select_value(v,depth);
              //   }
              //   else {
              //     callback(data[v.id],name);
              //   }
              // })
              
            if (v.icon != selected.icon || search_term != "") {
              var search_icon = item.append("div")
                .attr("class","search_icon")
                .style("background-image","url("+v.icon+")")
              if (["wld","bra"].indexOf(type) < 0 || (type == "wld" && v.id.length != 5)) {
                search_icon.style("background-color",v.color)
              }
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
              
            if (type != "file" && searching) {
              text.append("div")
                .attr("class","search_sub")
                .html(dataviva.format.text(type+"_"+v.id.length))
            }
            
            if (v.id_ibge) {
              var sub_text = dataviva.format.text("id_ibge") + ": " + v.id_ibge.toString()
            }
            else {
              var sub_text = dataviva.format.text(type+"_id") + ": " + v.display_id.toString()
            }
            
            text.append("div")
              .attr("class","search_data")
              .html(sub_text)
            
            if (v.desc && type == "file") {
              text.append("div")
                .attr("class","search_data")
                .text(v.desc)
            }
               
            if (v[value]) {
              text.append("div")
                .attr("class","search_data")
                .text(dataviva.format.text(value)+": "+dataviva.format.number(v[value],value))
            }
            
            var buttons = item.append("div")
              .attr("class","search_buttons")
              
            if (v.id.length < depths[depths.length-1]) {
              
              if (v.id == "mg" && type == "bra") {
              
                var d = depths.indexOf(v.id.length)
                var length = depths[d+1]
                var suffix = dataviva.format.text("bra_7_plural")
              
                var b = buttons.append("input")
                  .attr("type","button")
                  .attr("id","pr")
                  .attr("value",suffix)
                  
                b.node().onclick = function(){
                  select_value(v,7)
                }
                
                leon("#pr").color(v.color)
              }
              
              var d = depths.indexOf(v.id.length)
              var length = v.id.length == 7 && type == "bra" ? 8 : depths[d+1]
              var suffix = dataviva.format.text(type+"_"+length+"_plural")
              
              var b = buttons.append("input")
                .attr("type","button")
                .attr("id","child"+v.id)
                .attr("value",suffix)
                  
              b.node().onclick = function(){
                select_value(v,length)
              }
                
              leon("#child"+v.id).color(v.color)
              
            }
            else if (type == "bra" && v.id.length == depths[depths.length-1]) {

              text.append("div")
                .attr("id","withins"+v.id)
                .attr("class","search_withins")
                .style("display","none")
                
              if (v.distance) update_distance(v.distance,v.id)

              var prox_toggles = buttons.append("div")
                .attr("class","proximity_toggles")
                
              prox_toggles.append("label")
                .attr("for","distance"+v.id)
                .html(dataviva.format.text("Municipalities within"))
                
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
      
              leon("#distance"+v.id).color(v.color)
              
            }
              
            if (!limit || v.id.length >= limit) {
              
              var b = buttons.append("input")
                .attr("type","button")
                .attr("id","select"+v.id)
                .attr("value",dataviva.format.text("select"))
                  
              b.node().onclick = function(){
                callback(data[v.id],name)
              }
                
              leon("#select"+v.id).color(v.color)
            }
          
            if (results[i+1] || i == results.length-1) {
              body.append("div")
                .attr("class","vizwhiz_tooltip_data_seperator")
            }
            
            var width = item.node().offsetWidth
            width -= parseFloat(item.style("padding-left"),10)
            width -= parseFloat(item.style("padding-right"),10)
            width -= 12
            if (search_icon) {
              width -= search_icon.node().offsetWidth
              width -= parseFloat(search_icon.style("margin-right"),10)
            }
            width -= buttons.node().offsetWidth
            text.style("max-width",width+"px")
              
          }
        
        })
    
      }
  
      set_height = function() {
        // Set height for selector_body, based off of the title height
        var parent = container.node().parentNode,
            display = d3.select(parent).style("display")
            
        if (display == "none") {
          parent.style.visibility = "hidden"
          parent.style.display = "block"
        }
        var max_height = container.node().offsetHeight
        
        max_height -= body.node().offsetTop
        max_height -= parseFloat(body.style("padding-top"),10)
        max_height -= parseFloat(body.style("padding-bottom"),10)
        max_height = Math.floor(max_height)
        if (display == "none") {
          parent.style.visibility = "visible"
          parent.style.display = "none"
        }
        body.style("height",max_height+"px")
      }
      
      var close = null,
          header = null,
          header_select_div = null,
          header_select = null, 
          bread = null, 
          icon = null, 
          title = null, 
          description = null,
          search = null, 
          body = null, 
          sort_toggles = null,
          sorter = null,
          current_depth = null,
          depth_path = [],
          searching = false;
          
      var distance_url = "/attrs/bra/munic.value/",
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
          value = sort_types[type] ? sort_types[type] : null,
          sorts = ["name"]
          
      if (type == "bra") {
        var depths = dataviva.depths(type,false)
      }
      else {
        var depths = dataviva.depths(type,true)
      }
          
      if (value) {
        sorts.push(value)
        var sorting = value
      }
      else {
        var sorting = "name"
      }
       
      d3.select(this).select(".selector").remove()
      var container = d3.select(this)
        .append("div")
          .attr("class","selector")

      var selector_load = new dataviva.ui.loading(container.node())
      selector_load.color("#ffffff")
      
      if (type != "file") {
        selector_load.text("Loading Attribute List").show()
      }
      
      if (data) {
        clean_data()
      }
      else if (lists[type]) {
        data = lists[type]
        create_elements()
      }
      else {
        d3.json("/attrs/"+type+"/")
          .header("X-Requested-With", "XMLHttpRequest")
          .get(function(error,attrs) {
            data = attrs.data
            clean_data()
          })
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
  
  util.type = function(value) {
    if (!arguments.length) return name;
    name = value
    type = value.split("_")[0]
    return util;
  }
  
  return util;
}
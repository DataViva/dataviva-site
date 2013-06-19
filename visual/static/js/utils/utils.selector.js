function Selector() {
  
  var callback,
      type = "bra",
      name = "bra",
      initial_value = "all",
      distance = 0,
      language = "en",
      lists = {};
      
  function util(selection) {
    
    selection.each(function(data) {
      
      var distance_url = "/attrs/bra/munic.value/",
          depths = dataminas.depths(type,true),
          list = [],
          search = ""
          selected = null,
          proximities = [0,30,60,90];
          
      var container = d3.select(this)
        .html("")
        .append("div")
          .attr("class","selector")
        
      var header = container.append("div").attr("class","selector_header")
      var icon = header.append("div").attr("class","selector_header_icon");
                
      var block = header.append("div").attr("class","selector_title_block")
      var title = block.append("div").attr("class","selector_title")
      
      container.attr("class",function(){
        var c = this.className
        return c ? c+" selector" : "selector"
      })
      
      if (type == "bra") {
        var proximity = block.append("div")
          .attr("id","proximity")
          .style("display","none")
          
        var group = proximity.append("div")
          .attr("class","toggle_group")
          
        proximities.forEach(function(p){
          
          group.append("a")
            .attr("class",function(){
              return p == distance ? "button active" : "button"
            })
            .html(p+"km")
            .on(vizwhiz.evt.click,function(){
              if (d3.select(this).attr("class") == "button") {
                
                // Reset previous active button and set current
                group.select(".active").attr("class","button")
                d3.select(this).attr("class","button active")
                
                distance = p;
                update_proximities();
              }
            })
            
        })
    
        var proximity_list = proximity.append("div")
          .attr("class","proximity_list")
        
      }
      
      if (["file","help"].indexOf(type) < 0) {
        
        var submit = block.append("a").attr("class","selector_submit button")
          .html("Select »")
          .on(vizwhiz.evt.click,function(){
            if (callback) {
              var obj = distance > 0
                ? vizwhiz.utils.merge({"distance": distance},selected)
                : selected;
              obj.type = name;
              window[callback](obj,name);
            }
          });
      
      }
      
      if (depths.length > 1) {

        var nav = container.append("div").attr("class","selector_nav")
        var bread = nav.append("ul").attr("class","breadcrumb")
        nav.append("input")
          .attr("type","text")
          .attr("id",name+"_search")
          .attr("class","selector_search")
          .attr("placeholder","Search");
                  
        document.getElementById(name+"_search")
          .oninput = function() { populate_list(selected) };
          
      }
      
      if (type == "help") {
        var body = container.append("iframe")
          .attr("class","selector_body")
          .attr("width","100%")
          .style("height","auto");
      }
      else {
        var body = container.append("div")
          .attr("class","selector_body")
          .style("height","auto");
      }
      
      if (type == "help") {
        
        update_header(data[0]);

        body.attr("src","/about/apps/"+data[0].id+"/?ajax=true")
          
      }
      else if (type == "file") {
        lists.file = {
          "all": {
            "color": "#768593",
            "id": "all",
            "name": format_name("download",language)
          },
          "svg": {
            "color": "#e87600",
            "id": "svg",
            "name": format_name("svg",language)
          },
          "png": {
            "color": "#0b1097",
            "id": "png",
            "name": format_name("png",language)
          },
          "pdf": {
            "color": "#c8140a",
            "id": "pdf",
            "name": format_name("pdf",language)
          },
          "csv": {
            "color": "#00923f",
            "id": "csv",
            "name": format_name("csv",language)
          }
        }
        data = lists.file;
        clean_data();
      }
      else if (data) {
        lists[type] = data;
        clean_data();
      }
      else if (lists[type]) {
        data = lists[type];
        clean_data();
      }
      else {
        
        d3.json("/attrs/"+type+"/",function(attrs) {
          
          lists[type] = attrs.data
          data = lists[type];
          
          clean_data();
      
        })
        
      }
      
      function clean_data() {
        
        if (data instanceof Array) {
          var temp_dict = {};
          data.forEach(function(d){
            temp_dict[d.id] = d;
          })
          data = temp_dict;
        }
        
        if (!data.all) {
          if (type == "bra") var c = "#009b3a";
          else var c = "#768593";
          var title = type == "bra" ? "brazil" : type
          data = vizwhiz.utils.merge(data,{"all": {
            "color": c,
            "id": "all",
            "display_id": "All",
            "name": format_name(title,language)
          }});
        }
      
        for (d in data) {
          
          if (!data[d].display_id) {
            data[d].display_id = dataminas.displayID(d,type);
          }
          
          if (data[d].id.length > depths[1]) {
            data[d].parent = d.slice(0,depths[1]);
          }
          else if (data[d].id.length == depths[0]) {
            data[d].parent = "all"
          }
          else if (data[d].id.length == depths[1]) {
            data[d].parent = d.slice(0,depths[0]);
          }
          
          data[d].icon = dataminas.icon(d,type)
        }
        
        select_value(data[initial_value]);
        
      }
      
      function select_value(x) {
        
        update_header(x);
        
        // Un-highlight previous list item, if applicable
        if (selected && !d3.select("#result_"+selected.id).empty()) {
          d3.select("#result_"+selected.id+" > .search_link")
            .style("background-color","#ffffff")
            .style("color","#333333")
        }
        
        if (!selected || x.id.length == depths[0] || x.id == "all") {
          if (depths.length > 1) {
            update_breadcrumbs(x);
          }
          populate_list(x);
        }
          
        selected = x;
        
      }
      
      function update_header(x) {
        
        // Modify header title, color, and icon
        header
          .style("background-color",x.color)
          .style("color",vizwhiz.utils.text_color(x.color))
        title.html(x.name.toTitleCase())
        icon.style("background","url("+x.icon+")")
      
        // Load distances into span if relevant
        if (type == "bra") {
          if (x.id.length == 8) {
            proximity.style("display","block")
            update_proximities();
          }
          else {
            proximity.style("display","none");
          }
        }

        // Set height, now that the header is completely updated
        set_height();
        
      }
      
      function update_proximities() {
        
        if (distance == 0) {
          proximity_list.html("")
        }
        else {
          
          var id = selected ? selected.id : initial_value
          
          var u = distance_url
            .replace("munic",id)
            .replace("value",distance)
          d3.json(u,function(raw_distances){

            var distances = [];
            raw_distances.data.forEach(function(d,i){
              var string = data[d.bra_id_dest].name
              string += "<span class='road_sign'>";
              string += d.distance;
              string += "km</span>"
              distances.push(string)
            })
          
            if (distances.length > 0) {
              proximity_list.html(distances.join(", "))
            } else {
              proximity_list.html("No municipalities within that distance.")
            }
          }).on("progress",function(){
            proximity_list.html("Loading...")
          })
      
        }
        
      }
      
      function update_breadcrumbs(x) {

        bread.selectAll("*").remove()
        if (x.id == "all") {
          bread.append("li")
            .attr("class","active")
            .html(format_name(type+"_"+depths[0],language))
        } 
        else {
          bread.append("li")
            .append("a")
              .html(format_name(type+"_"+depths[0],language))
              .on(vizwhiz.evt.click,function(){
                if (type == "bra") {
                  select_value(data.all);
                }
                else {
                  update_breadcrumbs(data.all)
                  populate_list(data.all);
                }
              })
          bread.append("span")
            .attr("class","divider")
            .html(" / ")
          bread.append("li")
            .attr("class","active")
            .html(x.name.toTitleCase().truncate(25))
        }
        
      }
      
      // Used whenever a filter list needs to be re-populated
      function populate_list(parent) {

        // Remove all current list elements
        body.selectAll("div").remove();
        
        if (depths.length > 1) {
          // Get current search box value
          search = d3.select("#"+name+"_search").node()
            .value.toLowerCase().removeAccents();
            
          // If search box value is less than 3 characters, don't use it!
          if (search.length == 0) {
            if (parent.id.length == depths[1]) var match = parent.parent
            else var match = parent.id
            // Create list by matching parent ids
            list = d3.values(data).filter(function(v){
              return v.parent == match;
            })
          }
          // Search box contains more than 3 characters, so do this stuff!
          else {
          
            // Create master list by matching both name and id
            list = d3.values(data).filter(function(v){
              return (v.name.toLowerCase().removeAccents().indexOf(search) >= 0 
                      || v.id.indexOf(search) >= 0)
            })
          
            var list_new = []
        
            list.forEach(function(v,i){
          
              // If list item is not in the specified depth levels, 
              // add it's parent to the new "list_new" array
              if (depths.indexOf(v.id.length) < 0) {
                list_new.push(data[v.parent]);
              }
          
            })
                    
            list = list.concat(list_new)
        
            // Remove duplicates
            list = list.filter(function(elem, pos) {
                return list.indexOf(elem) == pos;
            })
                      
          }
          
          // Remove elements that aren't in the specified depth levels
          list = list.filter(function(v){
            if (v) {
              return v.id.length == depths[0] || v.id.length == depths[1]
            }
            else {
              return null;
            }
          })
            
        }
        else {
          list = d3.values(data).filter(function(v){
            return v.id != "all";
          });
        }
        
        list.sort(function(a, b){
          
          if (type == "bra") {
            var a_first = parseInt(a.population,10)
            var b_first = parseInt(b.population,10)
          }
          else if (parent.parent == "all" && type != "wld") {
            var a_first = d3.rgb(a.color).hsl().h
            var b_first = d3.rgb(b.color).hsl().h
            if (d3.rgb(a.color).hsl().s == 0) a_first = 361
            if (d3.rgb(b.color).hsl().s == 0) b_first = 361
          } else {
            var a_first = a.id.substr(0,depths[0])
            var b_first = b.id.substr(0,depths[0])
          }
          
          if(a_first != b_first) {
            if (typeof a_first === "string") return (a_first.localeCompare(b_first));
            else return (b_first - a_first);
          } else {
            var a_second = a.name.toTitleCase()
            var b_second = b.name.toTitleCase()
            return (a_second.localeCompare(b_second))
          }
        })
        
        add_results(40);
        
        body.on("scroll",function(){
          if(body.node().scrollTop + body.node().clientHeight + 10 >= body.node().scrollHeight) {
            if (list.length > 0) add_results(40);
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
          
            var link = item.append("div")
              .attr("class","search_link")
              .on(vizwhiz.evt.over,function(){
                d3.select(this)
                  .style("background-color",v.color)
                  .style("color",vizwhiz.utils.text_color(v.color))
              })
              .on(vizwhiz.evt.out,function(){
                if (v.id != selected.id) {
                  d3.select(this)
                    .style("background-color","#ffffff")
                    .style("color","#333333")
                }
              })
              .on(vizwhiz.evt.click,function(){
                if (type == "file") {
                  window[callback](v,name);
                }
                else {
                  select_value(v);
                }
              })
                        
            var item_icon = link.append("div")
              .attr("class","search_icon")
              .style("background-color",v.color)
              .style("background-image","url("+v.icon+")")
          
            var name = v.name.toTitleCase().truncate(65)
            if (search.length >= 3) {
              name = name.replace(search,"<b>"+search+"</b>")
              name = name.replace(search.toTitleCase(),"<b>"+search.toTitleCase()+"</b>")
            }
          
            link.append("span")
              .attr("class","search_title")
              .html(name)
                        
            link.append("span")
              .attr("class","search_id")
              .text(v.display_id)
              
          }
        
        })
    
      }
  
      function set_height() {
        // Set height for selector_body, based off of the title height
        var display = container.style("display")
        if (display == "none") container.style("visibility","hidden").style("display","block")
        
        var max_height = parseInt(container.style("height"),10)
        max_height -= header.node().offsetHeight
        if (depths.length > 1) {
          max_height -= nav.node().offsetHeight
        }
        max_height -= parseInt(body.style("padding-top"),10)
        max_height -= parseInt(body.style("padding-bottom"),10)
        max_height = Math.round(max_height)
        
        if (display == "none") container.style("visibility","visible").style("display","none")
        body.style("height",max_height+"px")
      }
      
      
    })
  }
  
  util.initial_value = function(value) {
    if (!arguments.length) return initial_value;
    initial_value = value;
    return util;
  }
  
  util.distance = function(value) {
    if (!arguments.length) return distance;
    distance = value;
    return util;
  }
  
  util.type = function(value) {
    if (!arguments.length) return name;
    name = value
    type = name == "bra2" ? "bra" : name;
    return util;
  }
  
  util.callback = function(value) {
    if (!arguments.length) return callback;
    callback = value;
    return util;
  }
  
  util.language = function(value) {
    if (!arguments.length) return language;
    language = value;
    return util;
  }
  
  return util;
}
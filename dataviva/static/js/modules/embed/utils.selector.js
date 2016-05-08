function Selector() {

  var callback,
      type = "bra",
      name = "bra",
      initial_value = "all",
      distance = 0,
      limit = null,
      header_color = "#333";

  var lists = {
    "file": {
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
  };

  function util(selection) {

    selection.each(function(data) {

      get_article = function(x) {
        var connect = "in";
        if (dataviva.language == "pt") {
          if (x.id == "all") connect = "do";
          else if (x.article_pt && x.gender_pt == "m") connect = "no";
          else if (x.article_pt && x.gender_pt == "f") connect = "na";
          else connect = "em";
          if (x.plural_pt && x.article_pt) connect += "s";
        }
        return connect;
      };

      update_distance = function(dist,id) {

        if (typeof id === "function") {
          id = id.container(Object).id.substr(5);
        }

        data[id].distance = dist;

        var div = d3.select("#withins"+id);

        if (dist > 0) {

          div.style("display","block");

          var u = distance_url
            .replace("munic",id)
            .replace("value",dist);

          d3.json("/"+u.substr(1)+"?lang="+dataviva.language)
            .header("X-Requested-With", "XMLHttpRequest")
            .get(function(error,raw_distances){
              var distances = [];
              raw_distances.data.forEach(function(d,i){
                if (i !== 0) {
                  var string = data[d.bra_id_dest].name;
                  string += " ("+d.distance+"km)";
                  distances.push(string);
                }
              });

              if (distances.length > 0) {
                div.html(dataviva.format.text("Including")+" "+distances.join(", "));
              } else {
                div.html(dataviva.format.text("No municipalities within that distance."));
              }

            });

        }
        else {
          div.style("display","none");
        }
      };

      populate_list = function(parent,sort) {

        if (sort) sorting = sort;

        // Remove all current list elements
        body.selectAll("div").remove();

        // Get current search box value
        search_term = search.node().value.toLowerCase().removeAccents();
        searching = search_term.length > 1;

        // User is searching, so do this stuff!
        if (searching) {

          // update_header(search_term);
          depth_list = [];
          other_list = [];
          for (var i in data) {
            var d = data[i];
            if (d.id !== "all" && d.search.indexOf(search_term) >= 0) {
              if (d.id.length === current_depth && (parent.id === "all" || d.parents.indexOf(parent.id) >= 0)) {
                depth_list.push(d);
              }
              else {
                other_list.push(d);
              }
            }
          }

          // Sort final generated list
          depth_list.sort(function(a, b){

            var a_first = a[sorting];
            var b_first = b[sorting];

            if (a_first != b_first) {
              if (typeof a_first === "string") return (a_first.localeCompare(b_first));
              else return (b_first - a_first);
            }
            else {
              var a_second = a.name.toTitleCase();
              var b_second = b.name.toTitleCase();
              return (a_second.localeCompare(b_second));
            }
          });

          // Sort final generated list
          other_list.sort(function(a, b){

            var a_first = a[sorting];
            var b_first = b[sorting];

            if (a_first != b_first) {
              if (typeof a_first === "string") return (a_first.localeCompare(b_first));
              else return (b_first - a_first);
            }
            else {
              var a_second = a.name.toTitleCase();
              var b_second = b.name.toTitleCase();
              return (a_second.localeCompare(b_second));
            }
          });

          var no_results = {"error": dataviva.dictionary.search_empty};

          var prefix = dataviva.dictionary[type+"_"+current_depth+"_plural"],
              connect,
              depth_title = prefix,
              other_title = dataviva.dictionary.other + " " + dataviva.dictionary[type+"_plural"];
          if (type === "bra") {
            connect = " " + get_article(parent) + " ";
            depth_title += connect + parent.name.toTitleCase();
            var all_connect = " " + get_article(data.all) + " ";
            other_title += all_connect + data.all.name.toTitleCase();
          }
          else if (parent.id !== "all") {
            connect = " " + get_article(parent) + " ";
            depth_title += connect + parent.name.toTitleCase();
          }
          depth_list.unshift({"title": depth_title});
          other_list.unshift({"title": other_title});

          if (depth_list.length === 1 && other_list.length === 1) {
            list = [no_results];
          }
          else {
            if (depth_list.length === 1) depth_list.push(no_results);
            if (other_list.length === 1) other_list.push(no_results);
            list = depth_list.concat(other_list);
          }

        }
        else {

          update_header(selected);

          if (type == "file") {
            list = d3.values(data).filter(function(v){
              return v.id != "all";
            });
          }
          else {
            // Create list by matching parent ids
            list = d3.values(data).filter(function(v){
              var child = true;
              if (parent.id != "all") {
                child = v.parents.indexOf(parent.id) >= 0;
              }
              return v.id.length === current_depth && v.id != "all" && child;
            });
          }

          // Sort final generated list
          list.sort(function(a, b){

            if (type === "bra" && current_depth === 3) {
                var a_state = a.id;
                var b_state = b.id;
              if (a_state !== b_state && [a_state, b_state].indexOf("4mg") >= 0) {
                return a_state === "4mg" ? -1 : 1;
              }
            }

            var a_first = a[sorting];
            var b_first = b[sorting];

            if (a_first != b_first) {
              if (typeof a_first === "string") return (a_first.localeCompare(b_first));
              else return (b_first - a_first);
            }
            else {
              var a_second = a.name.toTitleCase();
              var b_second = b.name.toTitleCase();
              return (a_second.localeCompare(b_second));
            }
          });

        }

        parent = container.node().parentNode;
        var display = d3.select(parent).style("display");

        if (display == "none") {
          parent.style.visibility = "hidden";
          parent.style.display = "block";
        }

        // Initially add some results
        add_results();

        if (display == "none") {
          parent.style.visibility = "visible";
          parent.style.display = "none";
        }

        // Add more results on scroll
        body.on("scroll",function(){
          if(this.scrollTop + this.clientHeight + 10 >= this.scrollHeight) {
            if (list.length > 0) add_results();
          }
        });

        body.node().scrollTop = 0;

      };

      select_value = function(x,depth) {

        search.node().value = "";

        if (depths.indexOf(x.id.length) === depths.length-1) {
          if (depths.length === 1) x = data.all;
          else x = data[x.parents[0]];
        }

        selected = x;

        if (depth === undefined) depth = starting_depth();
        else if (typeof depth === "string") depth = parseFloat(depth);

        current_depth = depth;

        if (depths.length > 1) {

          bread.select("a").remove();
          if (x.id != "all") {
            var remove_link = bread.append("a")
              .attr("class","site_crumb")
              .text(dataviva.dictionary.remove_filter)
              .on(d3plus.client.pointer.click,function(){
                search.node().value = "";
                select_value(data.all);
              })
              .on(d3plus.client.pointer.over,function(){
                this.style.color = d3plus.color.legible(x.color);
              })
              .on(d3plus.client.pointer.out,function(){
                this.style.color = "#888";
              }).append("i").attr("class", "fa fa-close");
          }

        }

        populate_list(x,sorting);

      };

      starting_depth = function() {

        var depth = 0;
        if (initial_value !== "all") {

          var d = depths.indexOf(initial_value.length);
          if (d + 1 === depths.length) {
            depth = depths[d];
          }
          else {
            depth = depths[d+1];
          }

        }
        else {
          depth = depths[depths.length-1];
        }

        return depth;

      };

      create_elements = function() {

        header = container.append("div").attr("class","selector_header");

        icon = header.append("div").attr("class","selector_header_icon");

        title_div = header.append("div").attr("class","selector_title_div");

        title = title_div.append("div").attr("class","selector_title");

        description = title_div.append("div").attr("class","selector_description");

        bread = title_div.append("div").attr("class","breadcrumb");

        sort_toggles = header.append("div").attr("class","selector_toggles");

        if (sorts.length > 1) {

          sort_toggles.append("legend")
            .attr("id","selector_sort")
            .html(dataviva.format.text("sort"));

          sorts.forEach(function(s){
            var input = sort_toggles.append("input")
              .attr("type","radio")
              .attr("id","selector_sort_"+s)
              .attr("value",s)
              .attr("name","selector_sort")
              .attr("onclick","populate_list(selected,this.value)");
            if (s == sorting) input.attr("checked","checked");
            sort_toggles.append("label")
              .attr("for","selector_sort_"+s)
              .html(dataviva.format.text(s));
          });

          sorter = leon("$selector_sort").color(dataviva.color);
        }

        header_select_div = sort_toggles.append("div").attr("id","header_select_div");

        var b = header_select_div.append("input")
          .attr("type","button")
          .attr("id","header_select")
          .attr("value",dataviva.format.text("select"));

        header_select = leon("#header_select");

        depth_select = header.append("div").attr("class", "selector_depth");

        search = header.append("input")
          .attr("type","text")
          .attr("id",name+"_search")
          .attr("class","leon text")
          .attr("placeholder",dataviva.format.text("search"));

        searcher = leon("#"+name+"_search").color(dataviva.color).size("medium");

        search.node().oninput = function() { populate_list(selected); };

        if (type == "file") {
          search.style("display", "none");
          depth_select.style("display", "none");
        }

        body = container.append("div")
          .attr("class","selector_body")
          .style("height","auto");

        selector_load.hide();

        var depth = 0;
        if (initial_value !== "all") {

            var d = depths.indexOf(initial_value.length);
            if (d === depths.length - 1) {
              initial_value = initial_value.slice(0,depths[d-1]);
            }

        }

        select_value(data[initial_value]);

      };

      search_string = function(d) {
        var strings = ["name","id","desc","keywords"];
        var str = "";
        for (var s = 0; s < strings.length; s++) {
          var val = d[strings[s]];
          if (val) {
            if (s) str += "_";
            str += val.toLowerCase().removeAccents();
          }
        }
        return str;
      };

      clean_data = function() {

        if (data instanceof Array) {

          if (type === "bra") {
            data = data.filter(function(d){
              return d.id.substr(0,1) !== "0";
            });
          }
          else {
            data = data.filter(function(d){
              return d.available;
            });
          }

          data = data.reduce(function(obj, d){
            d.search = search_string(d);
            obj[d.id] = d;
            return obj;
          }, {});

        }
        else {
          var temp_dict = {};
          for (var d in data) {
            if (d.available) {
              d.search = search_string(d);
              temp_dict[d] = data[d];
            }
          }
          data = temp_dict;
        }

        if (!data.all) {
          var c = "#ffffff";
          if (type == "bra") c = "#009b3a";
          var title = type == "bra" ? "brazil" : type;
          data.all = {
            "color": c,
            "id": "all",
            "display_id": "All",
            "name": dataviva.format.text(title),
            "search": dataviva.format.text(title).toLowerCase().removeAccents()
          };
        }

        for (var a in data) {

          if (!data[a].display_id) {
            data[a].display_id = dataviva.displayID(a,type);
          }

          var depth = depths.indexOf(a.length);

          if (a == "all") {
            data[a].parents = ["none"];
          }
          else {
            data[a].parents = [];
            for (var di = 0; di <= depth-1; di++) {
              data[a].parents.push(a.slice(0,depths[di]));
            }
          }

          if (!data[a].icon) data[a].icon = dataviva.icon(a,type,data[a].color);
        }

        lists[type] = data;
        create_elements();

      };

      get_depths = function(x) {
        var depth_toggles = depths.slice();
        if (x.id !== "all") {
          depth_toggles = depth_toggles.slice(depth_toggles.indexOf(x.id.length) + 1);
        }
        return depth_toggles;
      }

      update_header = function(x) {

        header_color = "#333333";
        if (typeof x === "string") {
          header_select_div.style("display","none");
          icon.style("display","none");
          title.text(dataviva.format.text("search_results"));
        }
        else {

          if (x.color !== "#ffffff") {
            header_color = x.color;
          }

          icon.style("display", "inline-block");

          if (x.icon) icon.style("background-image","url('"+x.icon+"')");

          if (["wld","bra"].indexOf(type) < 0 || (type == "wld" && x.id.length != 5)) {
            icon.style("background-color",x.color);
          }

          if (type !== "file" && (x.id !== "all" || type === "bra")) {
            header_select_div.style("display","inline-block");
            header_select.leons.header_select.node.onclick = function(){
              selector_load.text(dataviva.format.text("wait")).show();
              callback(data[x.id],name);
            };
            header_select.color(x.color);
          }
          else {
            header_select_div.style("display","none");
          }

          var prefix;
          if (type === "file") {
            prefix = x.name;
          }
          else if (type === "bra") {
            prefix = dataviva.format.text("bra_"+current_depth+"_plural");
          }
          else {
            prefix = dataviva.format.text(type+"_plural");
          }

          if (x.id == "all" && type != "bra") {
            title.text(prefix);
          }
          else {
            title.text(x.name.toTitleCase());
            // var connect = "in";
            // if (dataviva.language == "pt") {
            //   if (x.id == "all") connect = "do";
            //   else if (x.article_pt && x.gender_pt == "m") connect = "no";
            //   else if (x.article_pt && x.gender_pt == "f") connect = "na";
            //   else connect = "em";
            //   if (x.plural_pt && x.article_pt) connect += "s";
            // }
            // title.text(prefix+" "+connect+" "+x.name.toTitleCase());
          }

          if (x.desc && type == "file") {
            description.text(x.desc);
          }
          // else if (x.id !== "all"){
          //   description.text(dataviva.dictionary[type+"_"+x.id.length]);
          // }
          else {
            description.text("");
          }

        }

        var close = d3.select(container.node().parentNode).select(".selector_close");
        if (close.node()) {
          close.style("background-color", header_color);
        }

        if (sorter) {
          sorter.color(header_color);
        }
        searcher.color(header_color);

        if (type !== "file") {
          depth_select.html("");
          var depth_toggles = get_depths(x);

          if (depth_toggles.length > 1) {

            // depth_select.append("legend")
            //   .attr("id","selector_depth_toggle")
            //   .html(dataviva.dictionary.showing);

            depth_toggles.forEach(function(d){
              var input = depth_select.append("input")
                .attr("type","radio")
                .attr("id","selector_depth_"+d)
                .attr("value",d)
                .attr("name","selector_depth_toggle")
                .attr("onclick","select_value(selected,this.value)");
              if (d == current_depth) input.attr("checked","checked");
              depth_select.append("label")
                .attr("for","selector_depth_"+d)
                .html(dataviva.dictionary[type+"_"+d+"_plural"]);
            });

            leon("$selector_depth_toggle").color(header_color);
          }

        }

        var hw = header.node().offsetWidth;
        hw -= icon.node().offsetWidth;
        hw -= sort_toggles.node().offsetWidth;
        hw -= 40;

        if (hw > 0) title.style("max-width",hw+"px");

        // Set height, now that the header is completely updated
        set_height();

      };

      add_results = function() {

        var amount = parseFloat(body.style("height"), 10)/40;

        var results = [];
        for (var i = 0; i < amount; i++) {
          results.push(list.shift());
        }

        results.forEach(function(v,i){

          if (v && v.title) {
            var item = body.append("div")
              .attr("class","search_header")
              .text(v.title);
            if (i) {
              item.style("margin-top", "18px")
            }
          }
          else if (v && v.error) {
            body.append("div")
              .attr("class","search_error")
              .text(v.error);
          }
          else if (v) {

            var item = body.append("div")
              .attr("id","result_"+v.id)
              .attr("class","search_result");
              // .on(d3plus.client.pointer.click,function(){
              //   if (v.id.length < depths[depths.length-1]) {
              //     if (type == "bra" && v.id.substr(0,2) == "4mg") {
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
                      // selector_load.text(dataviva.format.text("wait")).show()
              //     callback(data[v.id],name);
              //   }
              // })

            var search_icon = false;
            if (v.icon && (v.icon != selected.icon || search_term !== "")) {
              search_icon = item.append("div")
                .attr("class","search_icon")
                .style("background-image","url("+v.icon+")");
              if (["wld","bra"].indexOf(type) < 0 || (type == "wld" && v.id.length != 5)) {
                search_icon.style("background-color",v.color);
              }
            }

            var title = v.name.toTitleCase().truncate(65);
            if (search.length >= 3) {
              title = title.replace(search,"<b>"+search+"</b>");
              title = title.replace(search.toTitleCase(),"<b>"+search.toTitleCase()+"</b>");
            }

            var text = item.append("div")
              .attr("class","search_text");

            text.append("div")
              .attr("class","search_title")
              .style("color",d3plus.color.legible(v.color))
              .html(title);

            if (type != "file" && searching) {

              if(type == "bra" && v.id.length > 3) {
                stateInfo = v.id.substr(1,2).toUpperCase();
                extrainfo = dataviva.format.text(type+"_"+v.id.length)+" "+dataviva.format.text("in")+" "+stateInfo;
              } else {
                extrainfo = dataviva.format.text(type+"_"+v.id.length);
              }

              text.append("div")
                .attr("class","search_sub")
                .html(extrainfo);
            }

            var sub_text;
            if (v.id_ibge) {
              sub_text = dataviva.format.text("id_ibge") + ": " + v.id_ibge.toString();
            }
            else if (type != "file") {
              sub_text = dataviva.format.text(type+"_id") + ": " + v.display_id.toString();
            }

            text.append("div")
              .attr("class","search_data")
              .html(sub_text);

            if (v.desc && type == "file") {
              text.append("div")
                .attr("class","search_data")
                .text(v.desc);
            }

            if (v[value]) {
              text.append("div")
                .attr("class","search_data")
                .text(dataviva.format.text(value)+": "+dataviva.format.number(v[value],{"key": value}));
            }

            var buttons = item.append("div")
              .attr("class","search_buttons");

            var button_depths = get_depths(v);

            if (v.id.length < depths[depths.length-1]) {

              var depth_links = text.append("div")
                .attr("class", "selector_depth_links")
                .text(dataviva.dictionary.show+":");

              button_depths.forEach(function(bd){
                depth_links.append("a")
                  .text(dataviva.dictionary[type+"_"+bd+"_plural"])
                  .on("click", function(){
                    select_value(v, bd);
                  });
              });

            }
            else if (type === "bra") {

              if (v.distance) update_distance(v.distance,v.id);

              var prox_toggles = buttons.append("div")
                .attr("class","proximity_toggles");

              var proxData = proximities.map(function(p){
                return {"text": p+"km", "value": p};
              });

              var proxFocus = v.distance || proxData[0].value;

              d3plus.form()
                .container({
                  "id": "prox_"+v.id,
                  "value": prox_toggles
                })
                .title(dataviva.format.text("Municipalities within"))
                .data(proxData)
                .focus(proxFocus, update_distance)
                .ui({"margin": 0})
                .type("drop")
                .id("value")
                .text("text")
                .draw();

            }

            if ((!limit || v.id.length >= limit)) {

              var b = buttons.append("input")
                .attr("type","button")
                .attr("id","select"+v.id)
                .attr("value",dataviva.format.text("select"))
                .node().onclick = function(){

                    val = d3.select("#distance"+v.id);

                    if(!val.empty()) {
                        //if there is distance selection
                        update_distance(val.property("value"),v.id);
                    }

                            selector_load.text(dataviva.format.text("wait")).show();
                        callback(data[v.id],name);

                };

              leon("#select"+v.id).color(v.color);

            }

            if (results[i+1] || i == results.length-1) {
              body.append("div")
                .attr("class","d3plus_tooltip_data_seperator");
            }

            if (type == "bra" && v.id.length == depths[depths.length-1]) {

              item.append("div")
                .attr("id","withins"+v.id)
                .attr("class","search_withins")
                .style("display","none");

            }

            var width = item.node().offsetWidth;
            width -= parseFloat(item.style("padding-left"),10);
            width -= parseFloat(item.style("padding-right"),10);
            width -= 12;
            if (search_icon) {
              width -= search_icon.node().offsetWidth;
              width -= parseFloat(search_icon.style("margin-right"),10);
            }
            width -= buttons.node().offsetWidth;
            text.style("max-width",width+"px");

          }

        });

      };

      set_height = function() {
        // Set height for selector_body, based off of the title height
        var parent = container.node().parentNode,
            display = d3.select(parent).style("display");

        if (display == "none") {
          parent.style.visibility = "hidden";
          parent.style.display = "block";
        }
        var max_height = container.node().offsetHeight;

        max_height -= body.node().offsetTop;
        max_height -= parseFloat(body.style("padding-top"),10);
        max_height -= parseFloat(body.style("padding-bottom"),10);
        max_height = Math.floor(max_height);
        if (display == "none") {
          parent.style.visibility = "visible";
          parent.style.display = "none";
        }
        body.style("height",max_height+"px");
      };

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
          searching = false;

      var distance_url = "/attrs/bra/munic.value/",
          list = [],
          search_term = ""
          selected = null,
          proximities = [0,30,60,90],
          sort_types = {
            "bra": "population",
            "hs": "export_val",
            "wld": "export_val",
            "cbo": "num_jobs",
            "cnae": "num_jobs",
            "course_hedu": "enrolled",
            "university": "enrolled",
            "course_sc": "enrolled",
            "school": "enrolled",
          },
          value = sort_types[type] ? sort_types[type] : null,
          sorts = ["name"]

      var depths = dataviva.depths(type);

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
        selector_load.text(dataviva.format.text("loading_attrs")).show()
      }

      if (data) {
        clean_data()
      }
      else if (lists[type]) {
        data = lists[type]
        create_elements()
      }
      else {
        function loadattrs() {
          var attr_url = "/attrs/"+type+"/?lang="+dataviva.language;
          localforage.getItem(attr_url, function(error, attrs){
            if (attrs)  {
              data = attrs.data;
              clean_data();
            }
            else {
              d3.json(attr_url)
                .header("X-Requested-With", "XMLHttpRequest")
                .get(function(error, attrs) {
                  localforage.setItem(attr_url, attrs);
                  data = attrs.data;
                  clean_data();
                })
            }
          })
        }
        localforage.getItem("version", function(error, version){
          if (error || version !== dataviva.attr_version) {
            localforage.clear(function(){
              localforage.setItem("version", dataviva.attr_version);
              loadattrs();
            })
          }
          else {
              loadattrs();
          }

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
    if (value.indexOf("_id") > 0) {
      type = value.slice(0,value.indexOf("_id"));
    }
    else if (value.charAt(value.length - 2) === "_") {
      type = value.slice(0,value.length-2);
    }
    else {
      type = value;
    }
    return util;
  }

  return util;
}
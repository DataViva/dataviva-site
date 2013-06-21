var visual = {};
visual.slide = {};
visual.popover = {};
visual.slide.timing = 0.75, // timing of page slides, in seconds

visual.ui = {}

visual.ui.tooltip = function(id,kill) {
  if (kill) {
    vizwhiz.tooltip.remove(id);
  }
  else {
    var item = document.getElementById(id),
        size = item.getBoundingClientRect()
    vizwhiz.tooltip.remove(id);
    vizwhiz.tooltip.create({
      "x": size.left+size.width/2,
      "y": size.top+size.height/2,
      "offset": size.height/2,
      "arrow": true,
      "description": id,
      "width": "auto",
      "id": id
    })
  }
}

// Returns a random number between the min and max passed to the function
visual.random = function(min,max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

visual.download = function(type, title) {
  
  var form = document.getElementById("svgform");
  
  if(type == "csv"){
    // console.log(app.csv_data()[0])
    // console.log(tooltip_info)
    
    var columns = app.csv_data()[0].filter(function(e,i,a){
      return tooltip_info.indexOf(e) > -1;
    })
    
    // console.log(app.csv_columns(columns).csv_data())
    // d3.csv.format([{'asdf':4, 'wwww':45}])
    
    form['data'].value = d3.csv.formatRows(app.csv_columns(columns).csv_data());
  }
  else {
    // Add necessary name space junk and get raw node
    var svg = d3.select("svg")
      .attr("version", 1.1)
      .attr("xmlns", "http://www.w3.org/2000/svg")
      .node()
    // Extract the data as SVG text string
    var svg_xml = (new XMLSerializer).serializeToString(svg);
    form['data'].value = svg_xml;
  }
  // Submit the <FORM> to the server.
  // The result will be an attachment file to download.
  form['output_format'].value = type;
  form['title'].value = title;
  form.submit();
}

visual.displayID = function(id,type) {

  if (id) {
    if (["hs","wld"].indexOf(type) >= 0 && id.length > 2) {
      return id.slice(2).toUpperCase();
    }
    else if (["isic"].indexOf(type) >= 0) return id.slice(1);
    else return id.toUpperCase();
  }
  else {
    return id;
  }
  
}

visual.icon = function(id,type) {
  
  if (["isic","cbo","hs","bra"].indexOf(type) >= 0 && id != "all"){
    var depth = visual.depths(type)[0],
        id = id.slice(0,depth);
  }
  else {
    var id = id;
  }
  
  return "/static/img/icons/"+type+"/"+type+"_"+id+".png";
  
}

visual.depths = function(type,flatten) {
  if (type == "isic") var array = [1,3,5];
  else if (type == "cbo") var array = [1,2,3,4];
  else if (type == "hs") var array = [2,4,6];
  else if (type == "bra") var array = [2,4,6,8];
  else if (type == "wld") var array = [2,5];
  else var array = [0];
  
  if (flatten && array.length > 1) {
    return [array[0],array[array.length-1]];
  }
  else {
    return array;
  }
  
}


/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
visual.toggle = function(name) {

  var radios = Array.prototype.slice.call( document.getElementsByName(name) ),
      parent = d3.select(radios[0].parentNode),
      label = parent.node().getElementsByTagName("legend")[0];
  
  if (label) {
    label.style.display = "none";
  
    parent.append("div")
      .attr("class","button_label")
      .html(label.innerHTML)
  }
    
  var group = parent.append("div").attr("class","toggle_group")
  
  var labels = radios[0].parentNode.getElementsByTagName("label");
  radios.forEach(function(radio,index){
    for (var i = 0; i < labels.length; i++) {
        if (labels[i].htmlFor.toLowerCase() == radio.value.toLowerCase()) {
            // It exists!
            radio.label = labels[i];
            // Hide it
            radio.label.style.display = "none";
            radio.style.display = "none";
            // Create custom label
            var button = group.append("a")
              .attr("id", radio.value)
              .html(radio.label.innerHTML)

            if (radio.checked) {
              button.attr("class","button active")
            } else {
              button.attr("class","button")
                .on(vizwhiz.evt.click, function(){ button_click(this) })
            }
        }
    }
  })
  
  function button_click(btn) {
    if (btn.id == "false") var value = false;
    else if (btn.id == "true") var value = true;
    else var value = btn.id;
    var radio = radios.filter(function(r){ return r.value == btn.id; })[0]
    radio.checked = true;
    if (radio.onclick) radio.onclick(value);
    
    parent.select(".active")
      .attr("class","button")
      .on(vizwhiz.evt.click,function(){button_click(this)})
    d3.select(btn).attr("class","button active").on(vizwhiz.evt.click,null)
  }
  
}

/*
CUSTOM DROPDOWN MENU CREATOR
Creates a custom dropdown menu, when passed the id of a <select> input
*/
visual.dropdown = function(id) {
  
  var select = document.getElementById(id.slice(1)),
      initial = select.options[select.selectedIndex],
      options = Array.prototype.slice.call( select.children ),
      arrow = options.length > 1 ? "<i class='icon-caret-down'></i>" : "";
      
  // Hide original <select> HTML
  select.style.display = "none";
  
  // Create new container <div> before <select> element
  var group = d3.select(select.parentNode)
    .insert("div",id)
    .attr("id",select.id+"_dropdown")
    .attr("class","dropdown_group")
  
  // Find label for <select>, if it exists
  var labels = document.getElementsByTagName('label');
  for (var i = 0; i < labels.length; i++) {
      if (labels[i].htmlFor == id.slice(1)) {
          // It exists!
          select.label = labels[i];
          // Hide it
          select.label.style.display = "none";
          // Create custom label
          group.append("div")
            .attr("class","button_label")
            .html(select.label.innerHTML)
      }
  }
  
  // Create <a> button in container <div>
  var button = group.append("a")
    .attr("class","button")
    .style("z-index",1001)
    .html(initial.innerHTML+arrow)
    .on(vizwhiz.evt.click,function(){
      if (options.length > 1) {
        var d = dropdown.style("visibility")
        if (d == "hidden") dropdown_show();
        else dropdown_hide(dropdown);
      }
    })

  // Create hidden dropdown menu
  var dropdown = group.append("div")
    .attr("class","dropdown")

  // Add <option> tags as <a> tags inside hidden dropdown <div>
  options.forEach(function(option,index){
    var a = dropdown.append("a")
      .attr("id",option.value)
      .html(option.innerHTML)
      .on(vizwhiz.evt.click,function(){
      
        // Hide dropdown on click of any <option>
        dropdown_hide(dropdown);
      
        // Only change things if it is not the selected <option>
        if (this.className != "selected") {
        
          // Apply "selected" class to new selected <option>
          dropdown.select(".selected").attr("class",null);
          this.className = "selected";
        
          // Change value of hidden <select> input
          select.selectedIndex = index;

          // Change content of button
          button.html(this.innerHTML+arrow);
          // Call onchange function, if it exists
          if (select.onchange) select.onchange(this);
        }
      })
    if (select.value == option.value) {
      a.attr("class","selected")
    }
  })

  var hide_height = "-"+button.style("height");
  var dropdown_margin = dropdown.style("margin-top");
  
  dropdown
    .style("margin-top",hide_height)
    .style("left",button.node().offsetLeft+"px")
  
  function dropdown_show() {
    
    // Close any other open dropdowns
    d3.selectAll(".dropdown")
      .each(function(){
        if (this.parentNode.id != group.attr("id")) {
          dropdown_hide(d3.select(this));
        }
      })
      
    dropdown
      .style("visibility","visible")
      .style("opacity",1)
      .style("margin-top",dropdown_margin)
      
    event.stopPropagation();
    
    d3.select("html").on(vizwhiz.evt.click,function(){
      dropdown_hide(dropdown);
      d3.select("html").on(vizwhiz.evt.click,null);
    })
  }
  
  function dropdown_hide(d) {
    
    // Fade out dropdown
    d
      .style("opacity",0)
      .style("margin-top",hide_height)
      
    // Get transition-duration, in milliseconds
    var timing = parseFloat(dropdown.style("transition-duration"),10)*1000
    
    // Set display to none after transition is complete
    setTimeout(function(){
      d.style("visibility","hidden")
    },timing)
  }
  
}

visual.popover.create = function(params) {
  
  var id = params.id ? params.id : "popover",
      pop_width = params.width ? params.width : "50%",
      pop_height = params.height ? params.height : "50%";
  
  if (d3.select("#popover_mask").empty()) {
    d3.select("body").append("div")
      .attr("id","popover_mask")
      .on(vizwhiz.evt.click,function(){
        visual.popover.hide();
      })
  }
  
  if (pop_width.indexOf("%") > 0) {
    var w_px = (parseFloat(pop_width,10)/100)*window.innerWidth;
  }
  else {
    var w_px = pop_width;
  }
  if (pop_height.indexOf("%") > 0) {
    h_px = (parseFloat(pop_height,10)/100)*window.innerHeight;
  }
  else {
    var h_px = pop_height;
  }
  
  var margin_left = ((w_px/2)/window.innerWidth)*100
  
  d3.select("body").append("div")
    .attr("id",id)
    .attr("class","popover")
    .style("width",pop_width)
    .style("height",pop_height)
    .style("left","50%")
    .style("top","50%")
    .style("margin-left",-margin_left+"%")
    .style("margin-top",-h_px/2+"px")
  
}

visual.popover.show = function(id) {
  
  d3.select("#popover_mask")
    .style("display","block")
    .style("opacity",0.75);
    
  d3.select(id)
    .style("display","block")
    .style("opacity",1);
  
  visual.resize();
  
}

visual.popover.hide = function(id) {
  
  if (id) var popover = d3.select(id)
  else var popover = d3.selectAll(".popover")

  popover.each(function(){
    
      if (d3.select(this).style("display") != "none") {
        
        var p = d3.select(this)

        d3.select("#popover_mask").style("opacity",0);
        p.style("opacity",0);
    
        setTimeout(function(){
          p.style("display","none")
          d3.select("#popover_mask").style("display","none")
        },250)
        
      }
      
    })

}

/* Generates a Sabrina avatar
Variables to pass:
parent = d3 selected container
outfit = "casual","worker","travel","preppy","lab"
presenting = true,false
emotion = "smile","smirk","scared","surprised"
blink = true,false
*/
visual.sabrina = function(params) {
  // Available styles
  var outfits = ["casual","worker","travel","preppy","lab"],
      hats = ["glasses","santa","worker"],
      emotions = ["smile","smirk","scared","surprised"]
  
  var outfit = outfits.indexOf(params.outfit) >= 0 ? params.outfit : "casual",
      presenting = params.presenting ? "_presenting" : "",
      parent = params.div ? params.div : d3.select("#container"),
      emotion = emotions.indexOf(params.emotion) >= 0 ? params.emotion : "smile",
      blink = params.blink ? params.blink : true,
      blink_timing = 200,
      height = 320, // height as a percentage of parent width
      body_size = {"width": 520, "height": 1100}, // corresponds to image file
      eye_size = {"width": 280, "height": 250}, // corresponds to image file
      mouth_size = {"width": 240, "height": 240}, // corresponds to image file
      hat_size = {"width": 300, "height": 190} // corresponds to image file
     
  // Should be in CSS
  var image_style = {
    "display": "block",
    "height": "0",
    "background-size": "100% 100%",
    "background-position": "left top",
    "background-repeat": "no-repeat",
    "margin-top": "-50px"
  }
  
  // Appends Sabrina's body
  var body = parent.append("div")
    .style("width",(height*(body_size.width/body_size.height))+"%")
    .style("padding-bottom",height+"%")
    .style("background-image","url('/static/img/sabrina/body_"+outfit+presenting+".png')")
    .style(image_style)
  
  // Appends Sabrina's eyes
  var eyes = parent.append("div")
    .style("position","absolute")
    .style("top","0px")
    .style("width",((height*(eye_size.height/body_size.height))*(eye_size.width/eye_size.height))+"%")
    .style("padding-bottom",(height*(eye_size.height/body_size.height))+"%")
    .style("background-image","url('/static/img/sabrina/eyes_"+emotion+".png')")
    .style(image_style)
  
  // Appends Sabrina's mouth
  var mouth = parent.append("div")
    .style("position","absolute")
    .style("top","0px")
    .style("width",((height*(mouth_size.height/body_size.height))*(mouth_size.width/mouth_size.height))+"%")
    .style("padding-bottom",(height*(mouth_size.height/body_size.height))+"%")
    .style("background-image","url('/static/img/sabrina/mouth_"+emotion+".png')")
    .style(image_style)
  
  // Appends Sabrina's "hat", if specified
  if (params.hat) {
    var hat = parent.append("div")
      .style("position","absolute")
      .style("top","0px")
      .style("width",((height*(hat_size.height/body_size.height))*(hat_size.width/hat_size.height))+"%")
      .style("padding-bottom",(height*(hat_size.height/body_size.height))+"%")
      .style("background-image","url('/static/img/sabrina/hat_"+params.hat+".png')")
      .style(image_style)
  }
  
  // Makes Sabrina blink, if blink = true
  if (blink) {
    
    // Gets called immediately, and then calls itself based on a random interval
    function blink_timer() {
      // Set random interval between 3 and 6 seconds (time between blinks)
      var time = visual.random(3000,6000)
      setTimeout(function(){
        // Call blink_image to actual make her blink
        blink_image();
        // Call itself to reset timer
        blink_timer();
      },time)
    }
    
    blink_timer();
    
    function blink_image() {
      // Close her eyes!
      eyes.style("background-image",
        "url('/static/img/sabrina/eyes_blink.png')")
      // Open her eyes after the defined blink_timing wait
      setTimeout(function(){
        eyes.style("background-image",
          "url('/static/img/sabrina/eyes_"+emotion+".png')")
        // She has a 1 in 5 chance of blinking a second time
        var second = visual.random(1,5)
        if(second == 1) {
          setTimeout(function(){
            eyes.style("background-image",
              "url('/static/img/sabrina/eyes_blink.png')")
            setTimeout(function(){
              eyes.style("background-image",
                "url('/static/img/sabrina/eyes_"+emotion+".png')")
            },blink_timing)
          },blink_timing)
        }
      },blink_timing)
    }
    
  }
      
}

visual.breadcrumbs = function() {
  
  var path_array = window.location.pathname.split("/"),
      window_path = path_array.slice(1,path_array.length-1),
      attr_lookup = ["guide","profiles"].indexOf(window_path[0]) >= 0 ? true : false,
      crumbs = [],
      waiting = [];
      
  window_path.forEach(function(p,i){
    
    crumbs.push({
      "id": p,
      "text": p.toTitleCase()
    })
    
    if (attr_lookup && [2,4].indexOf(i) >= 0) {
      
      if (["location","potential","growth","industries","wages"].indexOf(window_path[i-1]) >= 0) {
        var type = "bra";
        if (p == "all") {
          var type = "wld", id = "sabra";
        }
        else {
          var type = "bra", id = p;
        }
      }
      else if (["industry","attract"].indexOf(window_path[i-1]) >= 0) {
        if ([1,5].indexOf(p.length) >= 0) var type = "isic";
        else var type = "hs";
        var id = p;
      }
      else if (["career","occupation"].indexOf(window_path[i-1]) >= 0) {
        var type = "cbo", id = p;
      }
      else if (["product"] == window_path[i-1]) {
        var type = "hs", id = p;
      }
      else if (["partner"] == window_path[i-1]) {
        var type = "wld", id = p;
      }

      if (id == "all") {
        crumbs[i].text = "Suggestions"
      }
      else if (id) {
        
        if (id.indexOf(".") >= 0) {
          var split = id.split("."),
              distance = split[1]
          id = split[0]
        }
        else {
          var distance = 0
        }
        waiting.push(p);
        d3.json("/attrs/"+type+"/"+id, function(data){
          
          if (distance == 0) var name = data.data[0].name.toTitleCase();
          else var name = data.data[0].name.toTitleCase() + " (within "+distance+"km)"
          
          crumbs[i].text = name;
          
          waiting.splice(waiting.indexOf(p),1);
          if (waiting.length == 0) create_breadcrumb();
          
        })
      }
    }
    
  })
  
  if (waiting.length == 0) create_breadcrumb();
  
  function create_breadcrumb() {

    var breadcrumbs = d3.select("#site_breadcrumbs")
    breadcrumbs.selectAll("*").remove();
  
    crumbs.forEach(function(c,i){
    
      var crumb = breadcrumbs.append("div")
        .attr("id","crumb_"+c.id)
        .attr("class","site_crumb")
        .attr("name",c.name)
      
      if (i == 0 && crumbs.length == 1) {
        crumb.append("div").attr("class","site_crumb_back_red")
      }
      else if (i == 0) {
        crumb.append("div").attr("class","site_crumb_back_brown")
      }
      else if (i == crumbs.length-1) {
        crumb.append("div").attr("class","site_crumb_tail_red")
      }
      else {
        crumb.append("div").attr("class","site_crumb_tail_brown")
      }
    
      if (i == crumbs.length-1) {
        crumb.append("div").attr("class","site_crumb_body_red")
          .html(c.text.truncate(25))
        crumb.append("div").attr("class","site_crumb_arrow_red")
      }
      else {
        crumb.append("div").attr("class","site_crumb_body_brown")
          .html(c.text.truncate(25))
        crumb.append("div").attr("class","site_crumb_arrow_brown")
      
        crumb
          .style("cursor","pointer")
          .on(vizwhiz.evt.click,function(){
            var name = d3.select(this).attr("name")
            if (window["breadcrumb_click"]) window["breadcrumb_click"](name)
            if (window["load_page"]) {
              current_path = window_path.slice(1,i+1)
              load_page(true);
            }
            else {
              var new_path = window_path.slice(0,i+1)
              window.location = "/"+new_path.join("/")+"/";
            }
          })
      }
    
    })
    
  }
  
}

// Resize all the text on the page based off of a percentage
visual.resize = function () {
  
  // If pages are sliding in, only check that new page
  if (d3.select("div#slide_container").node()) {
    var container = d3.select(d3.selectAll("div#slide_container")[0].pop());
    // Set height of empty buffer container to correctly position footer
    d3.select("#slide_buffer").style("height",container.node().offsetHeight+"px");
  }
  // Else, check the entire container
  else if (!d3.select("div#container").empty()) {
    var container = d3.selectAll("div#container, div.popover")
  }
  else {
    var container = d3.select("body");
  }
  
  /* guide */
  d3.selectAll("iframe.guide_app")
    .style("height",function(){
      return this.offsetWidth*(4/6)+"px"
    })
  
  var arrows = [
    {"name": "question", "borderWidth": 2, 
     "point": "left", "fontSize": 16},
    {"name": "decision", "borderWidth": null, 
     "point": "right", "fontSize": 16},
    {"name": "help", "borderWidth": 5, 
     "point": "right", "fontSize": 16},
    {"name": "menu", "borderWidth": 2, 
     "point": "right", "fontSize": 14, "padding": 6}
  ]
  
  arrows.forEach(function(a){
    resize_arrow(a);
  })
  
  function resize_arrow(obj) {

    var border = obj.borderWidth ? obj.borderWidth : 0,
        font = obj.fontSize ? obj.fontSize : 16,
        padding = obj.padding ? obj.padding : font;
    
    if (obj.point == "left") {
      var text_border = border+"px "+border+"px "+border+"px 0px",
          arrow_border = "0px 0px "+border+"px "+border+"px",
          text_padding = padding+"px";
    }
    else {
      var text_border = border+"px 0px "+border+"px "+border+"px",
          arrow_border = border+"px "+border+"px 0px 0px",
          text_padding = padding+"px 0px "+padding+"px "+padding+"px";
    }

    // Set new font size, padding, and max-width for questions,
    // along with setting height to auto
    container.selectAll("."+obj.name+" > .text")
      .style("font-size",font+"px")
      .style("padding",text_padding)
      .style("height","auto")
      
    if (obj.name == "question") {
      container.selectAll("."+obj.name+" > .text")
        .style("max-width",function(){
          var parent_width = d3.select(this.parentNode).style("width");
          return (parseInt(parent_width,10)-(padding*6))+"px"
        })
    }
    else {
      container.selectAll("."+obj.name+" > .text")
        .style("width",function(){
          var parent_width = d3.select(this.parentNode).style("width");
          return parseInt(parent_width,10)-(padding*5)+"px"
        })
    }
    
    // Gets tallest question height
    var height = 0;
    container.selectAll("."+obj.name+" > .text")
      .each(function() {
        var h = parseFloat(d3.select(this).style("height"),10)
        if (h > height) height = h;
      })
    var outer_height = height+(padding*2)+(border/2),
        arrow_height = Math.sqrt((outer_height*outer_height)/2);
        
    container.selectAll("."+obj.name+" > .arrow")
      .style("border-width", arrow_border)
      .style("height",arrow_height+"px")
      .style("width",arrow_height+"px")
      .style("margin-right",function(){
        return obj.point == "left" ? -arrow_height-(border*0.75)+"px" : "0px";
      })
      .style("margin-left",function(){
        return obj.point == "left" ? arrow_height+(border*0.75)+"px" : "0px";
      })

    container.selectAll("."+obj.name+" > .text")
      .style("border-width", text_border)
      .style("height",height+"px")
    
    container.selectAll("."+obj.name)
      .style("height", height+(padding*2)+(border*2)+"px")
      .style("margin-bottom",padding+"px")
      .style("margin-left",function(){
        return obj.point == "left" ? -arrow_height-height+"px" : "0px";
      })
      .style("padding",function(){
        if (obj.point == "left") {
          return "0px "+(height)+"px"
        }
        else {
          return "0px "+(height)+"px 0px 0px"
        }
      })
      
  }
  
  if (!d3.select("#sabrina_selector").empty()) {
    
    var height = parseInt(d3.select("#sabrina_selector").style("height"),10);

    d3.select("#selector").style("height",(height*0.8)+"px");
      
  }
  
  // Selector Resizing
  
  d3.selectAll(".selector")
    .each(function(){
      
      if (this.style.display != "none") {
        
        var container = d3.select(this),
            w = this.offsetWidth,
            body = container.select(".selector_body");
          
        var max_height = this.offsetHeight
        if (container.select(".selector_header").node()) {
          max_height -= container.select(".selector_header").node().offsetHeight
        }
        if (container.select(".selector_nav").node()) {
          max_height -= container.select(".selector_nav").node().offsetHeight
        }
        if (body.node()) {
          max_height -= parseInt(body.style("padding-top"),10)
          max_height -= parseInt(body.style("padding-bottom"),10)
        }
        max_height = Math.round(max_height)
      
        body.style("height",max_height+"px");
        
      }
        
    })
    
  d3.selectAll(".popover")
    .each(function(){
      var h = -this.offsetHeight/2+"px"
      this.style.marginTop = h
    })
  
}

// Called after content has been fetched from the server
// If back = true, reverse the direction of the slide
visual.slide.load = function(content, back) {
  
  var prefix = visual.slide.back(back);
  
  // If there is no slide_buffer on the page, add one.
  // This keeps the page footer at the bottom, because slide_container
  // have absolute positioning.
  if (!d3.select("#slide_buffer").node()) {
    d3.select("#container").append("div")
      .attr("id","slide_buffer")
  }

  // Append new slide_container, positioned off-screen
  var new_div = d3.select("#container").append("div")
    .attr("id","slide_container")
    .style("left",prefix+"150%");

  // Load content into new slide_container
  new_div.node().appendChild(content);
  
  visual.resize();

  // move new slide_container back onto the page
  new_div
    .style("-webkit-transition-duration",visual.slide.timing+"s")
    .style("-moz-transition-duration",visual.slide.timing+"s")
    .style("transition-duration",visual.slide.timing+"s")
    .style("left","0%")
    
}

visual.slide.remove = function(back) {
  
  var prefix = visual.slide.back(!back);
  
  // move container off of page
  var old_divs = d3.selectAll("div#slide_container")
    .style("left",prefix+"150%");

  // wait for container to move off of page
  setTimeout(function(){
    old_divs.remove();
  },visual.slide.timing*1000)
  
}

visual.slide.back = function(back) {
  return back ? "-" : "";
}
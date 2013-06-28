// leon
// Created by Dave Landry

// Sup?

var leon = {}

leon.debug = true;
leon.autohide = true;
leon.version = 0.1

leon.corners = 0
leon.padding = 6

leon.time = {}
leon.time.fade = 0.25
leon.time.hover = 0.1

leon.color = {}

leon.color.tint = function(color, percent) {   
    var num = parseInt(color.slice(1),16),
    amt = Math.round(2.55 * percent),
    R = (num >> 16) + amt,
    B = (num >> 8 & 0x00FF) + amt,
    G = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
}

leon.color.text = function(color) {
  
  var light = "#fff", 
      dark = "#333",
      hsl = leon.color.hsl(color);
      
  if (hsl.l > 65) return dark;
  else if (hsl.l < 48) return light;
  return hsl.h > 35 && hsl.s >= 3 && hsl.l >= 41 ? dark : light;
  
}
  
leon.color.hsl = function(color){
    var r = parseInt(color.substr(1,2),16)
    var g = parseInt(color.substr(3,2),16)
    var b = parseInt(color.substr(5,2),16)
    r /= 255, g /= 255, b /= 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, l = (max + min) / 2;
    
    if(max == min){
        h = s = 0; // achromatic
    }else{
        var d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return {
      "h": Math.floor(h * 360),
      "s": Math.floor(s * 100),
      "l": Math.floor(l * 100)
    };
}

leon.color.main = {}
leon.color.main.normal = "#af1f24"
leon.color.main.dark = leon.color.tint(leon.color.main.normal,-10)
leon.color.accent = {}
leon.color.accent.normal = "#ffffff"
leon.color.accent.hover = "#efefef"
leon.color.accent.highlight = "#aaaaaa"
leon.color.accent.dark = "#888888"

leon.font = {}
leon.font.family = "Helvetica, Arial, sans-serif"
leon.font.size = 12
leon.font.weight = "normal"

leon.border = 0

leon.start = function(name) {
  
  if (!name) var name = "all"
  
  leon.get(name).forEach(function(obj){
    leon[obj.type.split("-")[0]](obj)
  })
  
}
leon.style = {}
var head = document.getElementsByTagName("head")[0]
var style = document.createElement("style")
style.type = "text/css"
style.innerHTML = "\
  .leon {\
    border-radius: "+leon.corners+"px;\
    -moz-border-radius: "+leon.corners+"px;\
    -webkit-border-radius: "+leon.corners+"px;\
    display: inline-block;\
    font-family: "+leon.font.family+";\
    font-size: "+leon.font.size+"px;\
    font-weight: "+leon.font.weight+";\
    z-index: 1000;\
  }\
  .leon.button {\
    background: "+leon.color.accent.normal+";\
    border: "+leon.border+"px solid "+leon.color.accent.dark+";\
    -webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);\
       -moz-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);\
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);\
    color: "+leon.color.text(leon.color.accent.normal)+";\
    padding: "+leon.padding+"px;\
    margin: "+leon.padding+"px;\
    text-align: center;\
    transition: color "+leon.time.hover+"s, background "+leon.time.hover+"s, border-color "+leon.time.hover+"s;\
    -webkit-transition: color "+leon.time.hover+"s, background "+leon.time.hover+"s, border-color "+leon.time.hover+"s;\
    vertical-align: top;\
  }\
  .leon.button > .icon{\
    background-repeat: no-repeat;\
    background-size: 100%;\
    float: left;\
    height: "+(leon.font.size+2)+"px;\
    margin-right: "+leon.padding+"px;\
    width: "+(leon.font.size+2)+"px;\
  }\
  .leon.button:hover {\
    background: "+leon.color.accent.hover+";\
    color: "+leon.color.main.normal+";\
    cursor: pointer;\
  }\
  .leon.button.active {\
    background: "+leon.color.main.normal+";\
    border-color: "+leon.color.main.dark+";\
    border-right-width: "+leon.border+"px !important;\
    color: "+leon.color.text(leon.color.main.normal)+";\
  }\
  .leon.button:active {\
    background: "+leon.color.main.normal+";\
    border-color: "+leon.color.main.dark+";\
    color: "+leon.color.text(leon.color.main.normal)+";\
  }\
  .leon.button.active:hover {\
    cursor: pointer;\
  }\
  .leon.radio {\
    display: inline-block;\
    margin: "+leon.padding+"px;\
  }\
  .leon.radio.group {\
    -webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);\
       -moz-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);\
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);\
    margin: 0px;\
  }\
  .leon.radio.group > .leon.button {\
    -webkit-box-shadow: none;\
       -moz-box-shadow: none;\
            box-shadow: none;\
    margin: 0px;\
  }\
  .leon.radio.group > .leon.button.first {\
    border-top-right-radius: 0px;\
    -moz-border-top-right-radius: 0px;\
    -webkit-border-top-right-radius: 0px;\
    border-bottom-right-radius: 0px;\
    -moz-border-bottom-right-radius: 0px;\
    -webkit-border-bottom-right-radius: 0px;\
    border-right-width: 0px;\
  }\
  .leon.radio.group > .leon.button.middle {\
    border-radius: 0px;\
    -moz-border-radius: 0px;\
    -webkit-border-radius: 0px;\
    border-right-width: 0px;\
  }\
  .leon.radio.group > .leon.button.last {\
    border-top-left-radius: 0px;\
    -moz-border-top-left-radius: 0px;\
    -webkit-border-top-left-radius: 0px;\
    border-bottom-left-radius: 0px;\
    -moz-border-bottom-left-radius: 0px;\
    -webkit-border-bottom-left-radius: 0px;\
  }\
  .leon.radio.group > .leon.button.first.active + .leon.button,\
  .leon.radio.group > .leon.button.middle.active + .leon.button {\
    border-left-width: 0px;\
  }\
  .leon.label {\
    border: "+leon.border+"px solid transparent;\
    color: "+leon.color.main.dark+";\
    float: left;\
    font-weight: bold;\
    padding: "+leon.padding+"px;\
  }\
  label.leon.label {\
    margin: "+leon.padding+"px -"+leon.padding+"px "+leon.padding+"px "+leon.padding+"px;\
  }\
  .leon.select {\
    display: inline-block;\
    margin: "+leon.padding+"px;\
    position: relative;\
    z-index: 1001;\
  }\
  .leon.select > .leon.button {\
    margin: 0px;\
    position: relative;\
    text-align: left;\
  }\
  .leon.select > .leon.button.active {\
    border-bottom-left-radius: 0px;\
    -moz-border-bottom-left-radius: 0px;\
    -webkit-border-bottom-left-radius: 0px;\
    border-bottom-right-radius: 0px;\
    -moz-border-bottom-right-radius: 0px;\
    -webkit-border-bottom-right-radius: 0px;\
  }\
  .leon.select.dropdown {\
    -webkit-box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.25);\
       -moz-box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.25);\
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.25);\
    left: 0px;\
    margin: 0px;\
    opacity: 0px;\
    position: absolute;\
    top: 0px;\
    transition: opacity "+leon.time.fade+"s, top "+leon.time.fade+"s;\
    -webkit-transition: opacity "+leon.time.fade+"s, top "+leon.time.fade+"s;\
    visibility: hidden;\
    z-index: -1;\
  }\
  .leon.select.dropdown > .leon.button {\
    -webkit-box-shadow: none;\
       -moz-box-shadow: none;\
            box-shadow: none;\
    display: block;\
    float: none;\
    margin: 0px;\
    text-align: left;\
    white-space: nowrap;\
  }\
  .leon.select.dropdown > .leon.button.first {\
    border-radius: 0px;\
    -moz-border-radius: 0px;\
    -webkit-border-radius: 0px;\
    border-bottom-width: 0px;\
    border-top-width: 0px;\
  }\
  .leon.select.dropdown > .leon.button.middle {\
    border-radius: 0px;\
    -moz-border-radius: 0px;\
    -webkit-border-radius: 0px;\
    border-bottom-width: 0px;\
  }\
  .leon.select.dropdown > .leon.button.last {\
    border-top-left-radius: 0px;\
    -moz-border-top-left-radius: 0px;\
    -webkit-border-top-left-radius: 0px;\
    border-top-right-radius: 0px;\
    -moz-border-top-right-radius: 0px;\
    -webkit-border-top-right-radius: 0px;\
  }\
  .leon.select.dropdown > .leon.button.first.active + .leon.button,\
  .leon.select.dropdown > .leon.button.middle.active + .leon.button {\
    border-left-width: 0px;\
  }\
  .leon.arrow {\
    float: right;\
    font-family: times;\
    font-size: 18px;\
    height: 14px;\
    line-height: 14px;\
    margin-left: 6px;\
    margin-right: 2px;\
    opacity: 0.5;\
    transform: rotate(90deg);\
    -moz-transform: rotate(90deg);\
    -webkit-transform: rotate(90deg);\
    width: 9px;\
  }\
  .leon.checkbox {\
    margin: "+leon.padding+"px;\
  }\
  .leon.checkbox.group {\
    background: "+leon.color.accent.dark+";\
    -webkit-box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
       -moz-box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
            box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
    cursor: pointer;\
    margin: 0px;\
    position: relative;\
    transition: background "+leon.time.hover+"s;\
    -webkit-transition: background "+leon.time.hover+"s;\
  }\
  .leon.checkbox.group > .leon.button {\
    display: block;\
    float: none;\
    left: 0px;\
    margin: 0px;\
    position: absolute;\
    transition: left "+leon.time.hover+"s;\
    -webkit-transition: left "+leon.time.hover+"s;\
  }\
  .leon.text {\
    background: "+leon.color.accent.normal+";\
    border: "+leon.border+"px solid "+leon.color.accent.dark+";\
    -webkit-box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
       -moz-box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
            box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
    color: "+leon.color.text(leon.color.accent.normal)+";\
    padding: "+leon.padding+"px;\
    margin: "+leon.padding+"px;\
    transition: color "+leon.time.hover+"s, background "+leon.time.hover+"s, border-color "+leon.time.hover+"s;\
    -webkit-transition: color "+leon.time.hover+"s, background "+leon.time.hover+"s, border-color "+leon.time.hover+"s;\
  }\
  .leon.text:hover {\
    background: "+leon.color.accent.hover+";\
    cursor: pointer;\
  }\
  .leon.text:focus {\
    background: "+leon.color.accent.normal+";\
    border-color: "+leon.color.main.normal+";\
    outline: none;\
  }\
  .leon.range {\
    margin: "+leon.padding+"px;\
    padding: 0px;\
  }\
  .leon.range > .leon.button.play {\
    margin: 0px "+leon.padding+"px 0px 0px;\
  }\
  .leon.range.slider {\
    background: "+leon.color.accent.dark+";\
    -webkit-box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
       -moz-box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
            box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.25);\
    margin: 0px;\
    position: relative;\
    -webkit-user-select: none;\
       -moz-user-select: none;\
        -ms-user-select: none;\
            user-select: none;\
  }\
  .leon.range.slider > .leon.button.tick {\
    background: none;\
    border-color: transparent;\
    -webkit-box-shadow: none;\
       -moz-box-shadow: none;\
            box-shadow: none;\
    color: "+leon.color.accent.hover+";\
    display: block;\
    float: none;\
    margin: 0px;\
    opacity: 0.5;\
    position: absolute;\
    text-align: center;\
    text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.25);\
  }\
  .leon.range.slider > .leon.button.tick.bullet {\
    line-height: "+(leon.font.size*1.35)+"px;\
  }\
  .leon.range.slider > .leon.button.handle {\
    display: block;\
    float: none;\
    margin: 0px;\
    position: absolute;\
    text-align: center;\
  }\
  .leon.range.slider > .leon.ranger {\
    background: "+leon.color.main.normal+";\
    display: block;\
    float: none;\
    margin: 0px;\
    position: absolute;\
  }\
"
head.appendChild(style)
// Finds all elements that match the passed ID or Class
leon.get = function(name) {
  
  if (leon.debug == true) console.log("[leon] leon.get("+name+")")
  
  var objs = []
  
  var labellist = document.getElementsByTagName('LABEL');
  var labels = []
  for(var i = labellist.length; i--; labels.unshift(labellist[i]));
  labels.forEach(function(label){
    if (label.htmlFor != '') {
      var elem = document.getElementById(label.htmlFor);
      if (elem) {
        elem.label = label;
      }
    }
  })
  
  if (name == "all") {
    var tags = ["SELECT","INPUT"]
    tags.forEach(function(tag){
      var nodelist = document.getElementsByTagName(tag)
      for(var i = nodelist.length; i--; objs.unshift(nodelist[i]));
    })
  }
  else {
    var prefixes = ["#",".","$"]
    if (prefixes.indexOf(name.charAt(0)) >= 0) {
      if (name.indexOf("$") == 0) {
        var nodelist = document.getElementsByName(name.substr(1))
      }
      else {
        var nodelist = document.querySelectorAll(name)
      }
    } 
    else {
      var nodelist = document.getElementsByTagName(name)
    }
    for(var i = nodelist.length; i--; objs.unshift(nodelist[i]));
  }
  
  var others = objs.filter(function(obj) {
    return obj.type != "radio"
  })
  
  var radios = objs.filter(function(obj) {
    return obj.type == "radio"
  })
  
  var radio_groups = [], return_radios = []
  radios.forEach(function(radio,i){
    if (return_radios.length) {
      var prev_group = return_radios[return_radios.length-1],
          prev_node = prev_group[prev_group.length-1]
      if (prev_node.name == radio.name) {
        prev_group.push(radio)
      }
      else {
        return_radios.push([radio])
      }
    }
    else {
      return_radios.push([radio])
    }
  })
  
  var objs = []
  others.forEach(function(obj) {
    objs.push({
      "items": obj,
      "type": obj.type
    })
  })
  
  return_radios.forEach(function(radio_group) {
    
    var temp_obj = {
          "items": radio_group,
          "type": "radio",
          "name": radio_group[0].name
        }
    
    objs.push(temp_obj)
  })

  
  var legendlist = document.getElementsByTagName('LEGEND');
  var legends = []
  for(var i = legendlist.length; i--; legends.unshift(legendlist[i]));
  objs.forEach(function(obj){
    for (var i = 0; i < legends.length; i++) {
      if (legends[i].id == obj.name) {
        obj.legend = legends[i]
      }
    }
  })
  
  if (leon.debug == true) console.log(objs)
  
  return objs
}
/*
CUSTOM BUTTON CREATOR
Creates a custom button when passed an item
*/
leon.button = function(item,parent) {
  
    if (item.type == "button") var item = item.items
    
    if (item.label) {
      if (typeof item.label != "string") {
        var html = item.label.innerHTML
        if (leon.autohide) item.label.style.display = "none"
      }
      else {
        var html = item.label
      }
    }
    else {
      var html = item.value
    }
    
    if (leon.autohide) item.style.display = "none"
    
    var button = document.createElement("div")
    button.className = "leon button"
    
    if (item.attributes.icon) {
      var icon = document.createElement("div")
      icon.className = "leon icon"
      icon.style.backgroundImage = item.attributes.icon.value
      if (item.attributes.color) {
        icon.style.backgroundColor = item.attributes.color.value
      }
      button.appendChild(icon)
    }
    
    button.innerHTML = button.innerHTML + html
    button.value = item.value
    
    if (parent) {
      parent.appendChild(button)
    }
    else {
      item.parentNode.insertBefore(button,item)
    }
    
    if (item.onclick) {
      button.addEventListener("click",function(e){
        if (this.className.indexOf("active") < 0) item.onclick()
      })
    }
    
    this.item = item
    this.node = button
    
    this.class = function(name) {
      if (name) {
        this.node.className = name
      }
      else {
        return this.node.className
      }
    }
    this.addclass = function(name) {
      this.class(this.node.className + " " + name)
    }
    this.removeclass = function(name) {
      var c = this.class().split(" ")
      var i = c.indexOf(name)
      if (i >= 0) c.splice(i,1)
      this.class(c.join(" "))
    }
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon.checkbox = function(obj) {
  
  enable = function() {
    buttongroup.style.background = leon.color.main.normal
    button.style.left = button.offsetHeight+"px"
    obj.items.checked = true
  }
  
  disable = function() {
    buttongroup.style.background = leon.color.accent.dark
    button.style.left = "0px"
    obj.items.checked = false
  }
  
  if (leon.autohide) obj.items.style.display = "none"
  
  var divgroup = document.createElement("div")
  divgroup.className = "leon checkbox"
  obj.items.parentNode.insertBefore(divgroup,obj.items)
  
  if (obj.items.label) {
    var label = new leon.label(obj.items,divgroup)
  }
  
  var buttongroup = document.createElement("div")
  buttongroup.className = "leon checkbox group"
  divgroup.appendChild(buttongroup)
  
  buttongroup.addEventListener("click",function(e){
    if (obj.items.checked) disable()
    else enable()
    if (obj.items.onclick) obj.items.onclick()
  })
  
  var button = document.createElement("div")
  button.className = "leon button"
  button.innerHTML = "&nbsp;"
  buttongroup.appendChild(button)
  
  var w = button.offsetHeight - leon.padding*2 - leon.border*2
  button.style.width = w+"px"
  buttongroup.style.width = (button.offsetHeight*2)+"px"
  buttongroup.style.height = button.offsetHeight+"px"
  
  if (obj.items.checked) enable()
  
}
/*
CUSTOM BUTTON CREATOR
Creates a custom button when passed an item
*/
leon.label = function(item,parent) {
  
    var html = item.innerHTML ? item.innerHTML : item.id
    if (item.label) {
      if (typeof item.label != "string") {
        html = item.label.innerHTML
        if (leon.autohide) item.label.style.display = "none"
      }
      else {
        html = item.label
      }
    }
    
    if (leon.autohide) item.style.display = "none"
    
    var label = document.createElement("div")
    label.className = "leon label"
    label.innerHTML = html
    
    if (parent) parent.appendChild(label)
    else item.parentNode.insertBefore(label,item)
    
    this.item = item
    this.node = label
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon.radio = function(obj) {
  
  var divgroup = document.createElement("div")
  divgroup.className = "leon radio"
  obj.items[0].parentNode.insertBefore(divgroup,obj.items[0])
  
  if (obj.legend) {
    var label = new leon.label(obj.legend,divgroup)
  }
  
  var buttongroup = document.createElement("div")
  buttongroup.className = "leon radio group"
  divgroup.appendChild(buttongroup)
  
  obj.items.forEach(function(item,i){
    
    var button = new leon.button(item,buttongroup)
    
    if (i == 0) button.addclass("first")
    else if (i == obj.items.length-1) button.addclass("last")
    else button.addclass("middle")
    
    button.node.addEventListener("click", function(d){
      if (obj.checked.div.value != this.value) {
        obj.checked.input.checked = false
        obj.checked.div.removeclass("active")
        item.checked = true
        button.addclass("active")
        obj.checked.input = item
        obj.checked.div = button
      }
    })
    
    if (item.checked) {
      button.addclass("active")
      obj.checked = {
        "input": item,
        "div": button
      }
    }
    
  })
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon.range = function(obj) {
  
  setvalue = function(value) {
    
    if (typeof value == "string") value = parseFloat(value)
    
    if (range) {
      
      var h1 = parseFloat(handle.innerHTML),
          h2 = parseFloat(handle2.innerHTML)
          
      if (value < h1 || value <= h1+((h2-h1)/2)) {
        h1 = value
        handle.innerHTML = h1
        handle.style.left = tick_positions[h1]+"px"
        obj.items.value = h1
        active_handle = handle
      }
      else {
        h2 = value
        handle2.innerHTML = h2
        handle2.style.left = tick_positions[h2]+"px"
        obj.items.alt = h2
        active_handle = handle2
      }
      
      ranger.style.left = tick_positions[h1]+"px"
      ranger.style.width = (tick_positions[h2]-tick_positions[h1])+"px"
      
    }
    else {
      obj.items.value = value
      handle.innerHTML = value
      handle.style.left = tick_positions[value]+"px"
      active_handle = handle
    }
    active_handle.className = "leon button handle active"
    obj.items.onchange()
    
  }
  
  var min = parseFloat(obj.items.min),
      max = parseFloat(obj.items.max),
      step = parseFloat(obj.items.step),
      label_step = step,
      tick_step = step,
      tick_length = 0,
      ticks = [],
      available_width = obj.items.parentNode.offsetWidth-leon.padding*2,
      tick_positions = {},
      dragging = false,
      handle_width = 0,
      tick_width = 0,
      range = false,
      active_handle,
      playing = false
      
  var divgroup = document.createElement("div")
  divgroup.className = "leon range"
  obj.items.parentNode.insertBefore(divgroup,obj.items)
  
  if (obj.items.label) {
    var label = new leon.label(obj.items,divgroup)
    available_width -= label.node.offsetWidth+leon.padding
  }
  
  if (!range) {
    
    var play = document.createElement("div")
    play.className = "leon button play"
    play.innerHTML = "&#9658"
    play.addEventListener("click",function(e){
      
        if (!playing) {
          playing = true;
          play.className = "leon button play active"
          
          var current = parseFloat(handle.innerHTML,10)
          if (current == max) var i = min;
          else var i = current+step;
          
          setvalue(i);
          i += step;
          
          var play_interval = function() {
            if (i < max) {
              setvalue(i);
              i += step;
              if (i > max) {
                stop_playback();
              }
            }
          }
          
          if (i > max) {
            stop_playback();
          }
          else {
            play_function = setInterval(play_interval,1500);
          }
          
        } 
        else {
          stop_playback();
        }
        
        function stop_playback() {
          clearInterval(play_function);
          playing = false;
          play.className = "leon button play"
          active_handle.className = "leon button handle"
        }
      
    })
    divgroup.appendChild(play)
    
  }
  
  if (leon.autohide) obj.items.style.display = "none"
  
  var slider = document.createElement("div")
  slider.className = "leon range slider"
  divgroup.appendChild(slider)
      
  for (var i = min; i <= max; i += step) {
    var tick = document.createElement("div")
    tick.className = "leon button tick"
    tick.style.opacity = 0
    tick.innerHTML = i
    slider.appendChild(tick)
    ticks.push(tick)
    tick_length++
    if (handle_width < tick.offsetWidth) handle_width = tick.offsetWidth
  }
  
  var handle = document.createElement("div")
  handle.className = "leon button handle"
  handle.innerHTML = obj.items.value
  handle.style.marginLeft = (-handle_width/2)+"px"
  handle.style.width = (handle_width-leon.padding*2)+"px"
  slider.appendChild(handle)

  handle.addEventListener("mousedown",function(){
    dragging = true
    active_handle = handle
  })
  handle.addEventListener("mouseup",function(){
    handle.className = "leon button handle"
    dragging = false
  })
  
  if (obj.items.alt) {
    
    range = true
    
    var ranger = document.createElement("div")
    ranger.className = "leon ranger"
    ranger.style.height = handle.offsetHeight+"px"
    ticks[0].parentNode.insertBefore(ranger,ticks[0])
    
    var handle2 = document.createElement("div")
    handle2.className = "leon button handle"
    handle2.innerHTML = obj.items.alt
    handle2.style.marginLeft = (-handle_width/2)+"px"
    slider.appendChild(handle2)

    handle2.addEventListener("mousedown",function(){
      dragging = true
      active_handle = handle2
    })
    handle2.addEventListener("mouseup",function(){
      handle2.className = "leon button handle"
      dragging = false
    })
  }
  
  document.addEventListener("mousemove",function(e){
    if (dragging) {
      active_handle.className = "leon button handle active"
      var x = e.x-active_handle.parentNode.offsetLeft,
          value = parseFloat(active_handle.innerHTML)
      if (x < tick_positions[value]-tick_width/2) {
        if (x > 0) {
          for (var p = min; p <= max; p++) {
            if (x < tick_positions[p]+tick_width/2) {
              if (p != value) setvalue(p)
              break;
            }
          }
        }
        else if (min != value) setvalue(min)
      }
      else if (x >= tick_positions[value]+tick_width/2) {
        if (x < parseFloat(slider.style.width,10)+handle_width) {
          for (var p = max; p >= min; p--) {
            if (x > tick_positions[p]-tick_width/2) {
              if (p != value) setvalue(p)
              break;
            }
          }
        }
        else if (max != value) setvalue(max)
      }
      
    }
  })
  document.addEventListener("mouseup",function(){
    if (dragging) {
      active_handle.className = "leon button handle"
      dragging = false
    }
  })

  slider.style.height = handle.offsetHeight+"px"
  slider.style.paddingLeft = (handle_width/2)+"px"
  slider.style.paddingRight = (handle_width/2)+"px"
  
  if (available_width < handle_width*tick_length) {
    slider.style.width = (available_width-handle_width)+"px"
    tick_width = available_width/tick_length
    var i = Math.floor(available_width/handle_width)-1, total = max-min
    while ((total/i)%1 != 0) {
      i--
    }
    label_step = total/i
    
    var i = Math.floor(available_width/leon.font.size)-1, total = max-min
    while ((total/i)%1 != 0) {
      i--
    }
    tick_step = total/i
    
  }
  else {
    slider.style.width = (handle_width*(tick_length-1))+"px"
    tick_width = handle_width
  }
  
  ticks.forEach(function(tick,i){
    
    tick.style.marginLeft = (-(tick_width)/2)+"px"
    tick.style.width = (tick_width-leon.padding*2)+"px"

    var value = parseFloat(tick.innerHTML)
    
    var percent = i*(100/(tick_length-1))
        x1 = handle_width/2,
        x2 = parseFloat(slider.style.width,10)+x1-leon.border*2
        
    tick_positions[value] = (percent/100) * (x2 - x1) + x1
    
    tick.style.left = tick_positions[value]+"px"
    tick.addEventListener("mousedown",function(){
      dragging = true
      setvalue(this.innerHTML)
    })
    tick.addEventListener("mouseup",function(){
      active_handle.className = "leon button handle"
      dragging = false
    })
    
    if (i%label_step == 0) {
      var label = document.createElement("div")
      label.className = "leon button tick"
      label.innerHTML = tick.innerHTML
      label.style.left = tick_positions[value]+"px"
      label.style.marginLeft = (-(handle_width)/2)+"px"
      label.style.width = (handle_width-leon.padding*2)+"px"
      slider.insertBefore(label,ticks[0])
    }
    
    if (i%label_step == 0 || i%tick_step == 0) {
      var label = document.createElement("div")
      if (i%label_step == 0) {
        label.innerHTML = tick.innerHTML
        label.className = "leon button tick"
      }
      else if (i%tick_step == 0) {
        label.innerHTML = "&bull;"
        label.className = "leon button tick bullet"
      }
      label.style.marginLeft = (-(handle_width)/2)+"px"
      label.style.width = (handle_width-leon.padding*2)+"px"
      label.style.left = tick_positions[value]+"px"
      slider.insertBefore(label,ticks[0])
    }
    
  })
  
  var value = parseFloat(handle.innerHTML)
  handle.style.left = tick_positions[value]+"px"
  if (range) {
    var value2 = parseFloat(handle2.innerHTML)
    handle2.style.left = tick_positions[value2]+"px"
    ranger.style.left = tick_positions[value]+"px"
    ranger.style.width = (tick_positions[value2]-tick_positions[value])+"px"
  }
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon.select = function(obj) {
  
  var divgroup = document.createElement("div")
  divgroup.className = "leon select"
  obj.items.parentNode.insertBefore(divgroup,obj.items)
  
  if (obj.items.label) {
    var label = new leon.label(obj.items.label,divgroup)
  }
  
  var arrow = "<span class='leon arrow'>&#8227</span>"
  
  obj.items.label = obj.items.selectedOptions[0].label + arrow
  
  var button = new leon.button(obj.items,divgroup)
  button.open = false
  
  var dropdown = document.createElement("div")
  dropdown.className = "leon select dropdown"
  dropdown.style.left = button.node.offsetLeft+"px"
  divgroup.appendChild(dropdown)
  
  var options = []
  for (var i = 0; i < obj.items.length; i++) {
    options.push(new leon.button(obj.items[i],dropdown))
  }
  
  button.show = function() {
    button.addclass("active")
    dropdown.style.visibility = "visible"
    dropdown.style.opacity = 1
    dropdown.style.top = button.node.offsetHeight+"px"
    button.open = true
  }
  
  button.hide = function() {
    button.removeclass("active")
    dropdown.style.opacity = 0
    dropdown.style.top = "0px"
    setTimeout(function() {
      dropdown.style.visibility = "hidden"
      button.open = false
    },leon.time.fade*1000)
  }
  
  button.node.addEventListener("click", function(d){
    if (button.open) {
      button.hide()
    }
    else {
      button.show()
    }
  })
  
  var w = 0
  options.forEach(function(option,i){
    
    var html = option.node.innerHTML
    option.node.innerHTML = html + arrow
    var width = option.node.offsetWidth - leon.padding*2
    if (width > w) w = width
    option.node.innerHTML = html
    
    if (option.item.selected) set_select(option)
    
    if (i == 0) option.addclass("first")
    else if (i == obj.items.length-1) option.addclass("last")
    else option.addclass("middle")
    
    option.node.addEventListener("click", function(d){
      if (obj.items.value != option.item.value) {
        set_select(option)
        obj.items.onchange()
      }
      button.hide()
    })
  })
  
  function set_select(option) {
    obj.items.value = option.item.value
    button.item = option.item
    button.node.innerHTML = option.node.innerHTML + arrow
  }
  
  button.node.style.width = w+"px"
  dropdown.style.width = (w+leon.padding*2+leon.border*2)+"px"
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon.text = function(obj) {
  
  if (obj.items.label) {
    obj.items.label.className = "leon label"
  }
  
  obj.items.className = obj.items.className + " leon text"
  
}

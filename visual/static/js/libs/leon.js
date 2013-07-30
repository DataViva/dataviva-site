// leon
// Created by Dave Landry

// Sup?

leon_construct = {}

leon_vars = {}
leon_vars.debug = false;
leon_vars.autohide = true;
leon_vars.version = 0.1

leon_vars.corners = 0
leon_vars.padding = 6

leon_vars.time = {}
leon_vars.time.fade = 0.25
leon_vars.time.hover = 0.1

leon_vars.font = {}
leon_vars.font.family = '"HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, sans-serif'
leon_vars.font.size = 12
leon_vars.font.weight = "normal"

leon_vars.border = 1

leon_vars.color = {}

leon_vars.color.tint = function(color, percent) {   
    var num = parseInt(color.slice(1),16),
    amt = Math.round(2.55 * percent),
    R = (num >> 16) + amt,
    B = (num >> 8 & 0x00FF) + amt,
    G = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
}

leon_vars.color.text = function(color) {
  
  var light = "#fff", 
      dark = "#666",
      hsl = leon_vars.color.hsl(color);
      
  if (hsl.l > 65) return dark;
  else if (hsl.l < 48) return light;
  return hsl.h > 35 && hsl.s >= 3 && hsl.l >= 41 ? dark : light;
  
}
  
leon_vars.color.hsl = function(color){
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

leon_vars.color.main = {}
leon_vars.color.main.normal = "#af1f24"
leon_vars.color.main.light = leon_vars.color.tint(leon_vars.color.main.normal,10)
leon_vars.color.main.dark = leon_vars.color.tint(leon_vars.color.main.normal,-10)
leon_vars.color.accent = {}
leon_vars.color.accent.normal = "#ffffff"
leon_vars.color.accent.hover = "#efefef"
leon_vars.color.accent.highlight = "#aaaaaa"
leon_vars.color.accent.dark = "#888888"

leon_construct.div = function(classname) {
  var div = document.createElement("div")
  div.className = classname
  return div
}// Finds all elements that match the passed ID or Class
leon = function(name) {
  
  if (!name) var name = "all"
  
  var objs = []
  
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
      "type": obj.type,
      "name": obj.id
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
        obj.label = legends[i]
      }
    }
  })
  
  var returns = {}
  objs.forEach(function(obj){
    var node = document.getElementById("leon_"+obj.items.id)
    if (node) {
      node.parentNode.removeChild(node)
      node = null
    }
    if (obj.items instanceof Array) var parent = obj.items[0].parentNode
    else var parent = obj.items.parentNode
    var display = parent.style.display
    if (display == "none") parent.style.display = "block"
    returns[obj.items.id] = new leon_construct[obj.type.split("-")[0]](obj)
    if (display == "none") parent.style.display = "none"
  })
  if (Object.keys(returns).length == 1) returns = returns[Object.keys(returns)[0]]
  
  return returns
  
}
var head = document.getElementsByTagName("head")[0]
var style = document.createElement("style")
style.type = "text/css"
style.innerHTML = "\
  .leon {\
    border-radius: "+leon_vars.corners+"px;\
    -moz-border-radius: "+leon_vars.corners+"px;\
    -webkit-border-radius: "+leon_vars.corners+"px;\
    display: inline-block;\
    font-family: "+leon_vars.font.family+";\
    font-size: "+leon_vars.font.size+"px;\
    font-weight: "+leon_vars.font.weight+";\
    z-index: 1000;\
  }\
  .leon.button {\
    background: "+leon_vars.color.accent.normal+";\
    border: "+leon_vars.border+"px solid "+leon_vars.color.accent.highlight+";\
    color: "+leon_vars.color.text(leon_vars.color.accent.highlight)+";\
    padding: "+leon_vars.padding+"px;\
    margin: "+leon_vars.padding+"px;\
    text-align: center;\
    transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
    -webkit-transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
    vertical-align: top;\
  }\
  .leon.button > .icon{\
    background-repeat: no-repeat;\
    background-size: 100%;\
    float: left;\
    height: "+(leon_vars.font.size+2)+"px;\
    margin-right: "+leon_vars.padding+"px;\
    width: "+(leon_vars.font.size+2)+"px;\
  }\
  .leon.button:hover {\
    background: "+leon_vars.color.accent.hover+";\
    color: "+leon_vars.color.main.normal+";\
    cursor: pointer;\
  }\
  .leon.button.active {\
    background: "+leon_vars.color.main.normal+";\
    border-color: "+leon_vars.color.main.dark+";\
    border-right-width: "+leon_vars.border+"px !important;\
    color: "+leon_vars.color.text(leon_vars.color.main.normal)+";\
  }\
  .leon.button:active {\
    background: "+leon_vars.color.main.normal+";\
    border-color: "+leon_vars.color.main.dark+";\
    color: "+leon_vars.color.text(leon_vars.color.main.normal)+";\
  }\
  .leon.button.active:hover {\
    cursor: pointer;\
  }\
  .leon.radio {\
    display: inline-block;\
    margin: "+leon_vars.padding+"px;\
  }\
  .leon.radio.group {\
    margin: 0px;\
  }\
  .leon.radio.group > .leon.button {\
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
    border: "+leon_vars.border+"px solid transparent;\
    color: "+leon_vars.color.accent.dark+";\
    float: left;\
    padding: "+leon_vars.padding+"px;\
  }\
  .leon.label.textlabel {\
    margin: "+leon_vars.padding+"px 0px;\
    padding: "+leon_vars.padding+"px 0px "+leon_vars.padding+"px "+leon_vars.padding+"px;\
  }\
  .leon.select {\
    display: inline-block;\
    margin: "+leon_vars.padding+"px;\
    position: relative;\
  }\
  .leon.select.active {\
    z-index: 1005;\
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
    left: 0px;\
    margin: 0px;\
    opacity: 0px;\
    position: absolute;\
    top: 0px;\
    transition: opacity "+leon_vars.time.fade+"s, top "+leon_vars.time.fade+"s;\
    -webkit-transition: opacity "+leon_vars.time.fade+"s, top "+leon_vars.time.fade+"s;\
    visibility: hidden;\
    z-index: -1;\
  }\
  .leon.select.dropdown > .leon.button {\
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
    margin: "+leon_vars.padding+"px;\
  }\
  .leon.checkbox.group {\
    background: "+leon_vars.color.accent.dark+";\
    cursor: pointer;\
    margin: 0px;\
    position: relative;\
    transition: background "+leon_vars.time.hover+"s;\
    -webkit-transition: background "+leon_vars.time.hover+"s;\
  }\
  .leon.checkbox.group > .leon.button {\
    display: block;\
    float: none;\
    left: 0px;\
    margin: 0px;\
    position: absolute;\
    transition: left "+leon_vars.time.hover+"s;\
    -webkit-transition: left "+leon_vars.time.hover+"s;\
  }\
  .leon.text {\
    background: "+leon_vars.color.accent.normal+";\
    border: "+leon_vars.border+"px solid "+leon_vars.color.accent.dark+";\
    color: "+leon_vars.color.text(leon_vars.color.accent.normal)+";\
    padding: "+leon_vars.padding+"px;\
    margin: "+leon_vars.padding+"px;\
    transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
    -webkit-transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
  }\
  .leon.text:hover {\
    background: "+leon_vars.color.accent.hover+";\
    cursor: pointer;\
  }\
  .leon.text:focus {\
    background: "+leon_vars.color.accent.normal+";\
    border-color: "+leon_vars.color.main.normal+";\
    outline: none;\
  }\
  .leon.range {\
    margin: "+leon_vars.padding+"px;\
    padding: 0px;\
  }\
  .leon.range > .leon.button.play {\
    margin: 0px "+leon_vars.padding+"px 0px 0px;\
  }\
  .leon.range.slider {\
    background: "+leon_vars.color.accent.dark+";\
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
    color: "+leon_vars.color.accent.hover+";\
    display: block;\
    float: none;\
    margin: 0px;\
    opacity: 0.5;\
    position: absolute;\
    text-align: center;\
    text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.25);\
  }\
  .leon.range.slider > .leon.button.tick.bullet {\
    line-height: "+(leon_vars.font.size*1.35)+"px;\
  }\
  .leon.range.slider > .leon.button.handle {\
    display: block;\
    float: none;\
    margin: 0px;\
    position: absolute;\
    text-align: center;\
  }\
  .leon.range.slider > .leon.ranger {\
    background: "+leon_vars.color.main.normal+";\
    display: block;\
    float: none;\
    margin: 0px;\
    position: absolute;\
  }\
"
head.appendChild(style)
/*
CUSTOM BUTTON CREATOR
Creates a custom button when passed an item
*/
leon_construct.label = function(item,parent) {

    var html = item.innerHTML ? item.innerHTML : item.id
    
    if (leon_vars.autohide) item.style.display = "none"
    
    var label = document.createElement("div")
    label.className = "leon label"
    label.innerHTML = html
    
    if (parent) parent.appendChild(label)
    else item.parentNode.insertBefore(label,item)
    
    this.item = item
    this.node = label
  
}
/*
CUSTOM BUTTON CREATOR
Creates a custom button when passed an item
*/
leon_construct.button = function(item,parent) {
  
    if (item.type == "button") var item = item.items
    
    if (item.labels && item.labels[0]) {
      var label = item.labels[0]
      if (typeof label != "string") {
        var html = label.innerHTML
        if (leon_vars.autohide) label.style.display = "none"
      }
      else {
        var html = label
      }
    }
    else {
      var html = item.innerHTML
    }
    
    if (leon_vars.autohide) item.style.display = "none"
    
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
    button.id = "leon_button_"+item.value
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
    this.id = button.id
    
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
leon_construct.checkbox = function(obj) {
  
  enable = function() {
    buttongroup.style.background = leon_vars.color.main.normal
    button.style.left = button.offsetHeight+"px"
    obj.items.checked = true
  }
  
  disable = function() {
    buttongroup.style.background = leon_vars.color.accent.dark
    button.style.left = "0px"
    obj.items.checked = false
  }
  
  if (leon_vars.autohide) obj.items.style.display = "none"
  
  var divgroup = document.createElement("div")
  divgroup.className = "leon checkbox"
  obj.items.parentNode.insertBefore(divgroup,obj.items)
  
  if (obj.items.labels[0]) {
    var label = new leon_construct.label(obj.items.labels[0],divgroup)
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
  
  var w = button.offsetHeight - leon_vars.padding*2 - leon_vars.border*2
  button.style.width = w+"px"
  buttongroup.style.width = (button.offsetHeight*2)+"px"
  buttongroup.style.height = button.offsetHeight+"px"
  
  if (obj.items.checked) enable()
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon_construct.radio = function(obj) {
  
  var divgroup = document.createElement("div")
  divgroup.className = "leon radio"
  obj.items[0].parentNode.insertBefore(divgroup,obj.items[0])
  
  if (obj.label) {
    var label = new leon_construct.label(obj.label,divgroup)
  }
  
  var buttongroup = document.createElement("div")
  buttongroup.className = "leon radio group"
  divgroup.appendChild(buttongroup)
  
  obj.items.forEach(function(item,i){
    
    var button = new leon_construct.button(item,buttongroup)
    
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
CUSTOM RANGE SLIDER CREATOR
*/
leon_construct.range = function(obj) {
  
  var self = this
  
  this.input = obj.items
  if (leon_vars.autohide) self.input.style.display = "none"
  
  var min = parseFloat(self.input.min),
      max = parseFloat(self.input.max),
      step = parseFloat(self.input.step),
      handle_width = 0,
      tick_width = 0,
      dragging = false,
      label_step = step,
      tick_step = step,
      tick_length = 0,
      ticks = [],
      available_width = self.input.parentNode.offsetWidth-leon_vars.padding*2,
      slider,
      handle,
      handle2,
      ranger,
      tick_positions = {},
      range = false,
      active_handle,
      play_button,
      playing = false,
      frame = self.min
  
  var play_function = function() {
    if (frame <= max) {
      self.value(frame);
      frame += step;
      if (frame > max) {
        self.stop()
      }
    }
  }
  
  var play_interval = null
      
  this.node = document.createElement("div")
  this.node.className = "leon range"
  this.input.parentNode.insertBefore(self.node,self.input)
  
  if (this.input.labels[0]) {
    this.label = new leon_construct.label(self.input.labels[0],self.node)
    available_width -= self.input.labels[0].offsetWidth+leon_vars.padding
  }
  
  if (!range) {
    
    play_button = document.createElement("div")
    play_button.className = "leon button play"
    play_button.innerHTML = "&#9658"
    play_button.addEventListener("click",function(){
        if (!playing) self.play()
        else self.stop()
    })
    self.node.appendChild(play_button)
    play_button.style.width = play_button.offsetHeight-leon_vars.padding*2-leon_vars.border*2
    
  }
  
  slider = leon_construct.div("leon range slider")
  self.node.appendChild(slider)
      
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
  
  handle = leon_construct.div("leon button handle")
  handle.innerHTML = self.input.value
  handle.style.marginLeft = (-handle_width/2)+"px"
  handle.style.width = (handle_width-leon_vars.padding*2)+"px"
  slider.appendChild(handle)

  handle.addEventListener("mousedown",function(){
    dragging = true
    active_handle = handle
  })
  handle.addEventListener("mouseup",function(){
    handle.className = "leon button handle"
    dragging = false
  })
  
  if (self.input.alt) {
    
    range = true
    
    ranger = leon_construct.div("leon ranger")
    ranger.style.height = handle.offsetHeight+"px"
    ticks[0].parentNode.insertBefore(ranger,ticks[0])
    
    handle2 = leon_construct.div("leon button handle")
    handle2.innerHTML = self.input.alt
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
              if (p != value) self.value(p)
              break;
            }
          }
        }
        else if (min != value) self.value(min)
      }
      else if (x >= tick_positions[value]+tick_width/2) {
        if (x < parseFloat(slider.style.width,10)+handle_width) {
          for (var p = max; p >= min; p--) {
            if (x > tick_positions[p]-tick_width/2) {
              if (p != value) self.value(p)
              break;
            }
          }
        }
        else if (max != value) self.value(max)
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
    
    var i = Math.floor(available_width/leon_vars.font.size)-1, total = max-min
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
    tick.style.width = (tick_width-leon_vars.padding*2)+"px"

    var value = parseFloat(tick.innerHTML)
    
    var percent = i*(100/(tick_length-1))
        x1 = handle_width/2,
        x2 = parseFloat(slider.style.width,10)+x1-leon_vars.border*2
        
    tick_positions[value] = (percent/100) * (x2 - x1) + x1
    
    tick.style.left = tick_positions[value]+"px"
    tick.addEventListener("mousedown",function(){
      dragging = true
      self.value(this.innerHTML)
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
      label.style.width = (handle_width-leon_vars.padding*2)+"px"
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
      label.style.width = (handle_width-leon_vars.padding*2)+"px"
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
  
  /*************/
  /* FUNCTIONS */
  /*************/
  
  this.value = function(value) {
    
    if (typeof value == "string") value = parseFloat(value)
    
    if (range) {
      
      var h1 = parseFloat(handle.innerHTML),
          h2 = parseFloat(handle2.innerHTML)
          
      if (value < h1 || value <= h1+((h2-h1)/2)) {
        h1 = value
        handle.innerHTML = h1
        handle.style.left = tick_positions[h1]+"px"
        self.input.value = h1
        active_handle = handle
      }
      else {
        h2 = value
        handle2.innerHTML = h2
        handle2.style.left = tick_positions[h2]+"px"
        self.input.alt = h2
        active_handle = handle2
      }
      
      ranger.style.left = tick_positions[h1]+"px"
      ranger.style.width = (tick_positions[h2]-tick_positions[h1])+"px"
      
    }
    else {
      self.input.value = value
      handle.innerHTML = value
      handle.style.left = tick_positions[value]+"px"
      active_handle = handle
    }
    active_handle.className = "leon button handle active"
    self.input.onchange()
    
  }
  
  this.play = function() {
    playing = true
    play_button.className = "leon button play active"
          
    var current = parseFloat(handle.innerHTML,10)
    if (current == max) frame = min;
    else frame = current+step;
    
    self.value(frame)
    frame += step;
          
    if (frame > max) {
      self.stop();
    }
    else {
      play_interval = setInterval(play_function,1500);
    }
    
  }

  this.stop = function() {
    clearInterval(play_interval);
    playing = false;
    play_button.className = "leon button play"
    active_handle.className = "leon button handle"
  }
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon_construct.select = function(obj) {
  
  var self = this
  
  this.input = obj
  
  this.set = function(value) {
    var option = self.options.filter(function(o){
      return o.id == "leon_button_"+value;
    })[0]
    if (!option) var option = self.options[0]
    self.input.items.value = value
    self.selected.node.innerHTML = option.node.innerHTML + arrow
  }
  
  this.show = function() {
    self.selected.addclass("active")
    self.node.className = "leon select active"
    self.dropdown.style.visibility = "visible"
    self.dropdown.style.opacity = 1
    self.dropdown.style.top = self.selected.node.offsetHeight+"px"
    self.selected.open = true
  }
  
  this.hide = function() {
    self.selected.removeclass("active")
    self.dropdown.style.opacity = 0
    self.dropdown.style.top = "0px"
    setTimeout(function() {
      self.dropdown.style.visibility = "hidden"
      self.node.className = "leon select"
      self.selected.open = false
    },leon_vars.time.fade*1000)
  }
  
  self.node = document.createElement("div")
  self.node.className = "leon select"
  self.node.id = "leon_"+self.input.items.id
  self.input.items.parentNode.insertBefore(self.node,self.input.items)
  
  if (self.input.items.labels[0]) {
    var label = new leon_construct.label(self.input.items.labels[0],self.node)
  }
  
  var arrow = "<span class='leon arrow'>&#8227</span>"
  
  this.selected = new leon_construct.button(self.input.items,self.node)
  self.selected.open = false
  
  this.dropdown = document.createElement("div")
  self.dropdown.className = "leon select dropdown"
  self.dropdown.id = "leon_dropdown_"+self.input.items.id
  self.dropdown.style.left = self.selected.node.offsetLeft+"px"
  self.node.appendChild(self.dropdown)
  
  this.options = []
  for (var i = 0; i < self.input.items.length; i++) {
    self.options.push(new leon_construct.button(self.input.items[i],self.dropdown))
  }
  
  self.selected.node.addEventListener("click", function(e){
    e.stopPropagation()
    if (self.selected.open) {
      self.hide()
    }
    else {
      self.show()
    }
  })
  
  var w = 0
  
  self.options.forEach(function(option,i){
    
    var html = option.node.innerHTML
    option.node.innerHTML = html + arrow
    var width = option.node.offsetWidth - leon_vars.padding*2
    if (width > w) w = width
    option.node.innerHTML = html
    
    if (option.item.selected) self.set(option.item.value)
    
    if (i == 0) option.addclass("first")
    else if (i == self.input.items.length-1) option.addclass("last")
    else option.addclass("middle")
    
    option.node.addEventListener("click", function(e){
      e.stopPropagation()
      if (self.input.items.value != option.item.value) {
        self.set(option.item.value)
        self.input.items.onchange()
      }
      self.hide()
    })
  })
  
  self.selected.node.style.width = (w+2)+"px"
  self.dropdown.style.width = (w+2+leon_vars.padding*2+leon_vars.border*2)+"px"
  
}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon_construct.text = function(obj) {
  
  if (obj.items.labels[0]) {
    obj.items.labels[0].className = "leon label textlabel"
  }
  
  obj.items.className = obj.items.className + " leon text"
  
}

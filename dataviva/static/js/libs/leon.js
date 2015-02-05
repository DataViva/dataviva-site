// leon
// Created by Dave Landry

// Sup?

leon_construct = {}

leon_vars = {}
leon_vars.debug = false;
leon_vars.autohide = true;
leon_vars.version = 0.1

leon_vars.corners = 0
leon_vars.size = "medium"
leon_vars.padding = {}
leon_vars.padding.small = "3px 5px 4px 5px"
leon_vars.padding.medium = "4px 6px"
leon_vars.padding.large = "7px 8px 6px 8px"

leon_vars.time = {}
leon_vars.time.fade = 0.25
leon_vars.time.hover = 0.1

leon_vars.font = {}
leon_vars.font.family = '"HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, sans-serif'
leon_vars.font.size = {}
leon_vars.font.size.small = 10
leon_vars.font.size.medium = 12
leon_vars.font.size.large = 18
leon_vars.font.weight = "normal"

leon_vars.border = 1

leon_vars.color = {}

leon_functions = {}
leon_functions.darken = function(color) {
    var percent = -10, num = parseInt(color.slice(1),16),
    amt = Math.round(2.55 * percent),
    R = (num >> 16) + amt,
    B = (num >> 8 & 0x00FF) + amt,
    G = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
}

leon_functions.text_color = function(color) {

  var light = "#fff",
      dark = "#666",
      hsl = leon_vars.color.hsl(color);

  if (hsl.l > 65) return dark;
  else if (hsl.l < 48) return light;
  return hsl.h > 35 && hsl.s >= 3 && hsl.l >= 70 ? dark : light;

}

leon_functions.check_hidden = function(hidden_node) {
  if (hidden_node) {
    if (hidden_node instanceof Array) {
      hidden_node.forEach(function(h){
        h.node.style.visibility = h.v
        h.node.style.display = h.d
      })
    }
    else {
      hidden_objs = []
      function find_hidden(node) {
        function getStyle(el, cssprop){
          if (el.currentStyle)
            return el.currentStyle[cssprop]
          else if (document.defaultView && document.defaultView.getComputedStyle)
            return document.defaultView.getComputedStyle(el, "")[cssprop]
          else
            return el.style[cssprop]
        }
        if (getStyle(node,"display") == "none") hidden_objs.push({"node": node})
        if (node.parentNode && node.tagName != "BODY") find_hidden(node.parentNode)
      }
      find_hidden(hidden_node)
      hidden_objs.forEach(function(h){
        h.v = h.node.style.visibility
        h.d = h.node.style.display
        h.node.style.visibility = "hidden"
        h.node.style.display = "block"
      })
      return hidden_objs
    }
  }
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
leon_vars.color.main.dark = leon_functions.darken(leon_vars.color.main.normal)
leon_vars.color.accent = {}
leon_vars.color.accent.normal = "#ffffff"
leon_vars.color.accent.hover = "#efefef"
leon_vars.color.accent.highlight = "#aaaaaa"
leon_vars.color.accent.dark = "#888888"

leon_construct.div = function(classname,parent) {
  var div = document.createElement("div")
  div.className = classname
  if (parent) parent.appendChild(div)
  return div
}// Finds all elements that match the passed ID or Class
leon = function(name) {

  var self = {},
      objs = []

  if (name instanceof HTMLElement) {
    objs.push(name)
  }
  else if (typeof name === "object") {
    name.parent = name.parent || document.getElementsByTagName("body")[0]
    if (!name.id && !name.class) name.class = "created_by_leon"
    if (name.label && !name.id) name.id = "id_"+name.label
    leon_construct[name.type+"_input"](name)
    if (name.type == "radio") name = ["$"+name.id]
    else name = name.id ? ["#"+name.id] : ["."+name.class]
  }
  else if (typeof name === "string") {
    name = [name]
  }

  if (!name) {
    var tags = ["SELECT","INPUT"]
    tags.forEach(function(tag){
      var nodelist = document.getElementsByTagName(tag)
      for(var i = nodelist.length; i--; objs.unshift(nodelist[i]));
    })
  }
  else if (name instanceof Array) {
    var prefixes = ["#",".","$"]

    function get_nodes(n) {
      if (prefixes.indexOf(n.charAt(0)) >= 0) {
        if (n.indexOf("$") == 0) {
          var nodelist = document.getElementsByName(n.substr(1))
        }
        else {
          var nodelist = document.querySelectorAll(n)
        }
      }
      else {
        var nodelist = document.getElementsByTagName(n)
      }
      for(var i = nodelist.length; i--; objs.unshift(nodelist[i]));
    }

    name.forEach(function(n){get_nodes(n)})
  }

  function find_var(string,variable,seperator) {
    return obj.outerHTML.split("min=")[1].split(sep)[1]
  }

  objs.forEach(function(obj){
    if (obj.type == "text") {
      var text = obj.outerHTML
      if (text.indexOf("min=") > 0 && text.indexOf("max=") > 0 && text.indexOf("step=") > 0) {
        var sep = text.split("id=")[1].charAt(0)
        obj.min = text.split("min=")[1].split(sep)[1]
        obj.max = text.split("max=")[1].split(sep)[1]
        obj.step = text.split("step=")[1].split(sep)[1]
      }
    }
  })

  var others = objs.filter(function(obj) {
    return obj.type != "radio" && obj.type
  })

  var radios = objs.filter(function(obj) {
    return obj.type == "radio" && obj.type
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
    if (obj.type == "text" && obj.min && obj.max && obj.step) var type = "range"
    else var type = obj.type
    var o = {
      "items": obj,
      "type": type,
      "name": obj.id
    }
    objs.push(o)
  })

  var labellist = document.getElementsByTagName('LABEL');
  var labels = []
  for(var i = labellist.length; i--; labels.unshift(labellist[i]));

  return_radios.forEach(function(radio_group) {

    radio_group.forEach(function(obj){
      for (var i = 0; i < labels.length; i++) {
        if (labels[i].getAttribute("for") == obj.id) {
          obj.label = labels[i]
        }
      }
    })

    var temp_obj = {
          "items": radio_group,
          "type": "radio",
          "name": radio_group[0].name
        }

    objs.push(temp_obj)
  })

  objs.forEach(function(obj){
    for (var i = 0; i < labels.length; i++) {
      if (labels[i].getAttribute("for") == obj.name) {
        obj.label = labels[i]
      }
    }
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

  self.leons = {}
  objs.forEach(function(obj){
    var node = document.getElementById("leon_"+obj.name)
    if (node) {
      node.parentNode.removeChild(node)
      node = null
    }
    self.leons[obj.name] = new leon_construct[obj.type.split("-")[0]](obj)
    if (obj.items.onclick && obj.type == "button") {
      self.leons[obj.name].node.addEventListener("click",function(){
        obj.items.onclick(this.value)
      })
    }
  })

  self.color = function(color) {
    for (obj in self.leons) {
      if (self.leons[obj].set_color) self.leons[obj].set_color(color)
    }
    return self
  }

  self.size = function(size) {
    for (obj in self.leons) {
      if (self.leons[obj].set_size) self.leons[obj].set_size(size)
    }
    return self
  }

  self.hide = function() {
    for (obj in self.leons) {
      if (self.leons[obj].hide) self.leons[obj].hide()
    }
    return self
  }

  self.set = function(value) {
    for (obj in self.leons) {
      if (self.leons[obj].set_value) self.leons[obj].set_value(value)
    }
    return self
  }

  self.color(leon_vars.color.main.normal)
  self.size(leon_vars.size)

  return self

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
    font-weight: "+leon_vars.font.weight+";\
    vertical-align: middle;\
    z-index: 300;\
  }\
  .leon.button {\
    background: "+leon_vars.color.accent.normal+";\
    border: "+leon_vars.border+"px solid "+leon_vars.color.accent.highlight+";\
    color: "+leon_functions.text_color(leon_vars.color.accent.highlight)+";\
    text-align: center;\
    transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
    -webkit-transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
  }\
  .leon.button:hover {\
    cursor: pointer;\
  }\
  .leon.button > .leon.icon{\
    background-repeat: no-repeat;\
    background-size: 100%;\
    float: left;\
  }\
  .leon.button > .leon.icon.small{\
    height: "+(leon_vars.font.size.small+2)+"px;\
    margin-right: "+parseFloat(leon_vars.padding.small.split(" ")[1],10)+"px;\
    padding: 0px;\
    width: "+(leon_vars.font.size.small+2)+"px;\
  }\
  .leon.button > .leon.icon.medium{\
    height: "+(leon_vars.font.size.medium+2)+"px;\
    margin-right: "+parseFloat(leon_vars.padding.medium.split(" ")[1],10)+"px;\
    padding: 0px;\
    width: "+(leon_vars.font.size.medium+2)+"px;\
  }\
  .leon.button > .leon.icon.large{\
    height: "+(leon_vars.font.size.large+2)+"px;\
    margin-right: "+parseFloat(leon_vars.padding.large.split(" ")[1],10)+"px;\
    padding: 0px;\
    width: "+(leon_vars.font.size.large+2)+"px;\
  }\
  .leon.button.active {\
    border-right-width: "+leon_vars.border+"px !important;\
  }\
  .leon.button.active:hover {\
    cursor: pointer;\
  }\
  .leon.radio {\
    display: inline-block;\
    margin: 0px;\
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
  }\
  .leon.small {\
    font-size: "+leon_vars.font.size.small+"px;\
    padding: "+leon_vars.padding.small+";\
  }\
  .leon.medium {\
    font-size: "+leon_vars.font.size.medium+"px;\
    padding: "+leon_vars.padding.medium+";\
  }\
  .leon.large {\
    font-size: "+leon_vars.font.size.large+"px;\
    padding: "+leon_vars.padding.large+";\
  }\
  .leon.select {\
    display: inline-block;\
    margin: 0px;\
    position: relative;\
  }\
  .leon.select.active {\
    z-index: 400;\
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
    opacity: 0.5;\
    transform: rotate(90deg);\
    -moz-transform: rotate(90deg);\
    -webkit-transform: rotate(90deg);\
  }\
  .leon.button.small > .leon.arrow {\
    font-size: "+leon_vars.font.size.small*1.5+"px;\
    height: "+leon_vars.font.size.small+"px;\
    line-height: "+leon_vars.font.size.small+"px;\
    margin-left: "+leon_vars.font.size.small/2+"px;\
    margin-right: "+leon_vars.font.size.small/6+"px;\
    width: "+leon_vars.font.size.small*0.75+"px;\
  }\
  .leon.button.medium > .leon.arrow {\
    font-size: "+leon_vars.font.size.medium*1.5+"px;\
    height: "+leon_vars.font.size.medium*1.25+"px;\
    line-height: "+leon_vars.font.size.medium+"px;\
    margin-left: "+leon_vars.font.size.medium/3+"px;\
    margin-right: "+leon_vars.font.size.medium/4+"px;\
    width: "+leon_vars.font.size.medium*0.75+"px;\
  }\
  .leon.button.large > .leon.arrow {\
    font-size: "+leon_vars.font.size.large*1.5+"px;\
    height: "+leon_vars.font.size.large+"px;\
    line-height: "+leon_vars.font.size.large+"px;\
    margin-left: "+leon_vars.font.size.large/2+"px;\
    margin-right: "+leon_vars.font.size.large/6+"px;\
    width: "+leon_vars.font.size.large*0.75+"px;\
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
  .leon.textbox {\
    background: "+leon_vars.color.accent.normal+";\
    border: "+leon_vars.border+"px solid "+leon_vars.color.accent.highlight+";\
    color: "+leon_functions.text_color(leon_vars.color.accent.normal)+";\
    margin: 0px;\
    transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
    -webkit-transition: color "+leon_vars.time.hover+"s, background "+leon_vars.time.hover+"s, border-color "+leon_vars.time.hover+"s;\
  }\
  .leon.textbox:hover {\
    background: "+leon_vars.color.accent.hover+";\
    cursor: pointer;\
  }\
  .leon.textbox:focus {\
    background: "+leon_vars.color.accent.normal+";\
    outline: none;\
  }\
  .leon.range {\
    margin: 0px;\
    padding: 0px;\
  }\
  .leon.range.slider {\
    background: "+leon_vars.color.accent.dark+";\
    margin: 0px;\
    position: relative;\
    -webkit-touch-select: none;\
     -webkit-user-select: none;\
      -khtml-user-select: none;\
        -moz-user-select: none;\
         -ms-user-select: none;\
             user-select: none;\
  }\
  .leon.range.slider > div {\
    -webkit-touch-select: none;\
     -webkit-user-select: none;\
      -khtml-user-select: none;\
        -moz-user-select: none;\
         -ms-user-select: none;\
             user-select: none;\
  }\
  .leon.range.slider.small {\
    height: 21px;\
  }\
  .leon.range.slider.medium {\
    height: 25px;\
  }\
  .leon.range.slider.large {\
    height: 37px;\
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

  var self = this

  var html = item.innerHTML ? item.innerHTML : item.id

  if (leon_vars.autohide) item.style.display = "none"

  var label = document.createElement("div")
  label.className = "leon label"
  label.innerHTML = html

  if (parent) parent.appendChild(label)
  else item.parentNode.insertBefore(label,item)

  self.item = item
  self.node = label

  self.set_size = function(size) {
    self.node.className = "leon label "+size
    return self
  }

  return self

}
leon_construct.select_input = function(params) {

  if (params.label) {
    label = document.createElement("label")
    label.innerHTML = params.label
    label.setAttribute("for",params.id)
    params.parent.appendChild(label)
  }

  select = document.createElement("select")
  if (params.id) select.id = params.id
  if (params.class) select.className = params.class
  if (params.event) {
    if (typeof params.event === "string") params.event = window[params.event]
    select.onchange = function(){ params.event(this.value,params.id) }
  }

  params.parent.appendChild(select)
  if (params.data instanceof Array) {
    var temp_data = {}
    params.data.forEach(function(d){
      temp_data[d] = d
    })
    params.data = temp_data
  }

  for (name in params.data) {
    if (!params.default) params.default = name
    option = document.createElement("option")
    option.value = name
    option.innerHTML = params.data[name]
    if (name == params.default) option.selected = true
    select.appendChild(option)
  }

}

leon_construct.radio_input = function(params) {

  if (params.label) {
    legend = document.createElement("legend")
    legend.innerHTML = params.label
    legend.id = params.id
    params.parent.appendChild(legend)
  }

  if (params.data instanceof Array) {
    var temp_data = {}
    params.data.forEach(function(d){
      temp_data[d] = d
    })
    params.data = temp_data
  }

  for (name in params.data) {
    if (!params.default) params.default = name

    radio = document.createElement("input")
    radio.type = "radio"
    radio.value = name
    radio.id = name
    radio.name = params.id
    if (params.event) {
      if (typeof params.event === "string") params.event = window[params.event]
      radio.onclick = function(){ params.event(this.value,params.id) }
    }
    if (name == params.default) radio.checked = true
    params.parent.appendChild(radio)

    label = document.createElement("label")
    label.setAttribute("for",name)
    label.innerHTML = params.data[name]
    params.parent.appendChild(label)
  }

}

leon_construct.range_input = function(params) {

  if (params.label) {
    label = document.createElement("label")
    label.innerHTML = params.label
    label.setAttribute("for",params.id)
    params.parent.appendChild(label)
  }

  range = document.createElement("input")
  range.type = "range"
  range.min = params.data.min
  range.max = params.data.max
  range.step = params.data.step
  range.value = params.default || range.min
  if (params.id) range.id = params.id
  if (params.class) range.className = params.class
  if (params.event) {
    if (typeof params.event === "string") params.event = window[params.event]
    range.onchange = function(){ params.event(this.value,params.id) }
  }
  params.parent.appendChild(range)

}

leon_construct.button_input = function(params) {

  if (params.label) {
    label = document.createElement("label")
    label.innerHTML = params.label
    label.setAttribute("for",params.id)
    params.parent.appendChild(label)
  }

  button = document.createElement("input")
  button.type = "button"
  if (params.data) button.value = params.data
  if (params.id) button.id = params.id
  if (params.class) button.className = params.class
  if (params.event) {
    if (typeof params.event === "string") params.event = window[params.event]
    button.onclick = function(){ params.event(this.value,params.id) }
  }
  params.parent.appendChild(button)

}

leon_construct.text_input = function(params) {

  if (params.label) {
    label = document.createElement("label")
    label.innerHTML = params.label
    label.setAttribute("for",params.id)
    params.parent.appendChild(label)
  }

  text = document.createElement("input")
  text.type = "text"
  if (params.data) text.value = params.data
  if (params.id) text.id = params.id
  if (params.class) text.className = params.class
  if (params.event) {
    if (typeof params.event === "string") params.event = window[params.event]
    text.onchange = function(){ params.event(this.value,params.id) }
  }
  params.parent.appendChild(text)

}

leon_construct.checkbox_input = function(params) {

  if (params.label) {
    label = document.createElement("label")
    label.innerHTML = params.label
    label.setAttribute("for",params.id)
    params.parent.appendChild(label)
  }

  checkbox = document.createElement("input")
  checkbox.type = "checkbox"
  if (params.default) checkbox.checked = true
  if (params.data) checkbox.value = params.data
  if (params.id) checkbox.id = params.id
  if (params.class) checkbox.className = params.class
  if (params.event) {
    if (typeof params.event === "string") params.event = window[params.event]
    checkbox.onclick = function(){ params.event(this.checked,params.id) }
  }
  params.parent.appendChild(checkbox)

}
/*
CUSTOM BUTTON CREATOR
Creates a custom button when passed an item
*/
leon_construct.button = function(item,parent) {

  var self = this
  self.size = "medium"

  self.active = false

  if (typeof item == "string") {
    var html = item
  }
  else if (item.label) {
    var label = item.label
    if (typeof label != "string") {
      var html = label.innerHTML
      if (leon_vars.autohide) label.style.display = "none"
    }
    else {
      var html = label
    }
  }
  else if (item.innerHTML) {
    var html = item.innerHTML
  }
  else {
    var html = item.value
  }

  if (item.type && item.type == "button") {
    var item = item.items
    if (!html) html = item.value
  }
  self.item = item

  if (typeof item != "string" && leon_vars.autohide) item.style.display = "none"

  self.node = leon_construct.div("leon button "+self.size)

  if (item.attributes && item.attributes.icon) {
    var icon = document.createElement("div")
    icon.className = "leon icon"
    icon.style.backgroundImage = item.attributes.icon.value
    if (item.attributes.color) {
      icon.style.backgroundColor = item.attributes.color.value
    }
    self.node.appendChild(icon)
  }

  self.node.innerHTML = self.node.innerHTML + html
  if (item.value) {
    self.node.value = item.value
  }
  if (item.id) {
    self.node.id = "leon_"+item.id
  }

  if (parent) {
    parent.appendChild(self.node)
  }
  else {
    item.parentNode.insertBefore(self.node,item)
  }

  self.node.addEventListener("mouseover",function(){
    if (!self.active) {
      this.style.background = leon_vars.color.accent.hover
      this.style.color = leon_functions.text_color(leon_vars.color.accent.hover)
    }
  })

  self.node.addEventListener("mouseout",function(){
    if (!self.active) {
      this.style.background = leon_vars.color.accent.normal
      this.style.color = leon_functions.text_color(leon_vars.color.accent.highlight)
    }
  })

  self.node.addEventListener("mousedown",function(e){
    if (!self.active) {
      self.node.style.background = self.color
      self.node.style.borderColor = leon_functions.darken(self.color)
      self.node.style.color = leon_functions.text_color(self.color)
    }
  })

  self.node.addEventListener("mouseup",function(e){
    if (!self.active) {
      self.node.style.background = leon_vars.color.accent.hover
      self.node.style.borderColor = leon_vars.color.accent.highlight
      self.node.style.color = leon_functions.text_color(leon_vars.color.accent.hover)
    }
  })

  self.add_class = function(name) {
    self.node.className = self.node.className+" "+name
  }

  self.set_color = function(color) {
    if (color) self.color = color
    else self.color = leon_vars.color.main.normal
    self.active_color()
    return self
  }

  self.set_size = function(size) {
    self.node.className = self.node.className.replace(self.size,size)
    self.size = size
    return self
  }

  self.set_active = function(bool,miss) {
    if (bool && self.item.onclick && !miss) self.item.onclick()
    self.active = bool
    self.active_color()
    return self
  }

  self.active_color = function(bool) {
    if (self.active && self.color) {
      self.node.style.background = self.color
      self.node.style.borderColor = leon_functions.darken(self.color)
      self.node.style.color = leon_functions.text_color(self.color)
    }
    else {
      self.node.style.background = leon_vars.color.accent.normal
      self.node.style.borderColor = leon_vars.color.accent.highlight
      self.node.style.color = leon_functions.text_color(leon_vars.color.accent.highlight)
    }
    return self
  }

  return self

}
leon_construct.checkbox = function(obj) {

  var self = this

  self.item = obj.items
  self.color = leon_vars.color.main.normal

  self.set_value = function(value) {
    if (value) {
      self.bg.style.background = self.color
      self.button.style.left = self.button.offsetHeight+"px"
    }
    else {
      self.bg.style.background = leon_vars.color.accent.dark
      self.button.style.left = "0px"
    }
    self.item.checked = value
  }

  if (leon_vars.autohide) self.item.style.display = "none"

  self.node = leon_construct.div("leon checkbox")
  self.node.id = "leon_"+obj.name
  self.item.parentNode.insertBefore(self.node,self.item)

  if (obj.label) {
    self.label = new leon_construct.label(obj.label,self.node)
  }

  self.bg = document.createElement("div")
  self.bg.className = "leon checkbox group"
  self.node.appendChild(self.bg)

  self.bg.addEventListener("click",function(e){
    if (self.item.checked) self.set_value(false)
    else self.set_value(true)
    if (self.item.onclick) self.item.onclick()
  })

  self.button = document.createElement("div")
  self.button.className = "leon button"
  self.button.innerHTML = "&nbsp;"
  self.bg.appendChild(self.button)

  if (self.item.checked) self.set_value(true)

  self.set_size = function(size) {
    var hidden_node = leon_functions.check_hidden(self.node)
    self.button.style.padding = leon_vars.padding[size]
    self.button.style.fontSize = leon_vars.font.size[size]
    var w = self.button.offsetHeight
    self.bg.style.width = (w*2)+"px"
    self.bg.style.height = w+"px"
    w -= parseFloat(self.button.style.paddingLeft,10)
    w -= parseFloat(self.button.style.paddingRight,10)
    w -= leon_vars.border*2
    self.button.style.width = w+"px"
    if (self.item.checked) self.set_value(true)
    if (self.label) self.label.set_size(size)
    leon_functions.check_hidden(hidden_node)
    return self
  }

  self.set_color = function(color) {
    if (color) self.color = color
    else self.color = leon_vars.color.main.normal
    if (self.item.checked) self.bg.style.background = self.color
    return self
  }

  return self

}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon_construct.radio = function(obj) {

  var self = this

  self.set_value = function(value) {
    if (obj.checked.node.value != value) {
      obj.checked.item.checked = false
      obj.checked.set_active(false)
      button = self.buttons.filter(function(b){return b.item.value == value})[0]
      button.item.checked = true
      button.set_active(true)
      obj.checked = button
    }
  }

  self.set_size = function(size) {
    self.buttons.forEach(function(b){
      b.set_size(size)
    })
    if (self.label) self.label.set_size(size)
  }

  self.set_color = function(color) {
    self.buttons.forEach(function(b){
      b.set_color(color)
    })
  }

  self.node = leon_construct.div("leon radio")
  self.node.id = "leon_"+obj.name
  obj.items[0].parentNode.insertBefore(self.node,obj.items[0])

  if (obj.label) {
    self.label = new leon_construct.label(obj.label,self.node)
  }

  var buttongroup = document.createElement("div")
  buttongroup.className = "leon radio group"
  self.node.appendChild(buttongroup)

  self.buttons = []
  obj.items.forEach(function(item,i){

    var button = new leon_construct.button(item,buttongroup)

    if (i == 0) button.add_class("first")
    else if (i == obj.items.length-1) button.add_class("last")
    else button.add_class("middle")

    button.node.addEventListener("click", function(d){
      self.set_value(this.value)
    })

    if (item.checked) {
      button.set_active(true,true)
      obj.checked = button
    }

    self.buttons.push(button)

  })

  return self

}
/*
CUSTOM RANGE SLIDER CREATOR
*/
leon_construct.range = function(obj) {

  var self = this
  self.input = obj.items
  self.handles = []
  self.max_width = self.input.parentNode.offsetWidth
  self.tick_positions = {}
  self.height = 0
  self.handle_width = 0
  self.tick_indexes = {}
  self.size = "medium"
  self.min = parseFloat(self.input.min)
  self.max = parseFloat(self.input.max)
  self.step = parseFloat(self.input.step)
  self.label_step = self.step
  self.tick_step = self.step
  self.playing = false
  self.frame = self.min

  // Determine if slider is a self.range
  if (self.input.alt) self.range = true

  // Hide HTML input
  if (leon_vars.autohide) self.input.style.display = "none"

  var play_function = function() {
    if (self.frame <= self.max) {
      self.set_value(self.frame);
      self.frame += self.step;
      if (self.frame > self.max) {
        self.stop()
      }
    }
  }

  // Create range group
  this.node = leon_construct.div("leon range")
  this.node.id = "leon_"+obj.name
  this.input.parentNode.insertBefore(self.node,self.input)

  // Create label
  if (obj.label) {
    this.label = new leon_construct.label(obj.label,self.node)
  }

  // Create Play Button, if not a range slider
  if (!self.range) {

    self.play_button = new leon_construct.button("&#9658",self.node)
    self.play_button.node.addEventListener("click",function(){
        if (!self.playing) self.play()
        else self.stop()
    })

  }

  // Create Background DIV
  self.slider = new leon_construct.div("leon range slider "+self.size,self.node)

  // Create Initial Ticks
  self.ticks = []
  var x = 0
  for (var i = self.min; i <= self.max; i += self.step) {
    var tick = new leon_construct.div("leon button tick",self.slider)
    tick.style.opacity = 0
    if (self.step < 1) {
      var t = parseFloat(i.toFixed(self.step.toString().length-2))
    }
    else {
      var t = i
    }
    tick.innerHTML = t
    self.ticks.push(tick)
    self.tick_indexes[t+""] = x
    x++

    tick.addEventListener("mousedown",function(){
      self.dragging = true
      self.set_value(this.innerHTML)
    })
    tick.addEventListener("mouseup",function(){
      self.active_handle.className = "leon button handle"
      self.dragging = false
    })
  }

  // Create Main Handle
  self.handles.push(new leon_construct.button(self.input.value,self.slider))

  // Create self.range background and handle, if applicable
  if (self.range) {
    self.range = leon_construct.div("leon range "+self.size)
    self.slider.insertBefore(self.range,self.slider.firstChild)
    self.handles.push(new leon_construct.button(self.input.alt,self.slider))
  }

  // Add Handle Event Listeners
  self.handles.forEach(function(handle){
    handle.node.setAttribute("unselectable","on")
    handle.node.style.position = "absolute"
    handle.node.addEventListener("mousedown",function(){
      self.dragging = true
      self.active_handle = handle
    })
    handle.node.addEventListener("mouseup",function(){
      self.dragging = false
      self.active_handle = null
    })
  })

  // Create Tick Labels
  self.tick_labels = []
  self.ticks.forEach(function(tick,i){

    var label = document.createElement("div")

    // if (i%self.label_step == 0) {
      label.innerHTML = tick.innerHTML
      label.className = "leon button tick"
    // }
    // else if (i%self.tick_step != 0) {
    //   label.innerHTML = "&bull;"
    //   label.className = "leon button tick bullet"
    // }
    self.slider.insertBefore(label,self.ticks[0])

    self.tick_labels.push(label)

  })

  /*************/
  /* FUNCTIONS */
  /*************/

  self.set_value = function(value) {

    if (typeof value == "number") value = value+""

    if (self.range) {

      var h1 = self.handles[0].node.innerHTML,
          h2 = self.handles[1].node.innerHTML

      if (value < h1 || value <= h1+((h2-h1)/2)) {
        h1 = value
        self.handles[0].node.innerHTML = h1
        self.handles[0].node.style.left = self.tick_positions[h1]+"px"
        self.input.value = h1
        self.active_handle = self.handles[0]
      }
      else {
        h2 = value
        self.handles[1].node.innerHTML = h2
        self.handles[1].node.style.left = self.tick_positions[h2]+"px"
        self.input.value = h2
        self.active_handle = self.handles[1]
      }

      self.range.style.left = self.tick_positions[h1]+"px"
      self.range.style.width = (self.tick_positions[h2]-self.tick_positions[h1])+"px"

    }
    else if (self.input.value != value) {
      self.input.value = value
      self.handles[0].node.innerHTML = value
      self.handles[0].node.style.left = self.tick_positions[self.tick_indexes[value]]+"px"
      self.active_handle = self.handles[0]
      if (self.input.onchange) self.input.onchange()
    }

    return self
  }

  self.play = function() {

    self.playing = true
    self.play_button.set_active(true)

    var current = parseFloat(self.handles[0].node.innerHTML,10)
    if (current == self.max) self.frame = self.min;
    else self.frame = current+self.step;
    self.set_value(self.frame)
    self.frame += self.step;

    if (self.frame > self.max) {
      self.stop();
    }
    else {
      self.play_interval = setInterval(play_function,1500);
    }
    return self
  }

  self.stop = function() {
    clearInterval(self.play_interval);
    self.playing = false;
    self.play_button.set_active(false)
    self.active_handle.set_active(false)
    return self
  }

  self.set_color = function(color) {
    self.play_button.set_color(color)
    self.handles.forEach(function(handle){
      handle.set_color(color)
    })
  }

  self.set_size = function(size) {

    var hidden_node = leon_functions.check_hidden(self.node)
    var available_width = self.max_width

    self.handle_width = 0
    self.padding = parseFloat(leon_vars.padding[size].split(" ")[1],10)

    self.ticks.forEach(function(tick,i){

      tick.style.padding = leon_vars.padding[size]
      tick.style.fontSize = leon_vars.font.size[size]
      tick.style.width = "auto"

      var w = tick.offsetWidth
      if (self.handle_width < w) self.handle_width = w

    })

    // Resize label and minus width from available_width
    if (self.label) {
      self.label.set_size(size)
      available_width -= self.label.node.offsetWidth
      available_width -= parseFloat(self.label.node.style.paddingLeft,10)
      available_width -= parseFloat(self.label.node.style.paddingRight,10)
    }

    if (self.play_button) {
      self.play_button.set_size(size)
      self.play_button.node.style.marginRight = self.padding+"px"
      available_width -= self.play_button.node.offsetWidth
    }
    // self.play_button.style.width = self.play_button.offsetHeight-leon_vars.padding*2-leon_vars.border*2

    self.handles.forEach(function(handle){
      handle.set_size(size)
      handle.node.style.width = (self.handle_width-(self.padding*2))+"px"
      handle.node.style.marginLeft = (-(self.handle_width-(self.padding*2))/2)+"px"
    })

    if (self.range) {
      self.range.className = self.range.className.replace(self.size,size)
    }

    self.slider.className = self.slider.className.replace(self.size,size)
    self.slider.style.paddingLeft = (self.handle_width/2)+"px"
    self.slider.style.paddingRight = (self.handle_width/2)+"px"

    if (available_width < self.handle_width*self.ticks.length) {
      self.slider.style.width = (available_width-self.handle_width)+"px"
      self.tick_width = (available_width/self.ticks.length)-(self.padding*2)
      var i = Math.floor(available_width/self.handle_width)-1, total = self.max-self.min
      while ((total/i)%1 != 0) {
        i--
      }
      self.label_step = total/i

      var i = Math.floor(available_width/leon_vars.font.size)-1, total = self.max-self.min
      while ((total/i)%1 != 0) {
        i--
      }
      self.tick_step = total/i

    }
    else {
      self.slider.style.width = (self.handle_width*(self.ticks.length-1))+"px"
      self.tick_width = self.handle_width
    }

    self.ticks.forEach(function(tick,i){

      tick.style.marginLeft = (-(self.tick_width)/2)+"px"
      tick.style.width = self.tick_width-(self.padding*2)+"px"

      var percent = i*(100/(self.ticks.length-1))
          x1 = self.handle_width/2,
          x2 = parseFloat(self.slider.style.width,10)+x1-leon_vars.border*2

      self.tick_positions[i] = (percent/100) * (x2 - x1) + x1

      tick.style.left = self.tick_positions[i]+"px"

    })

    self.tick_labels.forEach(function(label,i){
      label.style.padding = leon_vars.padding[size]
      label.style.fontSize = leon_vars.font.size[size]
      label.style.marginLeft = (-(self.handle_width)/2)+"px"
      label.style.width = self.handle_width-(self.padding*2)+"px"
      label.style.left = self.tick_positions[i]+"px"
    })

    self.handles.forEach(function(handle){
      var value = self.tick_indexes[parseFloat(handle.node.innerHTML)]
      handle.node.style.marginLeft = (-(self.handle_width)/2)+"px"
      handle.node.style.left = self.tick_positions[value]+"px"
    })

    if (self.range) {
      var value = self.tick_indexes[parseFloat(self.handles[0].node.innerHTML)],
          value2 = self.tick_indexes[parseFloat(self.handles[1].node.innerHTML)]
      self.range.style.left = self.tick_positions[value]+"px"
      self.range.style.width = (self.tick_positions[value2]-self.tick_positions[value])+"px"
    }

    self.size = size
    hidden_node = leon_functions.check_hidden(hidden_node)

    return self
  }

  document.addEventListener("mousemove",function(e){
    if (self.dragging) {
      self.active_handle.set_active(true)
      var x = e.clientX-self.active_handle.node.parentNode.offsetLeft,
          value = self.tick_indexes[self.active_handle.node.innerHTML]
      if (x < self.tick_positions[value]-self.tick_width/2) {
        if (x > 0) {
          for (var p = self.min; p <= self.max; p += self.step) {
            if (self.step < 1) {
              var t = parseFloat(p.toFixed(self.step.toString().length-2))
            }
            else {
              var t = p
            }
            if (x < self.tick_positions[self.tick_indexes[t]]+self.tick_width/2) {
              if (t != value) self.set_value(t)
              break;
            }
          }
        }
        else if (self.min != value) self.set_value(self.min)
      }
      else if (x >= self.tick_positions[value]+self.tick_width/2) {
        if (x < parseFloat(self.slider.style.width,10)+self.handle_width) {
          for (var p = self.max; p >= self.min; p -= self.step) {
            if (self.step < 1) {
              var t = parseFloat(p.toFixed(self.step.toString().length-2))
            }
            else {
              var t = p
            }
            if (x > self.tick_positions[self.tick_indexes[t]]-self.tick_width/2) {
              if (t != value) self.set_value(t)
              break;
            }
          }
        }
        else if (self.max != value) self.set_value(self.max)
      }

    }
  })

  document.addEventListener("mouseup",function(){
    self.handles.forEach(function(handle){
      handle.set_active(false)
    })
    self.dragging = false
  })

  return self

}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon_construct.select = function(obj) {

  var self = this

  self.set_color = function(color) {
    self.selected.set_color(color)
    self.options.forEach(function(option){
      option.set_color(color)
    })
  }

  self.set_size = function(size) {

    self.dropdown.style.width = "auto"

    self.selected.set_size(size)
    if (self.label) self.label.set_size(size)

    var icon = self.selected.node.getElementsByClassName("icon")[0]
    if (icon) icon.className = "leon icon "+size

    self.width = 0
    self.padding = parseFloat(leon_vars.padding[size].split(" ")[1],10)

    var hidden_node = leon_functions.check_hidden(self.node)
    self.options.forEach(function(option){

      option.set_size(size)

      var icon = option.node.getElementsByClassName("icon")[0]
      if (icon) icon.className = "leon icon "+size

      var html = option.node.innerHTML
      option.node.innerHTML = html + self.arrow
      var arrow_width = option.node.getElementsByTagName("span")[0].offsetHeight
      option.node.innerHTML = html
      var width = option.node.offsetWidth - self.padding*2 + arrow_width
      if (width > self.width) self.width = width

    })

    self.selected.node.style.width = (self.width)+"px"

    self.dropdown.style.width = (self.width+self.padding*2+leon_vars.border*2)+"px"
    self.dropdown.style.left = self.selected.node.offsetLeft+"px"

    leon_functions.check_hidden(hidden_node)

    return self
  }

  self.show = function() {
    self.selected.set_active(true)
    self.node.className = "leon select active"
    self.dropdown.style.visibility = "visible"
    self.dropdown.style.opacity = 1
    self.dropdown.style.top = self.selected.node.offsetHeight+"px"
    self.selected.open = true
    return self
  }

  self.hide = function() {
    self.selected.set_active(false)
    self.dropdown.style.opacity = 0
    self.dropdown.style.top = "0px"
    setTimeout(function() {
      self.dropdown.style.visibility = "hidden"
      self.node.className = "leon select"
      self.selected.open = false
    },leon_vars.time.fade*1000)
    return self
  }

  self.set_value = function(value,miss) {
    if (self.input.value != value || miss) {
      var option = self.options.filter(function(o){
        return o.node.value == value;
      })[0]
      if (!option) var option = self.options[0]
      self.input.value = value
      self.selected.node.innerHTML = option.node.innerHTML + self.arrow
      if (self.input.onchange && !miss) self.input.onchange()
    }
    return self
  }

  self.input = obj.items

  self.arrow = "<span class='leon arrow'>&#8227</span>"

  self.node = leon_construct.div("leon select")
  self.node.id = "leon_"+self.input.id
  self.input.parentNode.insertBefore(self.node,self.input)

  if (obj.label) {
    self.label = new leon_construct.label(obj.label,self.node)
  }

  self.selected = new leon_construct.button(self.input,self.node)
  self.selected.open = false

  self.dropdown = document.createElement("div")
  self.dropdown.className = "leon select dropdown"
  self.dropdown.id = "leon_dropdown_"+self.input.id
  self.dropdown.style.left = self.selected.node.offsetLeft+"px"
  self.node.appendChild(self.dropdown)

  self.options = []
  for (var i = 0; i < self.input.length; i++) {
    self.options.push(new leon_construct.button(self.input[i],self.dropdown))
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

  self.options.forEach(function(option,i){

    if (option.item.selected) self.set_value(option.item.value,true)

    if (i == 0) option.add_class("first")
    else if (i == self.input.length-1) option.add_class("last")
    else option.add_class("middle")

    option.node.addEventListener("click", function(e){
      e.stopPropagation()
      self.set_value(option.item.value)
      self.hide()
    })
  })

  return self

}
/*
CUSTOM RADIO TOGGLE CREATOR
Creates a custom toggle menu, when passed the name of a radio button group
*/
leon_construct.text = function(obj) {

  var self = this
  self.input = obj.items
  self.node = leon_construct.div("leon text")
  self.node.id = "leon_"+obj.name
  self.input.parentNode.insertBefore(self.node,self.input)
  self.color = leon_vars.color.main.normal

  if (obj.label) {
    self.label = obj.label
    self.node.appendChild(self.label)
  }

  self.node.appendChild(self.input)

  self.input.onfocus = function() {
    this.style.borderColor = self.color
  }

  self.input.onblur = function() {
    this.style.borderColor = leon_vars.color.accent.highlight
  }

  self.set_color = function(color) {
    self.color = color
    if (self.input == document.activeElement) {
      self.input.style.borderColor = self.color
    }
  }

  self.set_size = function(size) {
    self.input.className = self.input.className + "leon textbox "+size
    if (self.label) self.label.className = "leon label "+size
  }

  return self

}

function Key() {
    
  var attr_type;
      
  function util(selection) {
    
    selection.each(function(raw_data) {
      
      reset_check = function() {
        if (key_solos.length || key_filters.length) {
          reset_button.style("display","inline-block")
        }
        else {
          reset_button.style("display","none")
        }
      }
      
      var key = this,
          margin = 2,
          size = 30,
          key_filters = [],
          key_solos = [],
          depth = dataviva.depths(attr_type)[0];
          
      var data = d3.values(raw_data).filter(function(d){
        return d.id.length == depth
      })
          
      d3.select(key).append("div")
        .attr("class","leon label medium")
        .text(attr_type)
          
      data.sort(function(a, b){
        if (attr_type == "bra" || attr_type == "wld") {
          var a_name = a.name
          var b_name = b.name
        } else {
          var a_name = d3.rgb(a.color).hsl().h
          var b_name = d3.rgb(b.color).hsl().h
          if (d3.rgb(a.color).hsl().s == 0) a_name = 361
          if (d3.rgb(b.color).hsl().s == 0) b_name = 361
        }
        if(a_name < b_name) return -1;
        if(a_name > b_name) return 1;
        return 0;
      })
      
      data.forEach(function(d,i){
        d.icon = dataviva.icon(d.id,attr_type)
        var cat = d3.select(key).append("div")
          .attr("id","key"+d.id)
          .attr("class","key_icon_container")
          .on(vizwhiz.evt.over, function(e){
            
            var x_pos = this.offsetLeft+(this.offsetWidth/2)
            var y_pos = key.parentNode.offsetTop+key.offsetTop+this.offsetTop+(this.offsetHeight/2)
            
            key_filter = function() {
              if (key_filters.indexOf(d.id) < 0) key_filters.push(d.id)
              else key_filters.splice(key_filters.indexOf(d.id),1)
              if (key_solos.indexOf(d.id) >= 0) {
                key_solos.splice(key_solos.indexOf(d.id),1)
                app.update("solo",key_solos)
              }
              app.update("filter",key_filters)
              reset_check()
            }
            
            key_solo = function() {
              if (key_solos.indexOf(d.id) < 0) key_solos.push(d.id)
              else key_solos.splice(key_solos.indexOf(d.id),1)
              if (key_filters.indexOf(d.id) >= 0) {
                key_filters.splice(key_filters.indexOf(d.id),1)
                app.update("filter",key_filters)
              }
              app.update("solo",key_solos)
              reset_check()
            }
            
            if (key_filters.indexOf(d.id) >= 0) {
              var filter_class = "leon button medium active"
            }
            else {
              var filter_class = "leon button medium"
            }
            
            if (key_solos.indexOf(d.id) >= 0) {
              var solo_class = "leon button medium active"
            }
            else {
              var solo_class = "leon button medium"
            }
            
            var html = "<div class='filter_buttons'>\
                <div onclick='key_filter()' class='"+filter_class+"'>"+dataviva.format.text("filter")+"</div>\
                <div onclick='key_solo()' class='"+solo_class+"'>"+dataviva.format.text("solo")+"</div>\
              </div>"
              
            if (attr_type == "bra") var s = "default"
            else var s = "knockout"
            
            vizwhiz.tooltip.remove("key")
            vizwhiz.tooltip.create({
              "title": d.name,
              "color": d.color,
              "icon": d.icon,
              "style": s,
              "html": html,
              "id": "key",
              "x": x_pos,
              "y": y_pos-3,
              "offset": 0,
              "arrow": true,
              "mouseevents": this
            })
          })
          .on(vizwhiz.evt.out, function(e){
            vizwhiz.tooltip.remove("key")
          })
          .append("div")
            .attr("id","key_icon"+d.id)
            .attr("class","key_icon")
            .style("background-image","url('"+d.icon+"')")
            .style("background-color",function(){
              return attr_type == "bra" ? "none" : d.color
            })
        
      })
       
      var reset_button = d3.select(key).append("div")
        .attr("class","leon button medium square")
        .on(vizwhiz.evt.over,function(){
          
          var x_pos = this.offsetLeft+(this.offsetWidth/2)
          var y_pos = key.parentNode.offsetTop+key.offsetTop+this.offsetTop
          
          vizwhiz.tooltip.remove("key")
          vizwhiz.tooltip.create({
            "id": "key",
            "x": x_pos,
            "y": y_pos,
            "offset": 0,
            "arrow": true,
            "description": dataviva.format.text("reset")
          })
        })
        .on(vizwhiz.evt.out,function(){
          vizwhiz.tooltip.remove("key")
        })
        .on(vizwhiz.evt.click,function(){
          key_filters = []
          key_solos = []
          app.update("filter",key_filters)
          app.update("solo",key_solos)
          vizwhiz.tooltip.remove("key")
          reset_check()
        })
      
      reset_button.append("i")
        .attr("class","icon-remove")
        
      reset_check()
      
    })
  }
  
  util.type = function(value) {
    attr_type = value;
    return util;
  }
  
  return util
}
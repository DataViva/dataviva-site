function Key() {
    
  var attr_type;
      
  function util(selection) {
    
    selection.each(function(raw_data) {
      
      var key = this,
          margin = 2,
          size = 30,
          key_filters = [],
          key_solos = [],
          depth = visual.depths(attr_type)[0];
          
      var data = d3.values(raw_data).filter(function(d){
        return d.id.length == depth
      })
          
      d3.select(key).append("div")
        .attr("class","leon label")
        .text(attr_type)
          
      data.sort(function(a, b){
        if (attr_type == "geo" || attr_type == "country") {
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
        d.icon = visual.icon(d.id,attr_type)
        var cat = d3.select(key).append("div")
          .attr("id","key"+d.id)
          .attr("class","key_icon_container")
          .on(vizwhiz.evt.click, function(e){
            
            if (d3.event.shiftKey) {
              if (key_solos.indexOf(d.id) < 0) key_solos.push(d.id)
              else key_solos.splice(key_solos.indexOf(d.id),1)
              if (key_filters.indexOf(d.id) >= 0) {
                key_filters.splice(key_filters.indexOf(d.id),1)
                app_filter(key_filters)
              }
              solo(key_solos)
            }
            else {
              if (key_filters.indexOf(d.id) < 0) key_filters.push(d.id)
              else key_filters.splice(key_filters.indexOf(d.id),1)
              if (key_solos.indexOf(d.id) >= 0) {
                key_solos.splice(key_solos.indexOf(d.id),1)
                solo(key_solos)
              }
              app_filter(key_filters)
            }
            
            data.forEach(function(k){
              if (key_solos.indexOf(k.id) >= 0 && app.solo) {
                d3.select("div#key_icon"+k.id)
                  .style("margin","0px")
                  .style("width",(size+(margin*2))+"px")
                  .style("height",(size+(margin*2))+"px")
                  .style("background-size",(size+(margin*2))+"px")
              } else if (key_filters.indexOf(k.id) >= 0 && app.filter) {
                d3.select("div#key_icon"+k.id)
                  .style("margin",(margin+(size/4))+"px")
                  .style("width",(size/2)+"px")
                  .style("height",(size/2)+"px")
                  .style("background-size",(size/2)+"px")
              } else {
                d3.select("div#key_icon"+k.id)
                  .style("margin",margin+"px")
                  .style("width",size+"px")
                  .style("height",size+"px")
                  .style("background-size",size+"px")
              }
            })
          })
          .on(vizwhiz.evt.over, function(e){
            var x_pos = this.offsetLeft+(this.offsetWidth/2)
            var y_pos = key.parentNode.offsetTop+key.offsetTop+this.offsetTop
            var data = [
              {"name": "Click", "value": "toggle this category"},
              {"name": "ShiftClick", "value": "solo this category"}
            ]
            vizwhiz.tooltip.create({
              "title": d.name,
              "color": d.color,
              "data": data,
              "x": x_pos,
              "y": y_pos,
              "offset": 0,
              "arrow": true,
              "mouseevents": true
            })
          })
          .on(vizwhiz.evt.out, function(e){
            vizwhiz.tooltip.remove()
          })
          .append("div")
            .attr("id","key_icon"+d.id)
            .attr("class","key_icon")
            .style("background-image","url('"+d.icon+"')")
            .style("background-color",d.color)
        
      })
      
    })
  }
  
  util.type = function(value) {
    attr_type = value;
    return util;
  }
  
  return util
}
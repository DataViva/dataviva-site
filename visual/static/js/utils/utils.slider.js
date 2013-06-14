function Slider() {
  
  var callback,
      handle_value,
      title = ''
      
  function util(selection) {
    
    selection.each(function(data) {
      
      var dragging = false,
          hover = false,
          current_hand = 0,
          handles = [],
          parent = this,
          tick_size = 7 * d3.max(data,function(d){ return d.toString().length }) + 10,
          width = (tick_size*(data.length)),
          playing = false,
          play_function;

      if (handle_value instanceof Array) var currentWidth = tick_size*2
      else var currentWidth = tick_size
      
      // Remove any previous content inside of DIV
      d3.select(this).selectAll('div').remove()
      
      d3.select(this).append("a")
        .attr("class","button square")
        .attr("id","play_button")
        .style("float","left")
        .on(vizwhiz.evt.click, function(){
          if (!playing) {
            playing = true;
            d3.select("#play_button i").attr("class","icon-pause")
            if (handles[0].index == data.length-1) var i = 0;
            else var i = handles[0].index+1;
            set_slider(i);
            i++;
            var play_interval = function() {
              if (i < data.length) {
                set_slider(i);
                i++;
                if (i == data.length) {
                  stop_playback();
                }
              }
            }
            if (i == data.length) {
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
            d3.select("#play_button i").attr("class","icon-play");
          }
          
        })
        .append("i").attr("class","icon-play")
      
      if (title) {
        d3.select(this).append("div")
          .attr("class","slider_label")
          .html(title)
      }
      
      var background = d3.select(this).append("div")
        .attr("class","background")
    
      if (handle_value instanceof Array) {
        var ranger = background.append("div")
          .attr("class","ranger")
      }

      // Create the tickmarks for the slider
      var positions = []
      data.forEach(function(value,index) {
        var t = (100/(data.length))*(index)
        
        var tick = background.append("div")
          .attr("class","button tick")
          .text(value)
          .on(vizwhiz.evt.click,function(e){
            set_slider(index);
          })
          
        positions.push(t)
        
      })
      
      var handle = background.append("a")
        .attr("class","button")
        .attr("id","handle")
        .style("position","absolute")
  
      if (handle_value instanceof Array) {
    
        var handle0 = background.append("a")
          .attr("class","button")
          .attr("id","handle")
    
        handles.push({'index': data.indexOf(handle_value[0]), 'handle': handle0})
        handles.push({'index': data.indexOf(handle_value[1]), 'handle': handle})
        
        handle
          .style("left",positions[handles[1].index]+"%")
          .text(handle_value[1])
        
        handle0
          .style("left",positions[handles[0].index]+"%")
          .text(handle_value[0])
        
        ranger
          .style("left",positions[handles[0].index]+"%")
          .style("width",(positions[handles[1].index]-positions[handles[0].index])+"%")
      } 
      
      else {
        handles.push({'index': data.indexOf(handle_value), 'handle': handle})
        handle
          .style("left",positions[handles[0].index]+"%")
          .text(handle_value)
      }
  
      d3.select(document).on(vizwhiz.evt.up,function(e){
        dragging = false;
      })
  
      background.on(vizwhiz.evt.down,function(e){
        dragging = true;
      })
  
      document.addEventListener(vizwhiz.evt.move,function(e){
        if (dragging) {
          e.preventDefault()
          // CHECK THESE VARIABLES
          var pos = background.node().offsetLeft+parent.offsetLeft,
              top = e.pageX-pos-5,
              bottom = width
              
          // CHECK THESE VARIABLES
          var mouse = (top/bottom)*100
          var index = 0
          while(index < positions.length) {
            if(mouse > positions[index]) {
              if(mouse < positions[index+1]) {
                set_slider(index)
                break
              } else if (!positions[index+1]) {
                set_slider(index)
                break
              }
            } else {
              set_slider(index)
              break
            }
            index++
          }
        }
      })
  
      function set_slider(index) {
        if (handle_value instanceof Array) {
          if (Math.abs(handles[0].index-index) >= Math.abs(handles[1].index-index)) current_hand = 1
          else current_hand = 0
        }
        if (index != handles[current_hand].index) {
          handles[current_hand].index = index
          handles[current_hand].handle.style("left",positions[index]+"%")
          handles[current_hand].handle.html(data[index])
          if (handle_value instanceof Array) {
            var array = [data[handles[0].index],data[handles[1].index]]
            array.sort(function(a,b){return a-b})
            ranger.style("left",positions[data.indexOf(array[0])]+"%")
            ranger.style("width",(positions[data.indexOf(array[1])]-positions[data.indexOf(array[0])])+"%")
            window[callback](array);
          } else {
            window[callback](data[handles[current_hand].index]);
          }
        }
      }
      
    })
  }
  
  util.initial_value = function(value) {
    if (!arguments.length) return handle_value
    handle_value = value
    return util
  }
  
  util.title = function(value) {
    if (!arguments.length) return title
    title = value
    return util
  }
  
  util.callback = function(value) {
    if (!arguments.length) return callback
    callback = value
    return util
  }
  
  return util
}
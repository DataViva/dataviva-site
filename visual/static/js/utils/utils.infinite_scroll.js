function infinite_scroll(selection){
  var url = window.location.href,
      format_items = function(d){ return d };
  
  // Initialize variables
  var formatDate = d3.time.format("%B %-d, %Y"),
      parseDate = d3.time.format.iso.parse,
      offset = 0,
      fetching;
  
  scroll = function(selection) {
    selection.each(function(data_passed) {
      
      var container_el = this;
      
      // On first time add
      d3.select(container_el).selectAll(".loading")
        .data([container_el])
        .enter().append("div")
        .attr("class", "loading")
      
      // The item we're going to listen on for scrolling
      d3.select(window)
          .on("scroll", maybe_fetch)
      
      // Check if we need to fetch
      function maybe_fetch() {

        // get the position of the loading div
        var loading_div_y = !d3.select(".loading").empty() ? d3.select(".loading").node().getBoundingClientRect().top : NaN;

        // if we're not currently fetching and offset if not NaN and the loader
        // y pos is less than the height of the page then fetch new items
        if (!fetching && offset >= 0 && loading_div_y < innerHeight) {
          fetch();
        }

      }
      
      // Call the server for more acitivities
      function fetch() {
        fetching = true;
  
        // Here we set the header X-Requested-With to XMLHttpRequest so the 
        // server knows it's an AJAX call
        d3.json(url+"?offset="+offset)
          .header("X-Requested-With", "XMLHttpRequest")
          .get(display);
      }
      
      // The meat and potatoes, this function get called after we've made the 
      // call to the server
      function display(error, new_data) {
        
        activities = new_data.activities
  
        // we're obviously no longer fetching
        fetching = false;
  
        // if the server returned an empty list, return and get rid of loading
        // div
        if (!activities.length) {
          if(offset == 0){
            d3.select(container_el)
              .append("p")
              .text("No items here.")
          }
          offset = NaN;
          d3.select(".loading").remove();
          return;
        }
  
        // increment offset by number of items received from server
        offset += activities.length;
  
        // using d3's helpful enter/update/exit paradigm add new items from
        // the server
        format_items(container_el, activities)
  
        // maybe the user has a super dooper tall screen (or high resolution)
        // so we need to check if we're already at the bottem, even though we
        // just added new items
        setTimeout(maybe_fetch, 50);
        
      }
      
      // call this on page load
      maybe_fetch();
      
    })
  }
  
  scroll.url = function(value) {
    if(!arguments.length) return url;
    url = value;
    return scroll;
  }
  
  scroll.format_items = function(value) {
    if(!arguments.length) return format_items;
    format_items = value;
    return scroll;
  }
  
  return scroll
  
}

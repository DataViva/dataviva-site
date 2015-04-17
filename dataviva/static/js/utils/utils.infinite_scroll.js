function infinite_scroll(selection){
  var url = window.location.href,
      refresh = false,
      remove = false,
      done = false,
      limit = 50,
      offset = 0,
      order = null,
      order_clicked = null,
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
      var inf_loading_div = d3.select(container_el).selectAll(".infinite_loading")

      inf_loading_div.data([container_el])
        .enter().append("div")
        .attr("class", "infinite_loading")
        .each(function(){
          infinite_loading = dataviva.ui.loading(".infinite_loading")
        })

      infinite_loading.text(dataviva.format.text("loading_items")).show()

      // The item we're going to listen on for scrolling
      d3.select(window)
          .on("scroll", maybe_fetch)

      // Check if we need to fetch
      function maybe_fetch() {

        // get the position of the loading div
        var loading_div_y = !d3.select(".infinite_loading").empty() ? d3.select(".infinite_loading").node().getBoundingClientRect().top : NaN;

        // if we're not currently fetching and offset if not NaN and the loader
        // y pos is less than the height of the page then fetch new items
        if(isNaN(offset)){
          offset = 0;
        }
        // console.log(done, fetching, offset, loading_div_y-50, innerHeight, refresh)
        if ((!done && !fetching && offset >= 0 && loading_div_y-50 < innerHeight) || refresh || order_clicked) {
          fetch();
        }

      }

      // Call the server for more acitivities
      function fetch() {
        fetching = true;
        refresh = false;

        // conver url to Location object
        a = url;
        // decide whether to use '?' or '&'
        a = a.split("?");
        var joiner = a.length > 1 ? "&" : "?";
        a = a.join("?");
        if (order) {
          if(order_clicked){
            a += joiner + "limit="+limit+"&offset=0&order="+order;
            order_clicked = false;
          }
          else {
            a += joiner + "limit="+limit+"&offset="+offset+"&order="+order;
          }
        }
        else {
          a += joiner + "limit="+limit+"&offset="+offset;
        }

        // Here we set the header X-Requested-With to XMLHttpRequest so the
        // server knows it's an AJAX call
        d3.json(a)
          .header("X-Requested-With", "XMLHttpRequest")
          .get(display);
      }

      // The meat and potatoes, this function get called after we've made the
      // call to the server
      function display(error, new_data) {

        activities = new_data.activities || new_data.data;
        header = new_data.headers;

        if (!header && activities.length) {
          header = d3.keys(activities[0]);
          activities = activities.map(function(d){ return d3.values(d); });
        }
        
        if (new_data.pci){
          var pci_lookup = {}
          var pci_year_i = new_data.pci.headers.indexOf("year")
          var pci_hs_id_i = new_data.pci.headers.indexOf("hs_id")
          var pci_pci_i = new_data.pci.headers.indexOf("pci")
          
          // create PCI lookup
          new_data.pci.data.forEach(function(pci){
            if(!pci_lookup[pci[pci_year_i]]){
              pci_lookup[pci[pci_year_i]] = {}
            }
            pci_lookup[pci[pci_year_i]][pci[pci_hs_id_i]] = pci[pci_pci_i]
          })
          
          // add "pci" to header
          header.push('pci')
          
          // add pci value to data
          var year_i = header.indexOf("year")
          var hs_id_i = header.indexOf("hs_id")
          activities.forEach(function(d){
            var pci_val = pci_lookup[d[year_i]][d[hs_id_i]]
            d.push(pci_val)
          })
        }

        // we're obviously no longer fetching
        fetching = false;

        // if the server returned an empty list, return and get rid of loading
        // div
        if (!activities.length) {
          if(offset == 0){
            d3.select(container_el).selectAll("p.no_data")
              .data([0])
              .enter().append("p")
              .attr("class", "no_data")
              .style({
                "font-size": "16px",
                "margin": "20px 0 0 0",
                "opacity": 0.5,
                "padding": "20px"
              })
              .text(dataviva.dictionary.no_items)
            if(remove){
              // d3.select(container_el).html('')
            }
          }
          done = true;
          offset = NaN;
          d3.select(container_el).select(".infinite_loading")
            .style("opacity", 0)
            .style("height", 0)
          return;
        }

        // increment offset by number of items received from server
        offset += activities.length;

        // using d3's helpful enter/update/exit paradigm add new items from
        // the server
        format_items(container_el, activities, offset, false, header)

        // remove no data p
        d3.select(container_el).selectAll("p.no_data").remove()

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
    if(value.split("?")[0] != url.split("?")[0]){
      refresh = true;
    }
    url = value;
    return scroll;
  }

  scroll.format_items = function(value) {
    if(!arguments.length) return format_items;
    format_items = value;
    return scroll;
  }

  scroll.remove = function(value) {
    if(!arguments.length) return remove;
    remove = value;
    return scroll;
  }

  scroll.offset = function(value) {
    if(!arguments.length) return offset;
    offset = value;
    return scroll;
  }

  scroll.order = function(value) {
    if(!arguments.length) return order;
    order = value;
    order_clicked = true;
    return scroll;
  }

  return scroll

}

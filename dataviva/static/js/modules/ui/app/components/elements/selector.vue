<template>
  <div
    class="fixed z-9999 top-0 left-0 bottom-0 right-0 w-100 h-100 dt bg-black-50"
    v-if="db"
    @click="close()">
    <div class="dtc v-mid">
      <div 
        class="br3 pb1 bg-white relative mh2 mh5-ns vh-75 overflow-hidden"
        @click.stop>
          <!-- Header -->
          <div class="bg-green br--top br2 flex flex-row flex-nowrap">
            <h4 class="f2 ma0 pa4 white">{{ db.name }}</h4>
            <a
                @click="close()"
                id="close-x"
                class="f2 white ml-auto pr4 pt3 mt2 fw7">&times;
            </a>  
          </div>   
        <div class="ph4 h-75">          
          <!-- Filters and agregations -->
          <div
            v-if="!loading && !loading_depths"
            class="w-100 pt2 clearfix" >
            <div v-if="db.group_opts.length" class="fl w-100 w-auto-l pb2">
              <h5 class="tl mb0">Group</h5> 
              <div
                v-for="(option,index) in db.group_opts"
                @click="reset_scroll_bar(); clean_search(); reset_group_filter(); group_by_property(option);"
                class="tc mv3 pv2 pv2-m pv2-l ph3 ph3-m ph3-l ba b--black-10 fl br2 ttc"
                :class="btn_format(group, option, index, db.group_opts)">
                  {{option}}
              </div>
            </div>

            <div class="fr w-100 w-auto-l pb2">
              <h5 class="tl mb0">Sort</h5> 
              <div
                v-for="(option,index) in db.order_opts"
                @click="reset_scroll_bar(); sort_list_by_property(option); update_visible_items();"
                class="tc mv3 pv2 pv2-m pv2-l ph3 ph3-m ph3-l ba b--black-10 fl br2 ttc"
                :class="btn_format(order, option, index, db.order_opts)">
                  {{db.order_labels[index]}}  
              </div>
            </div>
          </div> <!-- Filters and agregations ends -->

          <!-- Search input -->
          <form class="pb3 black-80" autocomplete="off">
            <input
              id="name" 
              class="input-reset ba b--black-10 ph3 pv2 mb2 db w-100 br3 lh-copy"
              type="text"
              aria-describedby="name-desc"
              placeholder="SEARCH"
              v-model="search"
              @keyup="reset_group_filter(); filter_list();">
          </form>

        <!-- Item list -->
        <div
          class="h-75 w-100 overflow-y-auto" id="selectable-item-list"
          v-if="!loading" @scroll="infinity_scroll($event)">
          <SelectableItem
            v-for="(item, index) in visible_items"
            :item="mount_item(item, index)"
            :key="item.id"
            @select-filter="function (fil) { select_group(item, fil) }"/>
        </div> <!-- Item list ends -->
      </div>
     </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Selector",
  props: ["db", "confs"],
  data() {
    return {
      max_depth: 0, // max aggregation level
      depth: 0, // current aggregation
      group: "", // current aggregation name
      order: "extra_info", // current order option
      search: null, // search text
      loading: true, // store if the modal is loading
      loading_depths: true, // only shows controls and finishes loading levels
      max_visible_items: 10,
      items: null, 
      visible_items: [""], 
      filter_group: { // filters data by aggregation
        group: "",
        search: "",
      },
    };
  },
  created: function() {
    if (this.db) {
      let length = this.db.group_opts.length -1;
      // Sets group level to minimum
      this.group = this.db.group_opts[length];
      this.max_depth = length;
      // Sets current depth level to minimum
      this.depth = length;
      // Gets the first order option
      this.order = this.db.order_opts[0];
    }

    this.get_data()
  },
  methods: {
    // Purpose: gets item property according to the current language
    // Input: item and property name
    // Output: property value
    t_(item, prop) {
      return item[prop + "_" + this.confs.lang];
    },

    // Purpose: checks if object is an array
    // Input: object
    is_array(obj) {
      return obj.constructor === Array;
    },

    // Purpose: finds larger item by lexical order
    compareName(a, b) {
      return (this.t_(a, "name")).localeCompare(this.t_(b, "name"));
    },

    // Purpose: finds larger item by property
    // Input: object
    // 
    compareExtraInfo(a, b) {
      return b.extra_info_content - a.extra_info_content;
    },
  
    // Purpose: checks if item id is present in list
    // Input: id and list
    check_exist(list, id) {
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === id){
          return true;
        }
      }
      return false;
    },

    // Purpose: gets data from API and calls function to read data
    async get_data() {
      var ep = this.db.endpoint;

      if(!this.is_array(ep)) {
        axios.get(this.confs.api_url + "metadata/" + ep)
          .then(response => (this.read_data(response.data, null)))
      }

      // Some selectors need data from more than one endpoint
      else {
        for (var i = 0; i < ep.length; i++) {
          var group = ep[i];
          var res = await axios.get(this.confs.api_url + "metadata/" + ep[i]);
          this.read_data(res.data, group);
        }
      }
    },

    // Purpose: splits data from differents levels when data
    // comes from the same endpoint with differents depths
    async read_depths() {
      var minor_data = this.items[this.max_depth];

      for (var j = 0; j < this.max_depth; j++) {
        for (var i = 0; i < minor_data.length; i++) {
          let item = minor_data[i][this.db.group_opts[j]];

          // Adds information about higher levels
          for (var h = 0; h < j; h++) {
            var prop = minor_data[i][this.db.group_opts[h]];

            if (prop) {
              let names = {
                name_pt: prop.name_pt,
                name_en: prop.name_en,
              }
              item[this.db.group_opts[h]] = names;
            }
          }

          if (item && !this.check_exist(this.items[j], item.id)) {
            this.items[j].push(item);
          }
        }
      }

      this.loading_depths = false;
    },

    // Purpose: checks whether item has all group depths
    // Input: item and list of groups
    have_all_groups(item, group) {
      for (let i = 0; i < group.length - 1; i++) {
        if (!item[group[i]]) {
          return false;
        }
      }

      return true;
    },

    // Purpose: filters items without depth
    // Input: array of items and list of groups
    remove_incomplete(array, group) {
      return array.filter(item => this.have_all_groups(item, group));
    },

    read_data(data, group) {
      if(!this.items) {
        this.items = []
        let depth = group ? this.db.endpoint.indexOf(group) : this.depth;

        for (var i = 0; i <= this.max_depth; i++) {
          this.items[i] = [];
        }

        this.items[depth] = Object.values(data);

        if (!this.is_array(this.db.endpoint)) {
          this.items[depth] = this.remove_incomplete(this.items[depth], this.db.group_opts);
        }

        for (var i = 0; i < this.items[depth].length; i++) {
          this.items[depth][i].extra_info_content = Math.floor(Math.random() * 10000);
        }
        if (!group) {
          this.read_depths();
        }
        this.sort_list_by_property(this.order);
        this.update_visible_items();
        this.loading = false;
      }
      else if(group) {
        var pos = this.db.endpoint.indexOf(group);
        this.items[pos] = Object.values(data);
        this.loading_depths = false;
        this.update_visible_items();
      }
    },

    // Purpose: gets url path for items with image
    // Input: item
    // Output: url
    img_path(item) {
      let depth = this.depth;
      switch(this.db.code) {
        case "location":
          switch(depth) {
            case 1:
            case 2:
            case 3:
            case 4:
              return this.confs.s3_host + this.db.img_path[this.group] +
               item.id.substring(0,2) + ".png";
          }
        case "trade_partner":
          switch(depth) {
            case 0:
            case 1:
              return this.confs.s3_host + this.db.img_path[this.group] +
                item.id + ".png";
          }
      }
    },

    group_opts(list) {
      return list.slice(list.indexOf(this.group) + 1, list.length);
    },

    mount_item(item, index) {
      var mounted_item = {
        id: item.id,
        name: item.name_pt,
        url: "/" + this.db.code + "/" + item.id,
        id_description: this.db.id_description,
        extra_info: this.db.extra_info_label,
        extra_info_content: item.extra_info_content,
        filter_options: this.group_opts(this.db.group_opts),
      }

      if(this.db.img_path && this.db.img_path[this.group]){
        mounted_item.img = this.img_path(item);
      } else {
        mounted_item.icon = this.db.icon.item

        if (this.db.code === "location") {
          mounted_item.icon += item.id;
        }
        else if (this.db.code === "occupation") {
          mounted_item.icon += item.id.substring(0,1);
        }
        else if (this.db.code === "product") {
          if (item.product_section) {
            mounted_item.icon += item.product_section.id;
          }
          else {
            mounted_item.icon += item.id;
          }
        } 
        else if (this.db.code === "hedu_course") {
          mounted_item.icon += item.id.substring(0,2);
        }
      }

      if(index % 2 == 0){
        mounted_item.bg_light_grey = "bg-near-white";
      }

      return mounted_item;
    },

    // Purpose: updates visible items 
    update_visible_items() {
      let max = this.max_visible_items;
      this.visible_items = this.items[this.depth].slice(0, max);
    },

    sort_list_by_property(order) {
      this.items[this.depth].sort(this.get_compare_function(order));

      this.order = order;
    },

    // Purpose: gets corresponding depth of a group name
    // Input: group
    // Output: depth level
    corresponding_depth(group) {
      return this.db.group_opts.indexOf(group);
    },

    set_depth(group) {
      this.depth = this.corresponding_depth(group);
    },

    get_compare_function(order) {
      if (order === "name"){
        return this.compareName;
      } else {
        return this.compareExtraInfo;
      }
    },

    reset_group_filter() {
      this.filter_group = {};
    },

    // Purpose: cleans the search text field
    clean_search() {
      this.search = null;
    },

    // Purpose: shows items in group depth level 
    // Input: group depth name  
    group_by_property(group) {
      this.group = group;
      this.set_depth(group);

      this.sort_list_by_property(this.order);
      this.update_visible_items();
    },

    filter_list() {
      this.visible_items = this.items[this.depth]
        .filter(item => {
          return new RegExp(this.search.toLowerCase())
            .test(item.name_en.toLowerCase())
        })
          .sort(this.get_compare_function(this.order))
          .slice(0, this.max_visible_items)
    },

    filter_by_group(search, group) {
      this.visible_items = this.items[this.depth]
        .filter(item => {
          return new RegExp(search.toLowerCase())
            .test(item[group].name_pt.toLowerCase())
        })
        .sort(this.get_compare_function(this.order))
        .slice(0, this.max_visible_items)
    },

    btn_format(order, option, index, order_opts) {
      var clickable = "pointer grow"
      var classes = order == option ? "bg-moon-gray" : clickable;
      classes += index == order_opts.length - 1 ? " br--right" : " br--left";
      classes += index != 0 ? " br--right" : "";
      return classes;
    },

    select_group(item, group) {
      var father_group = this.group;
      this.set_depth(group);
      this.filter_group.group = father_group;
      this.filter_group.search = this.t_(item, "name");
      this.filter_by_group(this.t_(item, "name"), father_group);
      this.group = group;
    },

    // Purpose: requests parent component to hide modal
    close() {
      this.$emit("close")
    },

    // Purpose: increases the number of showed items when
    // the scroll end is reached
    // Input: scroll event
    infinity_scroll(event) {
      var div = document.getElementById("selectable-item-list");
      var end_scroll = (div.scrollTop + div.offsetHeight) == div.scrollHeight;

      if (end_scroll) {
        this.max_visible_items += this.max_visible_items;
        
        if(this.filter_group.search) {
          var filter = Object.values(this.filter_group);
          this.filter_by_group(filter[1], filter[0]);
        }
        else if(this.search){
          this.filter_list();
        }
        else {
          this.update_visible_items();
        }
      }
    },

    reset_scroll_bar() {
      let itemDiv = document.getElementById("selectable-item-list");
      itemDiv.scrollTop = 0;
    }, 
  },
  computed: {
  }
};
</script>

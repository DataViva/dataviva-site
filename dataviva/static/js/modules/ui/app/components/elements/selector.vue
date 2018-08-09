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
                @click="reset_scroll_bar(); reset_group_filter(); group_by_property(option);"
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
          </div> <!-- Filters and agregations end -->

          <!-- Search input -->
          <form class="pb3 black-80">
            <input
              id="name" 
              class="input-reset ba b--black-10 pa3 mb2 db w-100 br3 ttu"
              type="text"
              aria-describedby="name-desc"
              placeholder="search"
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
        </div> <!-- Item list end -->
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
      max_depth: 0, // max agregation level
      depth: 0, // actual agregation
      group: "", // actual agregation name
      order: "extra_info", // actual order option
      search: null, // search text
      loading: true, // store if the modal is loading
      loading_depths: true, // only show controls and finish to load levels
      max_visible_items: 10,
      items: null, // array of data
      visible_items: [""], // visible items
      filter_group: { // filter data by agregation
        group: "",
        search: "",
      },
    };
  },
  created: function() {
    if (this.db) {
      let length = this.db.group_opts.length -1;
      // Set group level to minimal
      this.group = this.db.group_opts[length];
      this.max_depth = length;
      // Set actual depth level to minimal
      this.depth = length;
      // Get the first order option
      this.order = this.db.order_opts[0];
    }

    this.get_data()
  },
  methods: {
    // Propose: get item property according with the actual lang
    // Receive: the item and the name of the property
    // Return: value of the property
    t_(item, prop) {
      return item[prop + "_" + this.confs.lang];
    },
    // Propose: check if object is a array
    // Receive: an object
    is_array(obj) {
      return obj.constructor === Array;
    },
    // Propose: discovery the larger item by lexical order
    // Receive: an object
    // Return: (-1) - if a comes first
    //         ( 1) - if b comes first
    //         ( 0) - if they are igual
    compareName(a, b) {
      if (this.t_(a, "name") < this.t_(b, "name")) {
        return -1;
      }
      if (this.t_(a, "name") > this.t_(b, "name")) {
        return 1;
      }
      return 0;
    },
    // Propose: discovery the larger item by property
    // Receive: an object
    // Return: (-1) - if a is lower than b
    //         ( 1) - if a is higher than b
    //         ( 0) - if they are igual
    compareExtraInfo(a, b) {
      if (a.extra_info_content < b.extra_info_content) {
        return 1;
      }
      if (a.extra_info_content > b.extra_info_content) {
        return -1;
      }
      return 0;
    },
    // Propose: check if item id is present is list
    // Receive: a list and an id
    check_exist(list, id) {
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === id){
          return true;
        }
      }
      return false;
    },
    // Propose: get data from API and call fuction to read
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
    // Propose: split data from differents levels when data
    // comes from the same endpoint with differents depths
    async read_depths() {
      var minor_data = this.items[this.max_depth];

      for (var j = 0; j < this.max_depth; j++) {
        for (var i = 0; i < minor_data.length; i++) {
          let item = minor_data[i][this.db.group_opts[j]];

          // Add information about superior levels
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
    // Propose: check if item have all groups depth
    // Receive: the item and the list of groups
    have_all_groups(item, group) {
      for (let i = 0; i < group.length - 1; i++) {
        if (!item[group[i]]) {
          return false;
        }
      }

      return true;
    },
    // Propose: filter items without depth
    // Receive: array of items and the list of groups
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
    // Propose: get url path for items with image
    // Receive: the item
    // Return: the url to respective image
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
        extra_info_content: "",
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
    // Propose: update visible items for user
    update_visible_items() {
      let max = this.max_visible_items;
      this.visible_items = this.items[this.depth].slice(0, max);
    },
    sort_list_by_property(order) {
      this.items[this.depth].sort(this.get_compare_function(order));

      this.order = order;
    },
    // Propose: get corresponding depth of a group name
    // Receive: the group
    // Return: the depth level
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
    // Propose: clean the search text field
    clean_search() {
      this.search = null;
    },
    // Propose: show items in group depth level 
    // Receive: group depth name  
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
    // Propose: request parent component to hide this modal
    close() {
      this.$emit("close")
    },
    // Propose: increase the number of showed items when
    // user reaches the scroll end
    // Receive: the scroll event
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

<template>
  <div class="fixed z-9999 top-0 left-0 bottom-0 right-0 w-100 h-100 dt bg-black-50" v-if="db" @click="close()">
    <div class="dtc v-mid">
      <div class="br3 bg-white relative mh2 mh5-ns vh-75 overflow-hidden" @click.stop>
        <div class="h-25">
          <!-- Header -->
          <div class="bg-green br--top br2">
            <h4 class="f2 ma0 pa4 white">{{t_(db, "name")}}</h4>
          </div>

          <!-- Search input -->
          <form class="pa4 pb2 black-80">
            <input id="name" 
              class="input-reset ba b--black-10 pa3 mb2 db w-100 br3"
              type="text"
              aria-describedby="name-desc"
              placeholder="Search"
              v-model="search"
              v-on:keyup="filter_list()">
          </form>

          <!-- Filters and agregations -->
          <div class="w-100 ph4">
            <div class="fl">
              <h4 class="ma0 tl mb1">Group</h4>
              <div
                v-for="(option,index) in db.group_opts"
                v-on:click="group_by_property(option)"
                class="tc pa3 ba b--black-10 fl br2 ttc"
                v-bind:class="button_format(group, option, index, db.group_opts)">
                  {{option}}
              </div>
            </div>

            <div class="fr">
              <h4 class="ma0 tl mb1">Sort</h4>
              <div
                v-for="(option,index) in db.order_opts"
                v-on:click="sort_list_by_property(option)"
                class="tc pa3 ba b--black-10 fl br2 ttc"
                v-bind:class="button_format(order, option, index, db.order_opts)">
                  {{db.order_labels[index]}}  
              </div>
            </div>
          </div>
        </div>

        <!-- Itens list -->
        <div
          class="pa4 h-75 w-100 overflow-y-scroll" id="selectable-item-list"
          v-if="!loading" v-on:scroll="infinity_scroll($event)">
          <SelectableItem
            v-for="(item, index) in visible_items"
            v-bind:item="mount_item(item, index)"
            :key="item.id"
            v-on:select-filter="select_group"/>
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
      max_depth: 0,
      depth: 0,
      group: "",
      order: "extra_info",
      search: null,
      loading: true,
      max_visible_items: 10,
      items: [""],
      visible_items: [""],
    };
  },
  created: function() {
    this.get_data()

    if (this.db) {
      let length = this.db.group_opts.length -1;
      this.group = this.db.group_opts[length];
      this.max_depth = length;
      this.depth = length;
    }
  },
  mounted: function() {
  },
  methods: {
    t_(item, prop) {
      return item[prop + "_" + this.confs.lang];
    },
    get_data() {
      axios.get(this.confs.api_url + "metadata/" + this.db.endpoint)
      .then(response => (this.read_data(response.data)))
    },
    check_exist(list, id) {
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === id){
          return true;
        }
      }
      return false;
    },
    read_depths() {
      for (var j = 0; j < this.max_depth; j++) {
        for (var i = 0; i < this.items[this.max_depth].length; i++) {
          let item = this.items[this.max_depth][i][this.db.group_opts[j]];
          if (!this.check_exist(this.items[j], item.id)) {
            this.items[j].push(item);
          }
        }
      }
    },
    read_data(data) {
      let depth = this.depth;
      for (var i = 0; i < this.max_depth; i++) {
        this.items[i] = [];
      }
      this.items[depth] = Object.values(data)

      for (var i = 0; i < this.items[depth].length; i++) {
        this.items[depth][i].extra_info_content = Math.floor(Math.random() * 10000);
      }
      this.visible_items = this.items[depth]
        .slice(0, this.max_visible_items);
      this.sort_list_by_property("extra_info");
      this.read_depths();
      this.loading = false;
    },
    img_path(item) {
      let depth = this.depth;
      switch(this.db.code) {
        case "location":
          switch(depth) {
            case 1:
              return "";
            case 4:
              return this.db.img_path + item.region.id
                + item.state.abbr_pt.toLowerCase() + ".png";
          }
        case "occupation":
          return this.db.img_path + item.id + "_black.png";
        case "industry":
          return "";
        case "product":
          return "";
        case "trade_partner":
          return "" + item.continent.id + "_black.png";
        case "university":
          return "";
        case "hedu_course":
          return "";
        case "basic_course":
          return "";
      }
    },
    group_opts(list) {
      return list.slice(0, list.length - list.indexOf(this.group) - 1);
    },
    mount_item(item, index) {
      var mounted_item = {
        id: item.id,
        name: item.name_pt,
        url: "/" + this.db.code + "/" + item.id,
        id_description: "IBGE ID",
        img: this.confs.s3_host + this.img_path(item),
        extra_info: this.db.extra_info_label,
        // extra_info_content: item.extra_info_content,
        filter_options: this.group_opts(this.db.group_opts),
      }

      if(index % 2 == 0){
        mounted_item.bg_light_grey = "bg-near-white";
      }

      return mounted_item
    },
    compareName(a, b) {
      if (a.name_en < b.name_en) {
        return -1;
      }
      if (a.name_en > b.name_en) {
        return 1;
      }
      return 0;
    },
    compareExtraInfo(a, b) {
      if (a.extra_info_content < b.extra_info_content) {
        return 1;
      }
      if (a.extra_info_content > b.extra_info_content) {
        return -1;
      }
      return 0;
    },
    update_visible_items() {
      this.visible_items = this.items[this.depth].slice(0, this.max_visible_items);
    },
    sort_list_by_property(order) {
      if (order === "name") {
        this.items[this.depth].sort(this.compareName);
      } else if (order === "extra_info") {
        this.items[this.depth].sort(this.compareExtraInfo);
      }

      this.order = order;
      this.update_visible_items();
    },
    group_by_property(group) {
      this.group = group;
      this.depth = this.db.group_opts.indexOf(group);
      this.update_visible_items();
    },
    filter_list() {
      this.visible_items = this.items[this.depth]
        .filter(item => {
          return new RegExp(this.search.toLowerCase())
            .test(item.name_en.toLowerCase())
        })
        .slice(0, this.max_visible_items)
        .sort(this.compareName)
    },
    button_format(order, option, index, order_opts) {
      var clickable = "pointer grow"
      var classes = order == option ? "bg-moon-gray" : clickable;
      classes += index == order_opts.length - 1 ? " br--right" : " br--left";
      classes += index != 0 ? " br--right" : "";
      return classes;
    },
    select_group(group) {
      console.log("Selected group: " + group)
    },
    close() {
      this.$emit("close")
    },
    infinity_scroll(event) {
      var div = document.getElementById("selectable-item-list");

      if ((div.scrollTop + div.offsetHeight) == div.scrollHeight) {
        this.max_visible_items += this.max_visible_items;
        this.visible_items = this.items[this.depth].slice(0, this.max_visible_items);
      }
    }
  },
  computed: {
  }
};
</script>

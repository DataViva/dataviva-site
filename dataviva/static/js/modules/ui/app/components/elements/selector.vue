<template>
  <div
    v-if="db"
    class="fixed z-9999 top-0 left-0 bottom-0 right-0 w-100 h-100
           dt bg-black-50"
    @click="close()">
    <div class="dtc v-mid">
      <div
        class="br3 pb1 bg-white relative mh3 mh5-ns vh-75-ns vh-100
               overflow-hidden"
        @click.stop>
        <!-- Header -->
        <div class="bg-green br--top br2 flex flex-row flex-nowrap">
          <h4
            id="modal-header-title"
            class="f2 ma0 pa4 white">{{ db.name }}</h4>
          <a
            id="close-x"
            class="f2 white ml-auto pr4 pt3 mt2 fw7"
            @click="close()">&times;
          </a>
        </div>
        <div
          class="ph4 h-75 relative">
          <!-- Filters and aggregations -->
          <div
            v-if="!loading && !loading_depths"
            class="w-100 pt2 clearfix" >
            <div
              v-if="db.group_opts.length"
              class="fl w-100 w-auto-l pb2">
              <h5 class="tl mb0">Group</h5>
              <div
                v-for="(option,index) in db.group_opts"
                :key="option"
                :class="btn_format(group, option, index, db.group_opts)"
                class="tc mv2 mv3-ns pv2 ph3 ba b--black-10
                       fl br2 ttc"
                @click="reset_scroll_bar(); clean_search();
                        reset_group_filter(); group_by_property(option);"
              >{{ option }}
              </div>
            </div>
            <div class="fr w-100 w-auto-l pb2">
              <h5 class="tl mb0">Sort</h5>
              <div
                v-for="(option,index) in db.order_opts"
                :key="option"
                :class="btn_format(order, option, index, db.order_opts)"
                class="tc mv2 mv3-ns pv2 ph3 ba b--black-10 fl
                       br2 ttc"
                @click="reset_scroll_bar(); sort_list_by_property(option);
                        update_visible_items();"
              >{{ db.order_labels[index] }}
              </div>
            </div>
          </div> <!-- Filters and aggregations ends -->
          <!-- Search input -->
          <form
            v-if="!loading"
            class="pb3 black-80"
            autocomplete="off">
            <input
              id="name"
              v-model="search"
              class="input-reset ba b--black-10 ph3 pv2 mb2 db w-100 br3
                     lh-copy"
              type="text"
              aria-describedby="name-desc"
              placeholder="SEARCH"
              @keyup="reset_group_filter(); filter_list();">
          </form>
          <Loader v-if="loading"/>
          <!-- Item list -->
          <div
            v-if="!loading"
            id="selectable-item-list"
            class="h-75 w-100 overflow-y-auto"
            @scroll="infinity_scroll()">
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
      loading: true, // stores if the modal is loading
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
  created() {
    if (this.db) {
      const length = this.db.group_opts.length - 1;
      // Sets group level to minimum
      this.group = this.db.group_opts[length];
      this.max_depth = length;
      // Sets current depth level to minimum
      this.depth = length;
      // Gets the first order option
      this.order = this.db.order_opts["0"];
    }

    this.get_data();
  },
  methods: {
    // Purpose: gets item property according to the current language
    // Input: item and property name
    // Output: property value
    t_(item, prop) {
      return item[`${prop}_${this.confs.lang}`];
    },
    // Purpose: finds larger item by lexical order
    compareName(a, b) {
      return (this.t_(a, "name")).localeCompare(this.t_(b, "name"));
    },
    // Purpose: finds larger item by property
    // Input: object
    compareExtraInfo(a, b) {
      return b.extra_info_content - a.extra_info_content;
    },
    // Purpose: checks if item id is present in list
    // Input: id and list
    check_exist(list, id) {
      for (let i = 0; i < list.length; i += 1) {
        if (list[i].id === id) {
          return true;
        }
      }
      return false;
    },
    // Purpose: gets data from API and calls function to read data
    async get_data() {
      const ep = this.db.endpoint;
      axios.get(`${this.confs.api_url}metadata/${ep}`)
        .then(response => (this.read_data(response.data)));
    },
    // Purpose: splits data from different levels when data
    // comes from the same endpoint with diverse depths
    async read_depths() {
      const minorData = this.items[this.max_depth];

      for (let j = 0; j < this.max_depth; j += 1) {
        for (let i = 0; i < minorData.length; i += 1) {
          const item = minorData[i][this.db.group_opts[j]];

          // Adds information about higher levels
          for (let h = 0; h < j; h += 1) {
            const prop = minorData[i][this.db.group_opts[h]];

            if (prop) {
              const names = {
                id: prop.id,
                name_pt: prop.name_pt,
                name_en: prop.name_en,
              };
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
      for (let i = 0; i < group.length - 1; i += 1) {
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
    // Purpose: reads response and creates dataset
    // Input: response data
    read_data(data) {
      this.items = [];
      let depth = this.depth;

      for (let i = 0; i <= this.max_depth; i += 1) {
        this.items[i] = [];
      }

      this.items[depth] = Object.values(data);

      if (["Occupations", "Products", "Trade Partners", "Higher Education",
           "Basic Courses"].includes(this.db.name)) {
        this.items[depth] = this.items[depth]
          .filter(item =>
          !this.db.hidden_ids.includes(String(item[this.db.group_opts[0]].id)));
      } else if (this.db.name === "Universities") {
        this.items[depth] = this.items[depth]
          .filter(item =>
          !this.db.hidden_ids.includes((item.school_type).toLowerCase()));
      }
      this.items[depth] =
        this.remove_incomplete(this.items[depth], this.db.group_opts);

      // Mock data
      for (let i = 0; i < this.items[depth].length; i += 1) {
        this.items[depth][i].extra_info_content =
          Math.floor(Math.random() * 10000);
      }

      this.read_depths();
      this.sort_list_by_property(this.order);
      this.update_visible_items();
      this.loading = false;
    },
    // Purpose: gets url path for items with image
    // Input: item
    // Output: url
    img_path(item) {
      let depth = this.depth;

      switch (this.db.code) {
        case "location":
          switch (depth) {
            case 1:
            case 2:
            case 3:
            case 4:
              return `${this.confs.s3_host}${this.db.img_path[this.group]}` +
                `${item.id.substring(0, 2)}.png`;
            default:
              return "";
          }

        case "trade_partner":
          switch (depth) {
            case 0:
            case 1:
              return `${this.confs.s3_host}${this.db.img_path[this.group]}` +
                `${item.id}.png`;
            default:
              return "";
          }
        default:
          return "";
      }
    },
    group_opts(list) {
      return list.slice(list.indexOf(this.group) + 1, list.length);
    },
    // Purpose: defines img url or icon class name
    // Input: mounted data to render and the original item
    define_icon_img(item) {
      let icon = ` ${this.db.icon.item}`;

      // highest level needs own id
      if (this.depth === 0) {
        icon += item.id;
      }
      // other levels need highest level id
      else if (this.db.group_opts[0]) {
        icon += item[this.db.group_opts[0]].id;
      }
      // universities
      else if (item.school_type) {
        icon += item.school_type.toLowerCase();
      }

      return icon;
    },
    define_color(item, colors) {
      // highest level needs own id
      if (this.depth === 0) {
        return colors[item.id];
      }
      // other levels need highest level id
      else if (this.db.group_opts[0]) {
        return colors[item[this.db.group_opts[0]].id];
      }
      // universities
      else if (item.school_type) {
        return colors[item.school_type];
      }
    },
    // Purpose: formats item to be rendered
    // Input: the original item and the current index in list of items
    // Output: mounted item with all data
    mount_item(item, index) {
      const mountedItem = {
        id: item.id,
        name: item.name_pt,
        url: `/${this.db.code}/${item.id}`,
        id_description: this.db.id_description,
        extra_info: this.db.extra_info_label,
        extra_info_content: item.extra_info_content,
        filter_options: this.group_opts(this.db.group_opts),
        color: this.define_color(item, this.db.colors),
      };
      if (this.db.img_path && this.db.img_path[this.group]) {
        mountedItem.img = this.img_path(item);
      } else {
        mountedItem.icon = this.define_icon_img(item);
      }

      // alternating column colours
      if (index % 2 === 0) {
        mountedItem.bg_light_grey = "bg-near-white";
      }
      return mountedItem;
    },
    // Purpose: updates visible items
    update_visible_items() {
      const max = this.max_visible_items;
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
      if (order === "name") {
        return this.compareName;
      }
      return this.compareExtraInfo;
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
        .filter(item =>
          new RegExp(this.search.toLowerCase())
            .test(this.t_(item, "name").toLowerCase()))
        .sort(this.get_compare_function(this.order))
        .slice(0, this.max_visible_items);
    },
    filter_by_group(search, group) {
      this.visible_items = this.items[this.depth]
        .filter(item =>
          new RegExp(search.toLowerCase())
            .test(item[group].name_pt.toLowerCase()))
        .sort(this.get_compare_function(this.order))
        .slice(0, this.max_visible_items);
    },
    btn_format(order, option, index, order_opts) {
      const clickable = "pointer grow";
      let classes = order === option ? "bg-moon-gray" : clickable;
      classes += index === order_opts.length - 1 ? " br--right" : " br--left";
      classes += index !== 0 ? " br--right" : "";
      return classes;
    },
    select_group(item, group) {
      const parentGroup = this.group;
      this.set_depth(group);
      this.filter_group.group = parentGroup;
      this.filter_group.search = this.t_(item, "name");
      this.filter_by_group(this.t_(item, "name"), parentGroup);
      this.group = group;
    },
    // Purpose: requests parent component to hide modal
    close() {
      this.$emit("close");
    },
    // Purpose: increases the number of showed items when
    // the scroll end is reached
    infinity_scroll() {
      const div = document.getElementById("selectable-item-list");
      const endScroll = (div.scrollTop + div.offsetHeight) === div.scrollHeight;
      if (endScroll) {
        this.max_visible_items += this.max_visible_items;
        if (this.filter_group.search) {
          const filter = Object.values(this.filter_group);
          this.filter_by_group(filter[1], filter[0]);
        } else if (this.search) {
          this.filter_list();
        } else {
          this.update_visible_items();
        }
      }
    },
    reset_scroll_bar() {
      const itemDiv = document.getElementById("selectable-item-list");
      itemDiv.scrollTop = 0;
    },
  },
};
</script>

<template>
  <div
    v-if="db"
    class="fixed z-9999 top-0 left-0 bottom-0 right-0 w-100 h-100
           dt t-bg-black-50"
    @click="close()">
    <div class="dtc v-mid">
      <div
        class="br3 pb1 t-bg-white relative mh3 mh5-ns vh-75-ns vh-100
               overflow-hidden"
        @click.stop>
        <!-- Header -->
        <div class="t-bg-green br--top br2 flex flex-row flex-nowrap">
          <h4
            id="modal-header-title"
            class="f2 ma0 pa4 white capitalize">{{ $t(db.name) }}</h4>
          <a
            id="close-x"
            class="f2 white ml-auto pr4 pt3 mt2 fw7"
            @click="close()">&times;
          </a>
        </div>
        <SelectedFilter
          v-if="filter_item"
          :item="mount_item(filter_item, 0, filter_item_depth)"
          @remove-filter="clear_filter();"/>
        <div
          class="ph4 h-75 relative">
          <!-- Filters and aggregations -->
          <div
            v-if="!loading && !loading_depths"
            class="w-100 pt2 clearfix" >
            <div
              v-if="db.group_opts.length"
              class="fl w-100 w-auto-l pb2">
              <h5 class="tl mb0 capitalize">{{ $t("message.group_by") }}</h5>
              <div
                v-for="(option,index) in db.group_opts"
                :key="option"
                :class="btn_format(group, option, index, db.group_opts)"
                class="tc mv2 mv3-ns pv2 ph3 ba b--black-10
                       fl br2 ttc"
                @click="group_data(option);">{{ $t(db.group_labels[index]) }}
              </div>
            </div>
            <div class="fr w-100 w-auto-l pb2">
              <h5 class="tl mb0 capitalize">{{ $t("message.sort_by") }}</h5>
              <div
                v-for="(option,index) in db.order_opts"
                :key="option"
                :class="btn_format(order, option, index, db.order_opts)"
                class="tc mv2 mv3-ns pv2 ph3 ba b--black-10 fl
                       br2 ttc"
                @click="sort_data(option);">{{ $t(db.order_labels[index]) }}
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
              :placeholder="$t('message.search')"
              class="input-reset ba b--black-10 ph3 pv2 mb2 db w-100 br3
                     lh-copy"
              type="text"
              aria-describedby="name-desc"
              @keyup="update_search();">
          </form>
          <Loader v-if="loading"/>
          <!-- Item list -->
          <div
            v-if="!loading"
            id="selectable-item-list"
            class="h-75 w-100 overflow-y-auto"
            @scroll="infinity_scroll();">
            <SelectableItem
              v-for="(item, index) in visible_items"
              :item="mount_item(item, index)"
              :key="item.id"
              @select-filter="function (fil) { select_group(item, fil) }"/>
          </div> <!-- Item list ends -->
          <div
            v-if="!loading && db.source"
            class="mt4 tc f5 capitalize">
            <p>{{ $t("message.source") }}: {{ db.source.database }}
              {{ db.source.year }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const LZUTF8 = require('lzutf8');

const configs = require("../../lib/configs.js");

export default {
  name: "Selector",
  props: ["db_name"],
  data() {
    return {
      db: [],
      confs: [],
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
      filter_item: null,
      filter_item_depth: 0,
      numeric_data: null,
      maxJsonSize: 500000,
      lang: configs.get_lang(),
    };
  },
  created() {
    this.setLang();

    if (this.db_name) {
      this.db = configs.databases[this.db_name];
      this.confs = configs.env;
      let length =  0;

      // Test if have agregations levels
      if (this.db.group_opts) {
        length = this.db.group_opts.length - 1;    
        // Sets group level to minimum
        this.group = this.db.group_opts[length];
        // Gets the second order option
        this.order = this.db.order_opts["1"];
      } else {
        this.db.group_opts = [];
      }

      this.max_depth = length;
      // Sets current depth level to minimum
      this.depth = length;

      this.readMountedDataFromLocalStorage();

      if (!this.items && this.db.extra_info.endpoint) {
        this.get_numeric_data();
      } else if (!this.items) {
        this.get_data();
      }
    } else {
      this.close();
    }
  },
  methods: {
    setLang() {
      this._i18n.locale = this.lang;
    },
    splitString(string, size) {
      var re = new RegExp('.{1,' + size + '}', 'g');
      return string.match(re);
    },
    readMountedDataFromLocalStorage() {
      if (this.checkLocalStorageSupport()) {
        this.items = this.retrieveDataFromLocalStorage(this.db.code);
        
        if (this.items) {
          this.sort_list_by_property(this.order);
          this.update_visible_items();
          this.loading = false;
          this.loading_depths = false;
        }
      }
    },
    checkLocalStorageSupport() {
      if (typeof(Storage) !== "undefined") {
        return true;
      } else {
        return false;
      }  
    },
    retrieveDataFromLocalStorage(key) {
      let keyName = "modal_data_" + key;

      try {
        let data = "";
        let part = "";
        let comp = "";

        for (let i = 0; comp != null; i++) {
          comp = localStorage.getItem(`${keyName}_${i}`);
          
          if (comp) {
            comp = new Uint8Array(JSON.parse("[" + comp + "]"));
            part = LZUTF8.decompress(comp);

            data += part;
          }
        }

        return JSON.parse(data);
      } catch(e) {
        let result = '';

        for (let i = 0; `${keyName}_${i}` in localStorage; i++) {
          localStorage.removeItem(`${keyName}_${i}`);
        }
        return "";
      }
    },
    saveDataToLocalStorage(key, data) {
      if (this.checkLocalStorageSupport()) {
        let parsedJson = JSON.stringify(data);
        let nParts = this.splitString(parsedJson, this.maxJsonSize);
        let keyName = "";
        let comp = "";

        for (let i = 0; i < nParts.length; i++) {
          keyName = `modal_data_${key}_${i}`;
          comp = LZUTF8.compress(nParts[i]);
          localStorage.setItem(keyName, comp);
        }
      }
    },
    // Purpose: gets item property according to the current language
    // Input: item and property name
    // Output: property value
    t_(item, prop) {
      return item[`${prop}_${this.lang}`];
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
    get_position(list, id) {
      for (let i = 0; i < list.length; i += 1) {
        if (list[i].id === id) {
          return i;
        }
      }
    },
    sum_extra_info(list, id, value) {
      for (let i = 0; i < list.length; i += 1) {
        if (list[i].id === id) {
          return parseFloat(list[i].extra_info_content) + parseFloat(value);
        }
      }
      return 0;
    },
    // Purpose: gets data from API and calls function to read data
    async get_data() {
      const ep = this.db.endpoint;
      axios.get(`${this.confs.api_url}metadata/${ep}`)
        .then(response => (this.read_data(response.data)));
    },
    async get_numeric_data() {
      const ep = `${this.confs.api_url}${this.db.extra_info.endpoint}`;
      axios.get(ep)
        .then(response => (this.read_numeric_data(response.data)))
        .catch(response => this.get_data());
    },
    // Purpose: splits data from different levels when data
    // comes from the same endpoint with diverse depths
    async read_depths() {
      const minorData = this.items[this.max_depth];
      let info = 0;
      let pos = 0;

      for (let j = 0; j < this.max_depth; j += 1) {
        for (let i = 0; i < minorData.length; i += 1) {
          const item = minorData[i][this.db.group_opts[j]];
          info = minorData[i].extra_info_content;
          info = Number.isNaN(info) || info === null ? 0 : info;

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
            item.extra_info_content = info;
            this.items[j].push(item);
          } else {
            pos = this.get_position(this.items[j], item.id);
            this.items[j][pos].extra_info_content =
              this.sum_extra_info(this.items[j], item.id, info);
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
      const depth = this.depth;

      for (let i = 0; i <= this.max_depth; i += 1) {
        this.items[i] = [];
      }

      this.items[depth] = Object.values(data);

      if (["occupation", "product", "trade_partner", "hedu_course",
        "basic_course"].includes(this.db.code)) {
             this.items[depth] = this.items[depth].filter(item =>
               !this.db.hidden_ids.includes(String(item[this.db.group_opts[0]]
               .id)) && !this.db.hidden_ids.includes(String(item.id)));
      } else if (this.db.code === "university") {
        this.items[depth] = this.items[depth]
          .filter(item =>
            !this.db.hidden_ids.includes((item.school_type).toLowerCase()));
      }

      if (this.group) {
        this.items[depth] =
          this.remove_incomplete(this.items[depth], this.db.group_opts);
      }

      if(this.numeric_data) {
        this.set_data_to_metadata();
      }
      this.read_depths();
      this.sort_list_by_property(this.order);
      this.update_visible_items();
      this.saveDataToLocalStorage(this.db.code, this.items);
      this.loading = false;
    },
    get_prop_position(prop, header) {
      for (let i = 0; i < header.length; i += 1) {
        if (prop === header[i]) {
          return i;
        }
      }
      return -1;
    },
    set_data_to_metadata() {
      const context = this;
      let data = null;
      const depth = this.depth;

      for (let i = 0; i < this.items[depth].length; i += 1) {
        data = this.numeric_data.find(function (obj) {
            return obj.id === context.items[depth][i].id;
        });
        this.items[depth][i].extra_info_content = data ? data.extra_info : null;
      }
    },
    read_numeric_data(response_data) {
      const formatted_data = [];
      const data = Object.values(response_data.data);
      const header = Object.values(response_data.headers);
      const info = {};
      const id = this.db.extra_info.id;
      const data_value = this.db.extra_info.data_value;

      for (const item in data) {
        if (data[item] !== null) {
          info.id = data[item][this.get_prop_position(id, header)];
          info.extra_info =
            data[item][this.get_prop_position(data_value, header)];
        }
        formatted_data[item] = Object.assign({}, info);
      }

      this.numeric_data = formatted_data;
      this.get_data();
    },
    // Purpose: gets url path for items with image
    // Input: item
    // Output: url
    img_path(item, item_depth) {
      const depth = item_depth !== undefined ? item_depth : this.depth;

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
      if (list) {
        return list.slice(list.indexOf(this.group) + 1, list.length);
      }

      return "";
    },
    // Purpose: defines img url or icon class name
    // Input: mounted data to render and the original item
    define_icon_img(item, item_depth) {
      const depth = item_depth !== undefined ? item_depth : this.depth;
      let icon = ` ${this.db.icon.item}`;

      // universities
      if (item.school_type) {
        icon += item.school_type.toLowerCase();
      }
      // highest level needs own id
      else if (depth === 0) {
        icon += item.id;
      }
      // other levels need highest level id
      else if (this.db.group_opts[0]) {
        icon += item[this.db.group_opts[0]].id;
      }
      return icon;
    },
    define_color(item, colors, item_depth) {
      const depth = item_depth !== undefined ? item_depth : this.depth;
      // universities
      if (item.school_type) {
        return colors[item.school_type];
      }
      // highest level needs own id
      else if (depth === 0) {
        return colors[item.id];
      }
      // other levels need highest level id
      else if (this.db.group_opts[0]) {
        return colors[item[this.db.group_opts[0]].id];
      }
    },
    // Purpose: formats item to be rendered
    // Input: the original item and the current index in list of items
    // Output: mounted item with all data
    mount_item(item, index, depth) {
      const mountedItem = {
        id: item.id,
        name: this.t_(item, "name"),
        url: `/${this.db.code}/${item.id}`,
        id_description: this.db.id_description,
        extra_info: this.db.extra_info.label,
        extra_info_content: item.extra_info_content,
        filter_options: this.group_opts(this.db.group_opts),
        color: this.define_color(item, this.db.colors, depth),
      };

      if (depth === 0 &&
      (["location", "trade_partner"].includes(this.db.code))) {
        mountedItem.icon = this.define_icon_img(item, depth);
      }
      else if (this.db.img_path && this.db.img_path[this.group]) {
        mountedItem.img = this.img_path(item, depth);
      } else {
        mountedItem.icon = this.define_icon_img(item, depth);
      }

      if (["product", "trade_partner"].includes(this.db.code)) {
        mountedItem.prefix = "USD ";
      }
      else {
        mountedItem.prefix = "";
      }

      // alternating column colours
      if (index % 2 === 0) {
        mountedItem.bg_light_grey = "t-bg-near-white";
      }
      return mountedItem;
    },
    // Purpose: updates visible items
    update_visible_items() {
      const max = this.max_visible_items;
      let depth = this.depth != -1 ? this.depth : 0;

      this.visible_items = this.items[depth].slice(0, max);
    },
    sort_list_by_property(order) {
      let depth = this.depth != -1 ? this.depth : 0;

      this.items[depth].sort(this.get_compare_function(order));

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
      this.filter_item = null;
      this.filter_item_depth = 0;
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
      let depth = this.depth != -1 ? this.depth : 0;

      if (this.filter_group.group) {
        this.visible_items = this.items[depth]
          .filter(item =>
            new RegExp(this.search.toLowerCase())
              .test(this.t_(item, "name").toLowerCase()) ||
            new RegExp(this.search).test(item.id))
          .filter(item =>
            new RegExp(this.filter_group.search.toLowerCase())
              .test(item[this.filter_group.group].name_pt.toLowerCase()))
          .sort(this.get_compare_function(this.order))
          .slice(0, this.max_visible_items);
      } else {
        this.visible_items = this.items[depth]
          .filter(item =>
            new RegExp(this.search.toLowerCase())
              .test(this.t_(item, "name").toLowerCase())
            ||
            new RegExp(this.search)
              .test(item.id))
          .sort(this.get_compare_function(this.order))
          .slice(0, this.max_visible_items);
      }
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
      let classes = order === option ? "t-bg-moon-gray" : clickable;
      classes += index === order_opts.length - 1 ? " br--right" : " br--left";
      classes += index !== 0 ? " br--right" : "";
      return classes;
    },
    select_group(item, group) {
      this.filter_item_depth = this.depth;
      const parentGroup = this.group;
      this.set_depth(group);
      this.filter_group.group = parentGroup;
      this.filter_group.search = this.t_(item, "name");
      this.filter_by_group(this.t_(item, "name"), parentGroup);
      this.group = group;
      this.filter_item = item;
      this.reset_scroll_bar();
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
    group_data(opt) {
      this.reset_scroll_bar();
      this.clean_search();
      this.reset_group_filter();
      this.group_by_property(opt);
    },
    sort_data(opt) {
      this.reset_scroll_bar();
      this.sort_list_by_property(opt);
      this.update_visible_items();
    },
    update_search() {
      // this.reset_group_filter();
      this.filter_list();
    },
    clear_filter() {
      this.reset_group_filter();
      this.update_visible_items();
      this.reset_scroll_bar();
    },
  },
};
</script>

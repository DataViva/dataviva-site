<template>
  <div
    v-if="db"
    id="dv-selector-modal"
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
        <template v-if="!loading">
          <SelectedFilter
            v-if="filterItem"
            :item="mountItem(filterItem, 0, filterItemDepth)"
            @remove-filter="clear_filter();"
            canRemove/>
          <SelectedFilter
            v-else-if="defaultOption"
            :item="defaultOption"/>
        </template>
        <div
          class="ph4 h-75 relative">
          <!-- Filters and aggregations -->
          <div
            v-if="!loading && !loadingDepths"
            class="w-100 pt2 clearfix" >
            <div
              v-if="db.groupOpts.length"
              class="fl w-100 w-auto-l pb2">
              <h5 class="tl mb0 capitalize">{{ $t("message.group_by") }}</h5>
              <div
                v-for="(option,index) in db.groupOpts"
                :key="option"
                :class="btn_format(group, option, index, db.groupOpts)"
                class="tc mv2 mv3-ns pv2 ph3 ba b--black-10
                       fl br2 ttc"
                @click="group_data(option);">{{ $t(db.groupLabels[index]) }}
              </div>
            </div>
            <div class="fr w-100 w-auto-l pb2">
              <h5 class="tl mb0 capitalize">{{ $t("message.sort_by") }}</h5>
              <div
                v-for="(option,index) in db.orderOpts"
                :key="option"
                :class="btn_format(order, option, index, db.orderOpts)"
                class="tc mv2 mv3-ns pv2 ph3 ba b--black-10 fl
                       br2 ttc"
                @click="sort_data(option);">{{ $t(db.orderLabels[index]) }}
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
              v-for="(item, index) in visibleItems"
              :item="mountItem(item, index)"
              :key="item.id"
              @select-item="() => setLoading()"
              @select-filter="(filter) => select_group(item, filter)"/>
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

const LZUTF8 = require("lzutf8");

const configs = require("../../lib/configs.js");

export default {
  name: "Selector",
  props: {
    database: {
      type: String,
      default: "location",
    },
  },
  data() {
    return {
      db: [],
      confs: [],
      maxDepth: 0, // max aggregation level
      depth: 0, // current aggregation
      group: "", // current aggregation name
      order: "extraInfo", // current order option
      search: null, // search text
      loading: true, // stores if the modal is loading
      loadingDepths: true, // only shows controls and finishes loading levels
      maxVisibleItems: 10,
      items: null,
      visibleItems: [""],
      filterGroup: { // filters data by aggregation
        group: "",
        search: "",
      },
      filterItem: null,
      defaultOption: null,
      filterItemDepth: 0,
      numericData: null,
      maxJsonSize: 300000,
      lang: configs.getLang(),
      isInternal: false,
    };
  },
  created() {
    this.setLang();
    if (this.database) {
      this.isInternal = this.isInternalPage();
      this.db = configs.databases[this.database];
      this.confs = configs.env;
      let length = 0;

      if (this.db) {
        // Test if have agregations levels
        if (this.db.groupOpts) {
          length = this.db.groupOpts.length - 1;
          // Sets group level to minimum
          this.group = this.db.groupOpts[length];

          const { orderOpts } = this.db;
          // Gets the second order option
          this.order = orderOpts[1] ? orderOpts[1] : orderOpts[0];
        } else {
          this.db.groupOpts = [];
        }

        this.maxDepth = length;
        // Sets current depth level to minimum
        this.depth = length;

        this.readMountedDataFromLocalStorage();

        this.setDefaultOption(this.db);

        if (!this.items && this.db.extraInfo.endpoint) {
          this.getNumericData();
        } else if (!this.items) {
          this.getData();
        }
      } else {
        this.close();
      }
    } else {
      this.close();
    }
  },
  methods: {
    setLoading() {
      this.loading = true;
    },
    setLang() {
      this._i18n.locale = this.lang;
    },
    splitString(string, size) {
      const re = new RegExp(`.{1,${size}}`, "g");
      return string.match(re);
    },
    setDefaultOption({defaultOption}) {
      if (defaultOption) {
        this.defaultOption = defaultOption;
        this.defaultOption.name = this.$t(this.defaultOption.name);
        this.defaultOption.url = this.getUrl(defaultOption);
      }
    },
    readMountedDataFromLocalStorage() {
      if (this.checkLocalStorageSupport()) {
        this.items = this.retrieveDataFromLocalStorage(this.db.code);

        if (this.items) {
          this.sortListByProperty(this.order);
          this.updateVisibleItems();
          this.loading = false;
          this.loadingDepths = false;
        }
      }
    },
    checkLocalStorageSupport() {
      if (typeof (Storage) !== "undefined") {
        return true;
      }
      return false;
    },
    retrieveDataFromLocalStorage(key) {
      const keyName = `modal_data_${key}`;

      try {
        let data = "";
        let part = "";
        let comp = "";

        for (let i = 0; comp != null; i += 1) {
          comp = localStorage.getItem(`${keyName}_${i}`);

          if (comp) {
            comp = new Uint8Array(JSON.parse(`[${comp}]`));
            part = LZUTF8.decompress(comp);

            data += part;
          }
        }

        return JSON.parse(data);
      } catch (e) {
        for (let i = 0; `${keyName}_${i}` in localStorage; i += 1) {
          localStorage.removeItem(`${keyName}_${i}`);
        }
        return "";
      }
    },
    removeDataFromLocalStorage(key, nParts) {
      let keyName = "";

      for (let i = 0; i < nParts; i += 1) {
        try {
          keyName = `modal_data_${key}_${i}`;
          localStorage.setItem(keyName);
        } catch (error) {
          return;
        }
      }
    },
    saveDataToLocalStorage(key, data) {
      if (this.checkLocalStorageSupport()) {
        const parsedJson = JSON.stringify(data);
        const nParts = this.splitString(parsedJson, this.maxJsonSize);
        let keyName = "";
        let comp = "";

        for (let i = 0; i < nParts.length; i += 1) {
          try {
            keyName = `modal_data_${key}_${i}`;
            comp = LZUTF8.compress(nParts[i]);
            localStorage.setItem(keyName, comp);
          } catch (error) {
            this.removeDataFromLocalStorage(key, i);
            console.log("Error: cannot save to localstorage.");
            return;
          }
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
      if (a.extra_info_content > b.extra_info_content) {
        return -1;
      }
      if (a.extra_info_content < b.extra_info_content) {
        return 1;
      }
      return 0;
    },
    // Purpose: checks if item id is present in list
    // Input: id and list
    checkExist(list, id) {
      for (let i = 0; i < list.length; i += 1) {
        if (list[i].id === id) {
          return true;
        }
      }
      return false;
    },
    getPosition(list, id) {
      for (let i = 0; i < list.length; i += 1) {
        if (list[i].id === id) {
          return i;
        }
      }

      return -1;
    },
    sumExtraInfo(list, id, value) {
      for (let i = 0; i < list.length; i += 1) {
        if (list[i].id === id) {
          return parseFloat(list[i].extra_info_content) + parseFloat(value);
        }
      }
      return 0;
    },
    // Purpose: gets data from API and calls function to read data
    async getData() {
      const ep = this.db.endpoint;
      axios.get(`${this.confs.apiUrl}metadata/${ep}`)
        .then(response => (this.readData(response.data)));
    },
    async getNumericData() {
      const ep = `${this.confs.apiUrl}${this.db.extraInfo.endpoint}`;
      axios.get(ep)
        .then(response => (this.readNumericData(response.data)))
        .catch(() => this.getData());
    },
    // Purpose: splits data from different levels when data
    // comes from the same endpoint with diverse depths
    async readDepths() {
      const minorData = this.items[this.maxDepth];
      let info = 0;
      let pos = 0;

      for (let j = 0; j < this.maxDepth; j += 1) {
        for (let i = 0; i < minorData.length; i += 1) {
          const item = minorData[i][this.db.groupOpts[j]];
          info = minorData[i].extra_info_content;
          info = Number.isNaN(info) || info === null ? 0 : info;

          // Adds information about higher levels
          for (let h = 0; h < j; h += 1) {
            const prop = minorData[i][this.db.groupOpts[h]];

            if (prop) {
              const names = {
                id: prop.id,
                name_pt: prop.name_pt,
                name_en: prop.name_en,
              };
              item[this.db.groupOpts[h]] = names;
            }
          }

          if (item && !this.checkExist(this.items[j], item.id)) {
            item.extra_info_content = info;
            this.items[j].push(item);
          } else {
            pos = this.getPosition(this.items[j], item.id);
            this.items[j][pos].extra_info_content =
              this.sumExtraInfo(this.items[j], item.id, info);
          }
        }
      }

      this.loadingDepths = false;
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
    removeIncomplete(array, group) {
      return array.filter(item => this.have_all_groups(item, group));
    },
    // Purpose: reads response and creates dataset
    // Input: response data
    readData(data) {
      this.items = [];
      const { depth } = this;
      const dbs = [
        "occupation", "product", "trade_partner", "major", "basic_course",
      ];

      for (let i = 0; i <= this.maxDepth; i += 1) {
        this.items[i] = [];
      }

      this.items[depth] = Object.values(data);

      if (dbs.includes(this.db.code)) {
        this.items[depth] = this.items[depth].filter(item =>
          !this.db.hiddenIds.includes(String(item[this.db.groupOpts[0]].id)) &&
          !this.db.hiddenIds.includes(String(item.id)));
      } else if (this.db.code === "university") {
        this.items[depth] = this.items[depth]
          .filter(item =>
            !this.db.hiddenIds.includes((item.school_type).toLowerCase()));
      }

      if (this.group) {
        this.items[depth] =
          this.removeIncomplete(this.items[depth], this.db.groupOpts);
      }

      if (this.numericData) {
        this.setDataToMetadata();
      }

      this.readDepths();
      this.sortListByProperty(this.order);
      this.updateVisibleItems();
      this.saveDataToLocalStorage(this.db.code, this.items);
      this.loading = false;
    },
    getPropPosition(prop, header) {
      for (let i = 0; i < header.length; i += 1) {
        if (prop === header[i]) {
          return i;
        }
      }
      return -1;
    },
    setDataToMetadata() {
      const context = this;
      let data = null;
      const { depth } = this;

      for (let i = 0; i < this.items[depth].length; i += 1) {
        data = this.numericData.find(o => o.id === context.items[depth][i].id);
        this.items[depth][i].extra_info_content = data ? data.extraInfo : null;
      }
    },
    readNumericData(responseData) {
      const formattedData = [];
      const data = Object.values(responseData.data);
      const header = Object.values(responseData.headers);
      const info = {};
      const { id, dataValue } = this.db.extraInfo;

      for (const item in Object.keys(data)) {
        if (item) {
          if (data[item] !== null) {
            info.id = data[item][this.getPropPosition(id, header)];
            info.extraInfo =
              data[item][this.getPropPosition(dataValue, header)];
          }
          formattedData[item] = Object.assign({}, info);
        }
      }

      this.numericData = formattedData;
      this.getData();
    },
    // Purpose: gets url path for items with image
    // Input: item
    // Output: url
    imgPath(item, itemDepth) {
      const depth = itemDepth !== undefined ? itemDepth : this.depth;

      /* eslint-disable */
      switch (this.db.code) {
        case "location":
          switch (depth) {
            case 1:
            case 2:
            case 3:
            case 4:
              return `${this.confs.s3Host}${this.db.imgPath[this.group]}` +
            `${item.id.substring(0, 2)}.png`;
            default:
              return "";
          }

        case "trade_partner":
          switch (depth) {
            case 0:
            case 1:
              return `${this.confs.s3Host}${this.db.imgPath[this.group]}` +
            `${item.id}.png`;
            default:
              return "";
          }
        default:
          return "";
      }
      /* eslint-enable */
    },
    groupOpts(list) {
      if (list) {
        return list.slice(list.indexOf(this.group) + 1, list.length);
      }

      return "";
    },
    // Purpose: defines img url or icon class name
    // Input: mounted data to render and the original item
    defineIconImg(item, itemDepth) {
      const depth = itemDepth !== undefined ? itemDepth : this.depth;
      let icon = ` ${this.db.icon.item}`;

      // universities
      if (item.school_type) {
        icon += item.school_type.toLowerCase();
      } else if (depth === 0) { // highest level needs own id
        // locations needs the old code (different from IBGE)
        if (this.db.code === "location") {
          icon += item.old_id;
        } else {
          icon += item.id;
        }
      } else if (this.db.groupOpts[0]) { // other levels need highest level id
        icon += item[this.db.groupOpts[0]].id;
      }
      return icon;
    },
    defineColor(item, colors, itemDepth) {
      const depth = itemDepth !== undefined ? itemDepth : this.depth;
      // universities
      if (item.school_type) {
        return colors[item.school_type];
      } else if (depth === 0) { // highest level needs own id
        return colors[item.id];
      } else if (this.db.groupOpts[0]) { // other levels need highest level id
        return colors[item[this.db.groupOpts[0]].id];
      }

      return null;
    },
    locationPath(item) {
      return `/${this.lang}/${this.db.code}/${item.old_id}`;
    },
    industryPath(item, search, depth) {
      /* eslint-disable */
      switch (depth) {
        case 1:
        case 2:
          if (item.industry_section) {
            return `/${this.db.code}/${item.industry_section.id}${item.id}${search}`;
          }
        default:
          return this.defaultPath(item, search);
      }
      /* eslint-enable */
    },
    productPath(item, search, depth) {
      /* eslint-disable */
      switch (depth) {
        case 1:
          if (item.product_section) {
            return `/${this.db.code}/${item.product_section.id}${item.id}${search}`;
          }
          break;
        default:
          return this.defaultPath(item, search);
      }
      /* eslint-enable */
    },
    tradepartnerPath(item, search, depth) {
      /* eslint-disable */
      switch (depth) {
        case 1:
          return `/${this.db.code}/${item.abbrv}${search}`;
        default:
          return this.defaultPath(item, search);
      }
      /* eslint-enable */
    },
    defaultPath(item, search) {
      return `/${this.db.code}/${item.id}${search}`;
    },
    hasPath() {
      const path = window.location.pathname;
      return (path !== "" && path !== undefined);
    },
    getDBsCodes() {
      return Object.keys(configs.databases);
    },
    isInternalPage() {
      const path = window.location.pathname;
      const dbs = this.getDBsCodes();

      for (const db in dbs) {
        if (path.indexOf(dbs[db]) !== -1) {
          return true;
        }
      }

      return false;
    },
    isLocation() {
      const path = window.location.pathname;
      return (path.indexOf("location") !== -1);
    },
    hasQueryString() {
      const { search } = window.location;
      return (search !== "" && search !== undefined);
    },
    getQueryString() {
      const { search } = window.location;
      return search;
    },
    pathWithlocationQuery(item) {
      const path = window.location.pathname;
      const search = `?bra_id=${item.old_id}`;
      return `${path}${search}`;
    },
    getUrl(item, selectedDepth) {
      let search = "";
      const depth = selectedDepth || this.depth;

      if (this.hasPath() && this.hasQueryString()) {
        search = this.getQueryString();
      }

      /* eslint-disable */
      switch (this.db.code) {
        case "location":
          if (this.isInternal && !this.isLocation()) {
            return this.pathWithlocationQuery(item);
          }
          return this.locationPath(item);
        case "industry":
          return this.industryPath(item, search, depth);
        case "product":
          return this.productPath(item, search, depth);
        case "trade_partner":
          return this.tradepartnerPath(item, search, depth);
        default:
          return this.defaultPath(item, search);
      }
      /* eslint-enable */
    },
    formatNumber(num) {
      if (this.lang === "pt" && num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
      } else if (num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      }
      return "";
    },
    // Purpose: formats item to be rendered
    // Input: the original item and the current index in list of items
    // Output: mounted item with all data
    mountItem(item, index, depth) {
      const mountedItem = {
        id: item.id,
        name: this.t_(item, "name"),
        url: this.getUrl(item),
        id_description: this.db.idDescription,
        extra_info: this.db.extraInfo.label,
        extra_info_content: this.formatNumber(item.extra_info_content),
        filter_options: this.groupOpts(this.db.groupOpts),
        color: this.defineColor(item, this.db.colors, depth),
      };

      if (depth === 0 &&
      (["location", "trade_partner"].includes(this.db.code))) {
        mountedItem.icon = this.defineIconImg(item, depth);
      } else if (this.db.imgPath && this.db.imgPath[this.group]) {
        mountedItem.img = this.imgPath(item, depth);
      } else {
        mountedItem.icon = this.defineIconImg(item, depth);
      }

      if (["product", "trade_partner"].includes(this.db.code)) {
        mountedItem.prefix = "USD ";
      } else {
        mountedItem.prefix = "";
      }

      // alternating column colours
      if (index % 2 === 0) {
        mountedItem.bg_light_grey = "t-bg-near-white";
      }
      return mountedItem;
    },
    // Purpose: updates visible items
    updateVisibleItems() {
      const max = this.maxVisibleItems;
      const depth = this.depth !== -1 ? this.depth : 0;

      this.visibleItems = this.items[depth].slice(0, max);
    },
    sortListByProperty(order) {
      const depth = this.depth !== -1 ? this.depth : 0;

      this.items[depth].sort(this.getCompareFunction(order));

      this.order = order;
    },
    // Purpose: gets corresponding depth of a group name
    // Input: group
    // Output: depth level
    correspondingDepth(group) {
      return this.db.groupOpts.indexOf(group);
    },
    setDepth(group) {
      this.depth = this.correspondingDepth(group);
    },
    getCompareFunction(order) {
      if (order === "name") {
        return this.compareName;
      }
      return this.compareExtraInfo;
    },
    reset_group_filter() {
      this.filterGroup = {};
      this.filterItem = null;
      this.filterItemDepth = 0;
    },
    // Purpose: cleans the search text field
    clean_search() {
      this.search = null;
    },
    // Purpose: shows items in group depth level
    // Input: group depth name
    group_by_property(group) {
      this.group = group;
      this.setDepth(group);

      this.sortListByProperty(this.order);
      this.updateVisibleItems();
    },
    filter_list() {
      const depth = this.depth !== -1 ? this.depth : 0;

      if (this.filterGroup.group) {
        this.visibleItems = this.items[depth]
          .filter(item =>
            new RegExp(this.search.toLowerCase())
              .test(this.t_(item, "name").toLowerCase()) ||
            new RegExp(this.search).test(item.id))
          .filter(item =>
            new RegExp(this.filterGroup.search.toLowerCase())
              .test((this.t_(item[this.filterGroup.group]), "name").toLowerCase()))
          .sort(this.getCompareFunction(this.order))
          .slice(0, this.maxVisibleItems);
      } else {
        this.visibleItems = this.items[depth]
          .filter(item =>
            new RegExp(this.search.toLowerCase())
              .test(this.t_(item, "name").toLowerCase())
            ||
            new RegExp(this.search)
              .test(item.id))
          .sort(this.getCompareFunction(this.order))
          .slice(0, this.maxVisibleItems);
      }
    },
    filter_by_group(search, group) {
      this.visibleItems = this.items[this.depth]
        .filter(item =>
          search.toLowerCase() === this.t_(item[group], "name").toLowerCase())
        .sort(this.getCompareFunction(this.order))
        .slice(0, this.maxVisibleItems);
    },
    btn_format(order, option, index, orderOpts) {
      const clickable = "pointer grow";
      let classes = order === option ? "t-bg-moon-gray" : clickable;
      classes += index === orderOpts.length - 1 ? " br--right" : " br--left";
      classes += index !== 0 ? " br--right" : "";
      return classes;
    },
    select_group(item, group) {
      this.filterItemDepth = this.depth;
      const parentGroup = this.group;
      this.filterGroup.group = parentGroup;
      this.filterGroup.search = this.t_(item, "name");
      this.setDepth(group);
      this.filter_by_group(this.t_(item, "name"), parentGroup);
      this.group = group;
      item.url = this.getUrl(item, this.filterItemDepth);
      this.filterItem = item;
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
        this.maxVisibleItems += this.maxVisibleItems;
        if (this.filterGroup.search) {
          const filter = Object.values(this.filterGroup);
          this.filter_by_group(filter[1], filter[0]);
        } else if (this.search) {
          this.filter_list();
        } else {
          this.updateVisibleItems();
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
      this.sortListByProperty(opt);
      this.updateVisibleItems();
    },
    update_search() {
      // this.reset_group_filter();
      this.filter_list();
    },
    clear_filter() {
      this.reset_group_filter();
      this.updateVisibleItems();
      this.reset_scroll_bar();
    },
  },
};
</script>


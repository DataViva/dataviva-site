<template>
  <div class="row">
    <div v-for="database in databases" class="col-lg-3 col-xs-6">
      <a :key="database.name"
         :data-content="$t(database.tooltipText)"
         class="no-underline burgundy t-bg-transparent hover-bg-burgundy mh2 h4 w5 mh2 mb4 pt1 hover-white"
         data-toggle="popover"
         data-placement="top"
         @click="selectDataBase(database.code);">
        <div class="tc">
          <div class="f1 mt3 mb2">
            <i :class="database.icon.db" />
          </div>
          <div>
            <p class="f3 capitalize">{{ $t(database.name) }}</p>
          </div>
        </div>
      </a>
    </div>
    <transition name="fade">
      <selector v-if="show" :database="database" @close="closeModal()"/>
    </transition>
  </div>
</template>


<script>
import "../../assets/css/*.css";

const configs = require("../../lib/configs.js");

export default {
  name: "DataBaseSelector",
  data() {
    return {
      show: false,
      databases: configs.databases,
      database: "",
      lang: configs.getLang(),
    };
  },
  created() {
    this.setLang();
  },
  methods: {
    selectDataBase(database) {
      this.database = database;
      this.show = true;
    },
    closeModal() {
      this.show = false;
    },
    setLang() {
      this._i18n.locale = this.lang;
    },
  },
};
</script>

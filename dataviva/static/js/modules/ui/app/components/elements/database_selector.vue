<template>
  <div
    class="flex flex-row flex-wrap justify-center pv3">
    <a
      v-for="database in databases"
      :key="database.name"
      :data-content="database.tooltip_text"
      class="no-underline burgundy bg-transparent hover-bg-burgundy mh2 h4
             w5 mh2 mb4 pt1"
      data-toggle="popover"
      data-placement="top"
      @click="selectDataBase(database);">
      <div class="tc">
        <div
          class="f1 mt3 mb2">
          <i
            :class="database.icon.db" />
        </div>
        <div>
          <span
            class="f3">
            {{ database.name }}
          </span>
        </div>
      </div>
    </a>
    <transition name="fade">
      <selector
        v-if="show"
        :db="database"
        :confs="confs"
        @close="closeModal"/>
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
      confs: configs.env,
      databases: configs.databases,
    };
  },
  methods: {
    selectDataBase(database) {
      this.database = database;
      this.show = true;
    },
    closeModal() {
      this.show = false;
    },
  },
};
</script>

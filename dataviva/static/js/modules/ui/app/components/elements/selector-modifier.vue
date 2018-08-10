<template>
  <span class="cursor_default">
    <template v-if="text">
      <span
        @click="showModal = true"
        class="pointer">
        {{text}}
      </span>
    </template>
    
    <selector
      v-if="showModal"
      v-bind:db="database"
      v-bind:confs="confs"
      v-bind:filter="filter"
      v-on:close="closeModal()">
    </selector>
  </span>
</template>

<script>
import "../../assets/css/*.css"
var configs = require("../../lib/configs.js");

export default {
  name: "SelectorModifier",
  props: ["db", "text", "filter"],
  data() {
    return {
      showModal: true,
      confs: configs.env,
      databases: configs.databases
    }
  },
  created: function () {
    this.database = this.databases[this.db];
  },
  methods: {
    closeModal() {
      this.showModal = false;
    }
  },
};
</script>

<style type="text/css" scoped>
  .cursor_default {
    cursor: default;
  }
</style>
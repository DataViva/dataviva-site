<template>
  <span class="cursor_default">
    <template v-if="text">
      <span
        class="pointer"
        @click="showModal = true">
        {{ text }}
      </span>
    </template>

    <selector
      v-if="showModal"
      :db_name="database"
      :filter="filter"
      @close="closeModal()"/>
  </span>
</template>

<script>
import "../../assets/css/*.css";

const configs = require("../../lib/configs.js");

export default {
  name: "SelectorModifier",
  props: {
    db: {
      type: Object,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
    filter: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showModal: true,
      confs: configs.env,
    };
  },
  created() {
    this.database = this.db;
  },
  methods: {
    closeModal() {
      this.showModal = false;
    },
  },
};
</script>

<style type="text/css" scoped>
  .cursor_default {
    cursor: default;
  }
</style>

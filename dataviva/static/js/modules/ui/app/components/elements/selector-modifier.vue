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
      :database="database"
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
      type: String,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showModal: true,
      confs: configs.env,
      lang: configs.getLang(),
    };
  },
  created() {
    this.database = this.db;
    this.setLang();
  },
  mounted() {
    const modal = document.getElementById("dv-selector-modal");
    const body = document.getElementsByTagName("body")[0];
    if (modal) {
      body.appendChild(modal);
    }
  },
  methods: {
    closeModal() {
      this.showModal = false;
    },
    setLang() {
      this._i18n.locale = this.lang;
    },
  },
};
</script>

<style type="text/css" scoped>
  .cursor_default {
    cursor: default;
  }
</style>

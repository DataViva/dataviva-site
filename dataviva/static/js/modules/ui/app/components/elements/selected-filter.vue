<template>
  <div
    class="t-bg-light-gray flex flex-row flex-nowrap pt3 pb3">
    <div class="tc">
      <template v-if="item.img">
        <div class="w3 w4-ns">
          <img
            :src="item.img"
            class="search-icon-size ml0-ns ml2">
        </div>
      </template>
      <template v-else-if="item.icon">
        <div class="w3 w4-ns">
          <i
            :style="'color: ' + item.color"
            :class="'f1-ns f2 lh-copy' + item.icon"/>
        </div>
      </template>
    </div>
    <div class="ph3 ph0-ns">
      <h3
        id="item-title"
        :style="'color: ' + item.color"
        class="mv0 fw4 lh-title measure-narrow measure-wide-ns">
        {{ item.name }}</h3>
      <div
        v-if="canRemove"
        class="burgundy">
        <span
          class="f3 fw4 pr4 pt3 mt2 pointer"
          @click="$emit('remove-filter')">&times;
          {{ $t("message.remove_filter") }}
        </span>
      </div>
    </div>
    <div
      class="ml-auto mr2-ns mr0">
      <a
        :href="item.url"
        class="select-button f4 ba burgundy br2 ph3 pv2 mr3 dib mt2
               hover-bg-burgundy capitalize">{{ $t("message.select") }}
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "SelectedFilter",
  props: {
    item: {
      type: Object,
      default() {
        return null;
      },
    },
    canRemove: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
    };
  },
  methods: {
    removeFilter() {
    },
  },
};
</script>

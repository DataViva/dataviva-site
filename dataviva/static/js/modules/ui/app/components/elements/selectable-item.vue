<template>
  <div
    :class="item.bg_light_grey"
    class="flex flex-row flex-nowrap pt3 pb3">

    <div class="tc">
      <template v-if="item.img">
        <div class="w3 w4-ns">
          <img
            :src="item.img"
            class="search-icon-size ml0-ns ml2">
        </div>
      </template>
      <template v-else-if="item.icon">
        <div class="pt2 w3 w4-ns">
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
      <small
        class="medium-gray f5">
        {{ $t(item.id_description) }}: {{ item.id }}
      </small>
      <template v-if="item.extra_info_content && item.extra_info">
        <br>
        <p
          class="medium-gray f5 capitalize dib mb0">
          {{ $t(item.extra_info) }}: {{ item.prefix }}
          {{ item.extra_info_content.toString()
          .replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}
        </p>
      </template>
      <template
        v-if="item.filter_options && item.filter_options.length > 0">
        <br><p class="medium-gray f4 capitalize dib mb0">
          {{ $t("message.show") }}:</p>
        <span
          v-for="filter in item.filter_options"
          :key="filter"
          href="#"
          class="burgundy no-underline underline-hover pointer f4"
          @click="$emit('select-filter', filter)">{{ filter + '  ' }}
        </span>
      </template>
    </div>
    <div
      class="ml-auto">
      <a
        :href="item.url"
        class="select-button f4 ba burgundy br2 ph3 pv2 mr3 dib mt2 capitalize
               hover-bg-burgundy">{{ $t("message.select") }}
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "SelectableItem",
  props: {
    item: {
      type: Object,
      default() {
        return null;
      },
    },
  },
  data() {
    return {
    };
  },
  methods: {
  },
};
</script>

<template>
  <div
    id="selectable-item"
    :class="item.bg_light_grey"
    class="flex flex-row flex-nowrap pv3">
    <img
      :src="item.img"
      class="search-icon-size ph2">
    <div
      class="ph3">
      <h3
        class="red mv0 f3 fontweight-400">{{ item.name }}</h3>
      <small
        class="medium-gray f5">
        {{ item.id_description }}: {{ item.id }}<br>
      </small>
      <small
        class="medium-gray f5">
        {{ item.extra_info }}: {{ item.extra_info_content }}
      </small>
      <template
        v-if="item.filter_options && item.filter_options.length > 0">
        <br><span class="medium-gray f4">Show:</span>
        <a
          v-for="filter in item.filter_options"
          :key="filter"
          href="#"
          class="burgundy no-underline underline-hover f4"
          @click="$emit('select-filter', filter)">{{ filter + '  ' }}
        </a>
      </template>
    </div>
    <div
      class="ml-auto">
      <a
        :href="item.url"
        class="f4 ba burgundy br2 ph3 pv2 mr2 dib mt2 no-underline">Select
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

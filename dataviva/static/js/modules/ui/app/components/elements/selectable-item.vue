<template>
  <div
    id="selectable-item"
    :class="item.bg_light_grey"
    class="flex flex-row flex-nowrap pv3">

    <div class="w4 tc">
      <img
        v-if="item.img"
        :src="item.img"
        class="search-icon-size mh1">
      <div class="pt3 mh3 search-icon-size">  
        <i
          v-if="item.icon"
          :class="'f1 lh-copy' + item.icon"/>
      </div>  
    </div>

    <div
      class="ph1">
      <h3
        class="red mv0 f3 fw4">{{ item.name }}</h3>
      <small
        class="medium-gray f5">
        {{ item.id_description }}: {{ item.id }}<br>
      </small>
      <small
        v-if="item.extra_info"
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
        class="f4 ba burgundy br2 ph3 pv2 mr3 dib mt2 no-underline">Select
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

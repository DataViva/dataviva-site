<template>
  <div>
    <div v-for="database in databases">
      <span class="pointer" v-on:click="selectDataBase(database)">
        {{t_(database, "name")}}
        <i v-bind:class="database.icon"></i>
      </span>
    </div>
    
    <selector
      v-if="show"
      v-bind:db="database"
      v-bind:confs="confs"
      v-on:close="closeModal"/>
  </div>
</template>

<script>
import "../../assets/css/*.css"

export default {
  name: "DataBaseSelector",
  data() {
    return {
      show: false,
      confs: {
        api_url: dataviva.api_url || "http://api.dataviva.info/",
        s3_host: dataviva.s3_host || "https://dataviva-site-production.s3.amazonaws.com",
        lang: dataviva.language || "pt",
      },
      database: "",
      databases: [
        {
          name_en: "Brazilian Locations",
          name_pt: "Localidades Brasileiras",
          code: "location",
          group_opts: ["region", "state", "mesoregion", "microregion"
            , "municipality"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Population"],
          extra_info_label: "Population", 
          endpoint: "municipality",
          img_path: "/static/img/icons/bra/bra_",
          icon: "dv-bra"
        },
        {
          name_en: "Occupations",
          name_pt: "Ocupações",
          code: "occupation",
          group_opts: ["main group", "familie"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Total Jobs"],
          extra_info_label: "Total Jobs", 
          endpoint: "occupation_group",
          img_path: "/static/img/icons/cbo/cbo_",
          icon: "dv-occupation"
        },
        {
          name_en: "Economic Activities",
          name_pt: "Atividades Econômicas",
          code: "industry",
          group_opts: ["section", "division", "classe"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Total Jobs"],
          extra_info_label: "Total Jobs", 
          endpoint: "municipality",
          img_path: "",
          icon: "dv-industry"
        },
        {
          name_en: "Products",
          name_pt: "Produtos",
          code: "product",
          group_opts: ["product_chapter", "position"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Exports"],
          extra_info_label: "Exports", 
          endpoint: "product",
          img_path: "",
          icon: "dv-product"
        },
        {
          name_en: "Trade Partners",
          name_pt: "Parceiros Comerciais",
          code: "trade_partner",
          group_opts: ["continent", "countrie"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Exports"],
          extra_info_label: "Exports", 
          endpoint: "country",
          img_path: "/static/img/icons/wld/wld_",
          icon: "dv-trade-partner"
        },
        {
          name_en: "Universities",
          name_pt: "Universidades",
          code: "university",
          group_opts: [],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Enrolled"],
          extra_info_label: "Enrolled", 
          endpoint: "university",
          img_path: "",
          icon: "dv-university"
        },
        {
          name_en: "Higher Education",
          name_pt: "Ensino Superior",
          code: "hedu_course",
          group_opts: ["field", "major"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Enrolled"],
          extra_info_label: "Enrolled", 
          endpoint: "hedu_course",
          img_path: "",
          icon: "dv-major"
        },
        {
          name_en: "Basic Courses",
          name_pt: "Curso Básico",
          code: "basic_course",
          group_opts: ["field", "course"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Enrolled"],
          extra_info_label: "Enrolled", 
          endpoint: "sc_course",
          icon: "dv-basic-course"
        }
      ]
    };
  },
  methods: {
    t_(item, prop) {
      return item[prop + "_" + this.confs.lang];
    },
    selectDataBase(database) {
      this.database = database;
      this.show = true;
    },
    closeModal() {
      this.show = false;
    }
  }
};
</script>

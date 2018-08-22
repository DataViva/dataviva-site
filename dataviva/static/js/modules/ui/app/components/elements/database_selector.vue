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
      @click="selectDataBase(database)">
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

export default {
  name: "DataBaseSelector",
  data() {
    return {
      show: false,
      confs: {
        api_url: dataviva.api_url || "http://api.dataviva.info/",
        s3_host: dataviva.s3_host ||
          "https://dataviva-site-production.s3.amazonaws.com",
        lang: dataviva.language || "pt",
      },
      database: "",
      databases: [
        {
          name: "Brazilian Locations",
          code: "location",
          id_description: "IBGE ID",
          group_opts: [
            "region",
            "state",
            "mesoregion",
            "microregion",
            "municipality",
          ],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Population"],
          extra_info_label: "Population",
          endpoint: "municipality",
          img_path: {
            state: "/static/img/icons/bra/",
            mesoregion: "/static/img/icons/bra/",
            microregion: "/static/img/icons/bra/",
            municipality: "/static/img/icons/bra/",
          },
          icon: {
            db: "dv-bra",
            item: "dv-bra-",
          },
          tooltip_text: `General profile by region, state, mesoregion, 
                         microregion or city. Check its international trade, 
                         economic activity, employment and education data. 
                         Examples: Southeast, Mato Grosso, Recife, 
                         Metropolitan Region of Porto Alegre.`,
        },
        {
          name: "Occupations",
          code: "occupation",
          id_description: "CBO ID",
          group_opts: ["occupation_group", "family"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Total Jobs"],
          extra_info_label: "Total Jobs",
          endpoint: "occupation_family",
          icon: {
            db: "dv-occupation",
            item: "dv-cbo-",
          },
          tooltip_text: `Regions with best employment rates by professional
                         activity, related courses, average wage and job 
                         statistics per year. Examples: Medium Level 
                         Technicians, Industry workers, Receptionists, 
                         Clinicians.`,
        },
        {
          name: "Economic Activities",
          code: "industry",
          id_description: "CNAE ID",
          group_opts: ["industry_section", "industry_division", "classe"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Total Jobs"],
          extra_info_label: "Total Jobs",
          endpoint: "industry_class",
          icon: {
            db: "dv-industry",
            item: "dv-cnae-",
          },
          tooltip_text: `Information on employment rate by region, average 
                         wage by occupation, average monthly income and 
                         economic opportunities. Examples: Businesses, Domestic
                         Service, Education, Restaurants, Call Center, 
                         Religious Organizations.`,
        },
        {
          name: "Products",
          code: "product",
          id_description: "HS ID",
          group_opts: ["product_section", "position"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Exports"],
          extra_info_label: "Exports",
          endpoint: "product",
          icon: {
            db: "dv-product",
            item: "dv-hs-",
          },
          tooltip_text: `Trade Balance data by product, import origin and 
                         export destination, ranking by location, economic 
                         activities and related occupations. Examples: Food,
                         Art and Antiques, Iron Ore, Coffee, Auto Parts.`,
        },
        {
          name: "Trade Partners",
          code: "trade_partner",
          id_description: "WLD ID",
          group_opts: ["continent", "country"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Exports"],
          extra_info_label: "Exports",
          endpoint: "country",
          img_path: {
            country: "/static/img/icons/wld/",
          },
          icon: {
            db: "dv-trade-partner",
            item: "dv-wld-",
          },
          tooltip_text: `Brazil’s top import and export partners, trade data 
                         by type of product or supplier city. Examples: Asia,
                         Africa, Europe, Mexico, Japan, USA, China, 
                         the Netherlands, Iran.`,
        },
        {
          name: "Universities",
          code: "university",
          id_description: "ID",
          group_opts: [],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Enrolled"],
          extra_info_label: "Enrolled",
          endpoint: "university",
          icon: {
            db: "dv-university",
            item: "dv-university-",
          },
          tooltip_text: `Number of enrollments in each offered course, student
                         status and similar university profiles. Examples: 
                         USP, UFMG, PUC Goiás.`,
        },
        {
          name: "Higher Education",
          code: "hedu_course",
          id_description: "ID",
          group_opts: ["hedu_course_field", "major"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Enrolled"],
          extra_info_label: "Enrolled",
          endpoint: "hedu_course",
          icon: {
            db: "dv-major",
            item: "dv-course-hedu-",
          },
          tooltip_text: `List of universities and cities that offer 
                         post-secondary courses or the selected field of 
                         study. Examples: Education, Health Sciences, Law, 
                         Production Engineering, Physiotherapy.`,
        },
        {
          name: "Basic Courses",
          code: "basic_course",
          id_description: "ID",
          group_opts: ["course_field", "course"],
          order_opts: ["name", "extra_info"],
          order_labels: ["Name", "Enrolled"],
          extra_info_label: "Enrolled",
          endpoint: "sc_course",
          icon: {
            db: "dv-basic-course",
            item: "dv-course-sc-",
          },
          tooltip_text: `Brazilian schools that offer professional education
                         and enrollment ranking by city. Examples: Elementary 
                         School, High School, Nursing Technician, Agriculture
                        and Livestock Technician.`,
        },
      ],
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

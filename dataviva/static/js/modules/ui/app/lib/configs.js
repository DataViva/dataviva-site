export const env = {
  api_url: dataviva.api_url || "http://api.dataviva.info/",
  s3_host: dataviva.s3_host || "https://dataviva-site-production.s3.amazonaws.com",
  lang: dataviva.language || "pt",
};

export const databases = {
  location: {
    name: "Brazilian Locations",
    code: "location",
    id_description: "IBGE ID",
    group_opts: ["region", "state", "mesoregion", "microregion"
      , "municipality"],
    order_opts: ["name", "extra_info"],
    order_labels: ["Name", "Population"],
    extra_info_label: "Population", 
    endpoint: "municipality",
    img_path: {
      "state": "/static/img/icons/bra/",
      "mesoregion": "/static/img/icons/bra/",
      "microregion": "/static/img/icons/bra/",
      "municipality": "/static/img/icons/bra/",
    },
    icon: {
      db: "dv-bra",
      item: "dv-bra-",
    },
  },
  occupation: {
    name: "Occupations",
    code: "occupation",
    id_description: "CBO ID",
    group_opts: ["main group", "family"],
    order_opts: ["name", "extra_info"],
    order_labels: ["Name", "Total Jobs"],
    extra_info_label: "Total Jobs", 
    endpoint: ["occupation_group", "occupation_family"],
    icon: {
      db: "dv-occupation",
      item: "dv-cbo-",
    },
  },
  industry: {
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
      item: "dv-hs-",
    },
  },
  product: {
    name: "Products",
    code: "product",
    id_description: "HS ID",
    group_opts: ["product_chapter", "position"],
    order_opts: ["name", "extra_info"],
    order_labels: ["Name", "Exports"],
    extra_info_label: "Exports", 
    endpoint: "product",
    icon: {
      db: "dv-product",
      item: "",
    },
  },
  trade_partner: {
    name: "Trade Partners",
    code: "trade_partner",
    id_description: "WLD ID",
    group_opts: ["continent", "country"],
    order_opts: ["name", "extra_info"],
    order_labels: ["Name", "Exports"],
    extra_info_label: "Exports", 
    endpoint: "country",
    img_path: {
      "country": "/static/img/icons/wld/",
      "continent": "/static/img/icons/wld/",
    },
    icon: {
      db: "dv-trade-partner",
      item: "",
    },
  },
  university: {
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
      item: "dv-university-t",
    },
  },
  hedu_course: {
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
  },
  basic_course: {
    name: "Basic Courses",
    code: "basic_course",
    id_description: "ID",
    group_opts: ["field", "course"],
    order_opts: ["name", "extra_info"],
    order_labels: ["Name", "Enrolled"],
    extra_info_label: "Enrolled", 
    endpoint: ["sc_course_field", "sc_course"],
    icon: {
      db: "dv-basic-course",
      item: "",
    }
  }
};

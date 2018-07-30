import Vue from "vue";
import * as Components from "./components/**/*.vue";

const selector = new Vue({ render: h => h("DataBaseSelector") });
Object.values(Components).map(a => a.name && Vue.component(a.name, a));

if (document.getElementById("database-selector") != null) {
  selector.$mount("database-selector");
}

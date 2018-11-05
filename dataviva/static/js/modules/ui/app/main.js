import Vue from "vue";
import i18n from "./lib/i18n";
import * as Components from "./components/**/*.vue";
import "./assets/css/*.css";

const selector = new Vue({ render: h => h("DataBaseSelector"), i18n });
let selectorModifier = null;

Object.values(Components).forEach((item) => {
  // Selector modifier componente need to be created dynamic
  if (item.name === "SelectorModifier") {
    selectorModifier = Vue.extend(item);
  } else {
    Vue.component(item.name, item);
  }
});

const selectorEL = document.getElementById("database-selector");
const modifiersEL = document.getElementsByTagName("optionChanger");

// Render if the DOM element exist (only in front page)
if (selectorEL) {
  selector.$mount("database-selector");
}

// Every tag name optionChanger create the component on click
Object.values(modifiersEL).forEach((element) => {
  if (element.dataset) {
    const item = element;
    item.onclick = ($event) => {
      const modifierEL = $event.currentTarget;
      const modifierData = modifierEL.dataset;

      if (modifierData) {
        selectorModifier({
          i18n,
          name: "selectorModifier",
          el: modifierEL,
          propsData: modifierData,
        });
      }
    };
  }
});

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
for (let index in Object.keys(modifiersEL)) {
  if (modifiersEL[index].dataset) {
    modifiersEL[index].onclick = function ($event) {
      const modifiersEL = $event.currentTarget;
      const modifierData = modifiersEL.dataset;

      if (modifierData) {
        new selectorModifier({
          i18n,
          name: "selectorModifier",
          el: modifiersEL,
          propsData: modifierData
        });
      }
    }
  }
} 

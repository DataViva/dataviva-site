import Vue from "vue";
import i18n from "/lib/i18n";
import * as Components from "./components/**/*.vue";
import "./assets/css/*.css"

const selector = new Vue({ render: h => h("DataBaseSelector"), i18n });
let selector_modifier = null;

for(let i in Components) {
  let item = Components[i];

  // Selector modifier componente need to be created dynamic
  if (item.name == 'SelectorModifier'){
    selector_modifier = Vue.extend(item);
  }
  else {
    Vue.component(item.name, item);
  }
}

const selector_el = document.getElementById("database-selector");
const modifiers_el = document.getElementsByTagName("optionChanger");

// Render if the DOM element exist (only in front page)
if (selector_el) {
  selector.$mount("database-selector");
}

// Every tag name optionChanger create the component on click
for (let index in modifiers_el) {
  if(modifiers_el[index].dataset) {
    modifiers_el[index].onclick = function($event) {
      let modifier_el = $event.currentTarget;
      let modifier_data = modifier_el.dataset;

      if (modifier_data) {
        new selector_modifier({
          i18n,
          name: "selector_modifier",
          el: modifier_el,
          propsData: modifier_data
        });
      }
    }
  }
}

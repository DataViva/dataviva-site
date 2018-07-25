import Vue from 'vue';
import * as Components from './components/**/*.vue';

Object.values(Components).map(a => a.name && Vue.component(a.name, a));

if (document.getElementById('vue-selector') != null) {
	var selector = new Vue({ render: h => h('Selector') })
	selector.$mount('vue-selector');
}

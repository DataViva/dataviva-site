import Vue from 'vue';
import * as Components from './components/**/*.vue';

Object.values(Components).map(a => a.name && Vue.component(a.name, a));
var selector = new Vue({ render: h => h('DataBaseSelector') })

if (document.getElementById('database-selector') != null) {
	selector.$mount('database-selector');
}
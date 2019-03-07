import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VModal from 'vue-js-modal'
import store from './store'
import CKEditor from '@ckeditor/ckeditor5-vue';

Vue.use(VModal)
Vue.use(CKEditor);

Vue.prototype.axios = axios

Vue.config.productionTip = false

new Vue({
    store,
    render: h => h(App)
}).$mount('#app')

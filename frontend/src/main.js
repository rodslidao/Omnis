import Vue from 'vue';
import router from '@/router';
import VueTheMask from 'vue-the-mask';
import VueHaptic from 'vue-haptic';
import VueApexCharts from 'vue-apexcharts';
// import {WebRTC} from 'vue-webrtc';

import AlertFeedback from '@/plugins/alertFeedback';
import AccessControl from '@/plugins/AccessControl';

import timestampToDate from '@/plugins/dateTime';

import { BaklavaVuePlugin } from '@baklavajs/plugin-renderer-vue';
import i18n from './i18n';
import App from './App.vue';
import '@baklavajs/plugin-renderer-vue/dist/styles.css';

import { store } from './store/index';
import vuetify from './plugins/vuetify';
import '@/assets/scss/main.scss';
import '@/assets/scss/_variables.scss';

// import './registerServiceWorker'
import wb from './registerServiceWorker';

// apollo
import { createProvider } from './vue-apollo';

Vue.use(BaklavaVuePlugin);

// const options = {
//   // reconnectionAttempts: 3,
//   reconnection: true,
//   // reconnectionDelay: 10,
//   // timeout: 30,
// };

// Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts);

// Vue.use(JsonEditor)

Vue.use(VueHaptic, {
  // Required. vue-haptic does not provide
  // any out-of-the-box patterns
  defaultHapticTrigger: 'touchstart',

  patterns: {
    success: [10, 100, 30],
    failure: [10, 50, 10, 50, 50, 100, 10],
    long: 200,
    default: 60,
  },
});

// Vue.use(VueTheMask)

// Vue.component(WebRTC.name, WebRTC);
Vue.use(VueTheMask, VueApexCharts, BaklavaVuePlugin, i18n);
Vue.use(timestampToDate);

Vue.use(AlertFeedback, {
  store,
});

Vue.use(AccessControl, {
  store,
});

Vue.prototype.$workbox = wb;

new Vue({
  vuetify,
  i18n,
  router,
  apolloProvider: createProvider(),
  store,
  render: (h) => h(App),
}).$mount('#app');

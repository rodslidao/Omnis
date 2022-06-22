import Vue from 'vue';
import App from './App.vue';
import router from '@/router';
import VueTheMask from 'vue-the-mask';
import VueHaptic from 'vue-haptic';
import JsonEditor from 'vue-json-edit';
import VueApexCharts from 'vue-apexcharts';
import i18n from './i18n';
// import {WebRTC} from 'vue-webrtc';

import AlertFeedback from '@/plugins/alertFeedback';

import { BaklavaVuePlugin } from '@baklavajs/plugin-renderer-vue';
import '@baklavajs/plugin-renderer-vue/dist/styles.css';

// import VueSocketIOExt from 'vue-socket.io-extended';
// import { io } from 'socket.io-client';
// import store from './store/index'

// const socket = io('http://192.168.1.31:5000');

// Vue.use(VueSocketIOExt, socket, { store });

// const SocketInstance = SocketIO(MY_URL);
// -------

// import VueSocketIO from 'vue-socket.io';
// import SocketIO from 'socket.io-client';
import { store } from './store/index';
import vuetify from './plugins/vuetify';
import '@/assets/scss/main.scss';
import '@/assets/scss/_variables.scss';

// import './registerServiceWorker'
import wb from './registerServiceWorker';

// apollo
import { createProvider } from './vue-apollo';

Vue.use(BaklavaVuePlugin);

const options = {
  // reconnectionAttempts: 3,
  reconnection: true,
  // reconnectionDelay: 10,
  // timeout: 30,
};

// Vue.use(new VueSocketIO({
//   debug: true,
//   // connection: SocketIO('http://' + process.env.VUE_APP_URL_API_IP +':'+ process.env.VUE_APP_URL_API_PORT, options),
//   connection: SocketIO(`http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}`, options),
//   vuex: {
//     store,
//     mutationPrefix: 'SOCKET_',
//     actionsPrefix: 'SOCKET_',
//   },

// }));

// -------

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
// soket.io instance creat
// import socketio from 'socket.io';
// import VueSocketIO from 'vue-socket.io';
// Vue.use(VueSocketIO, SocketInstance, store)

// Vue.use(VueSocketIO, SocketInstance)
// Vue.component(WebRTC.name, WebRTC);
Vue.use(VueTheMask, JsonEditor, VueApexCharts, BaklavaVuePlugin, i18n);
Vue.use(AlertFeedback, {
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

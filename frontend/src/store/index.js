// import { constants } from "fs";
import Vue from 'vue';
import Vuex from 'vuex';

// import serverJson from "@/engine/data/json/config/editable/server.json";
Vue.use(Vuex);

//import modules
import node from './modules/node';
import alert from './modules/alert';
import auth from './modules/auth';

const store = new Vuex.Store({
  //estado do dado
  modules: {
    node,
    alert,
    auth,
  },
});
export { store };

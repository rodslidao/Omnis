<template>
  <!-- <v-app-bar style="-webkit-app-region: drag" app dense> -->
  <v-app-bar :dark="$route.name == 'node'" v-if="$route.name != 'intro-logo'">
    <router-link to="/">
      <v-btn icon @click="$router.go(-1)" alt v-if="$route.name == 'settings'">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <!-- isso foi nojento -->
      <router-link to="/config">
        <v-btn
          icon
          @click="$router.go(-1)"
          alt
          v-if="$route.name == 'dashboard' || $route.name == 'node'"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
      </router-link>
      <div v-show="$route.name == 'progress'">
        <img
          class="logo"
          src="../assets/img/parallax-logo-06-black.svg"
          alt="logo da parallax"
        />
      </div>
    </router-link>
    <v-spacer>
      <span class="grey--text text--darken-2">
        <h3 v-if="$route.name == 'settings'">Configurações</h3>
        <h3 v-if="$route.name == 'dashboard'">Dashboard</h3>
      </span>
      <h3 v-if="$route.name == 'node'">Editor Node</h3>

      <!-- <h3 v-if="online">Online </h3> -->
      <!-- <h3 v-if="!online">Offline </h3> -->
    </v-spacer>
    <!-- <v-icon v-show="showUpdateUI" dark color="light-green lighten-1" @click="accept()">mdi-reload</v-icon >   -->

    <v-spacer></v-spacer>
    <!-- <SnackBar /> -->

    <RestartButton
      v-if="$route.name == 'settings'"
      :online="isConnected"
    ></RestartButton>

    <v-icon dark color="light-green lighten-1" v-show="isConnected"
      >mdi-lan-check</v-icon
    >
    <v-icon dark color="red darken-1" v-show="!isConnected"
      >mdi-lan-disconnect</v-icon
    >
    <router-link to="/config">
      <v-btn icon v-if="$route.name != 'settings'">
        <v-icon dark id="tune">mdi-tune</v-icon>
      </v-btn>
    </router-link>
    <template v-slot:extension v-if="$route.name == 'node'">
      <TabMenuNodes></TabMenuNodes>
    </template>
  </v-app-bar>
</template>

<script>
import { mapState } from 'vuex';
import { actions } from '@/store/index';
import RestartButton from '@/components/navbar/RestarButton.vue';
import TabMenuNodes from '@/components/node/TabMenuNodes.vue';

export default {
  name: 'NavBar',
  data: () => ({
    actions,
    restartDialog: false,
    online: false,
    showOnlineMsg: false,
    alert: true,
    listImgCantBeShow: ['dashboard', 'node', 'settings'],
  }),

  //checa se existe conexão tem a ver com o pwa
  mounted() {
    this.online = navigator.onLine;
    window.addEventListener('online', () => (this.online = true));
    window.addEventListener('offline', () => {
      this.online = false;
      this.showOnlineMsg = true;
    });
  },

  components: {
    RestartButton,
    TabMenuNodes,
  },
  methods: {
    validateRoute() {
      this.listImgCantBeShow.forEach((element) => {
        if (this.$route.name == element) {
          console.log(element);
          return false;
        }
      });
    },

    close() {
      const remote = require('electron').remote;
      const window = remote.getCurrentWindow();
      window.close();
    },

    //pwa app
    async accept() {
      this.showUpdateUI = false;
      await this.$workbox.messageSW({ type: 'SKIP_WAITING' });
    },
  },

  computed: {
    ...mapState(['isConnected', 'configuration']),
  },
};
</script>

<style scoped lang="scss">
.logo {
  filter: brightness(0) invert(0.6);
  height: 1.4em;
  margin-top: 0.5em;
}
// v-app-bar {
//   z-index: 999;
// }

.alert {
  // position: absolute;
  width: 100%;
  margin: 0 auto;
}
</style>
<template>
  <div>
    <!-- <v-app-bar style="-webkit-app-region: drag" app dense> -->
    <v-app-bar :dark="$route.name == 'node'" v-if="$route.name != 'intro-logo'">
      <!-- <router-link to="/"> -->

      <v-btn
        icon
        to="/progress"
        alt
        v-if="$router.currentRoute.path.split('/')[1] == 'config'"
      >
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
      <!-- </router-link> -->
      <v-spacer>
        <span class="grey--text text--darken-2">
          <h3 v-if="$router.currentRoute.path.split('/')[1] == 'config'">
            {{ $t('settings.name') }}
          </h3>
        </span>
        <h3 v-if="$route.name == 'node'">Editor Node</h3>

        <!-- <h3 v-if="online">Online </h3> -->
        <!-- <h3 v-if="!online">Offline </h3> -->
      </v-spacer>
      <!-- <v-icon v-show="showUpdateUI" dark color="light-green lighten-1" @click="accept()">mdi-reload</v-icon >   -->

      <v-spacer></v-spacer>
      <!-- <SnackBar /> -->

      <v-spacer></v-spacer>

      <login></login>
      <PowerButton
        v-if="$router.currentRoute.path.split('/')[1] == 'config'"
        :online="onlineWeb.value"
      ></PowerButton>

      <router-link
        to="/config"
        v-if="$router.currentRoute.path.split('/')[1] !== 'config'"
      >
        <v-btn icon v-if="$route.name != 'settings'">
          <v-icon dark id="tune">mdi-cog </v-icon>
        </v-btn>
      </router-link>
      <v-icon dark color="red darken-1" v-if="!onlineWeb.value">mdi-web</v-icon>
      <v-icon dark color="red darken-1" v-if="!onlineBack">mdi-wifi-off</v-icon>

      <!-- <template v-slot:extension v-if="$route.name == 'node'">
      <TabMenuNodes></TabMenuNodes>
    </template> -->
    </v-app-bar>
    <v-progress-linear
      v-if="$route.name != 'node' && $apollo.loading"
      indeterminate
    ></v-progress-linear>
    <TabMenuNodes v-show="$route.name == 'node'"></TabMenuNodes>
  </div>
</template>

<script>
import { useOnline } from '@vueuse/core';

import PowerButton from '@/components/navbar/PowerButton.vue';
import TabMenuNodes from '@/components/node/TabMenuNodes.vue';
import Login from '@/views/Auth/Login.vue';

export default {
  name: 'NavBar',

  components: {
    Login,
    PowerButton,
    TabMenuNodes,
  },

  data: () => ({
    restartDialog: false,
    onlineWeb: useOnline(),
    onlineBack: true,
    showOnlineMsg: false,
    alert: true,
  }),

  // checa se existe conexão tem a ver com o pwa
  mounted() {},

  methods: {
    close() {
      const { remote } = require('electron');
      const window = remote.getCurrentWindow();
      window.close();
    },

    // pwa app
    async accept() {
      this.showUpdateUI = false;
      await this.$workbox.messageSW({ type: 'SKIP_WAITING' });
    },
  },

  computed: {},
};
</script>

<style scoped lang="scss">
.logo {
  filter: brightness(0) invert(0.6);
  height: 1.4em;
  margin-top: 0.5em;
}

.alert {
  width: 100%;
  margin: 0 auto;
}
</style>

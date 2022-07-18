<template>
  <v-app class="d-flex">
    <!-- <div class="mx-auto"><Snack-bar v-if="!isConnected"></Snack-bar></div> -->
    <AlertFeedback />
    <DialogAlert />
    <NavBar class="NavBar" v-if="$route.name != 'intro'" />
    <transition>
      <router-view></router-view>
    </transition>
  </v-app>
</template>

<script>
import { mapState } from 'vuex';
import NavBar from '@/components/NavBar.vue';
import DialogAlert from '@/components/DialogAlert.vue';
import AlertFeedback from '@/plugins/alertFeedback/AlertFeedback.vue';

export default {
  name: 'App',

  components: {
    NavBar,
    DialogAlert,
    AlertFeedback,
  },

  data() {
    return {};
  },

  async created() {
    await this.$store.dispatch('auth/getAuthUser');
    await this.$store.dispatch('auth/getLevels');
    if (this.$workbox) {
      this.$workbox.addEventListener('waiting', () => {
        this.showUpdateUI = true;
      });
    }
  },

  computed: {
    ...mapState(['isConnected']),
  },
  methods: {},
};
</script>

<style lang="scss">
::-webkit-scrollbar {
  display: none;
}

.v-toolbar__extension {
  padding: 0;
}

html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  .NavBar {
    display: block;
    // position: absolute;
    z-index: 999;
  }
}
</style>

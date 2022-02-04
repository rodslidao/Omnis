<template>
  <v-app class="d-flex">
    <!-- <div class="mx-auto"><Snack-bar v-if="!isConnected"></Snack-bar></div> -->
    <DialogAlert
      v-if="alertList.length"
      @dismiss="closeDialog()"
      :info="alertList[alertList.length - 1]"
    />
    <NavBar class="NavBar" v-if="$route.name != 'intro'" />
    <div>
    <transition>
      <router-view></router-view>
    </transition>
    </div>
  </v-app>
</template>

<script>
import { mapState } from 'vuex';
import NavBar from '@/components/NavBar.vue';
import DialogAlert from '@/components/DialogAlert.vue';
import gql from 'graphql-tag';

export default {
  name: 'App',

  components: {
    NavBar,
    DialogAlert,
  },

  data() {
    return {
      alertList: [],
      alert: {
        level: 'warning',
        title: 'Deu Ruin',
        description: 'the program not started',
        how2solve: 'press restart button',
        buttonText: 'Ok',
      },
    };
  },

  created() {
    if (this.$workbox) {
      this.$workbox.addEventListener('waiting', () => {
        this.showUpdateUI = true;
      });
    }
    this.alertList.push(this.alert);
  },

  apollo: {
    // // Subscriptions
    // $subscribe: {
    //   // When a tag is added
    //   tagAdded: {
    //     query: gql`
    //       subscription {
    //         alerts {
    //           level
    //           title
    //           description
    //           how2solve
    //           buttonText
    //         }
    //       }
    //     `,
    //     // Result hook
    //     // Don't forget to destructure `data`
    //     result({ data }) {
    //       this.alertList.push(data.alerts);
    //       console.log(this.alertList);
    //     },
    //   },
    // },
  },

  computed: {
    ...mapState(['isConnected']),
  },
  methods: {
    closeDialog() {
      console.log('foi');
      this.alertList.pop();
    },
  },
};
</script>

<style lang="scss">
::-webkit-scrollbar {
  display: none;
}

html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  .NavBar {
    display: block;
    position: absolute;
    z-index: 999;
  }
}
</style>

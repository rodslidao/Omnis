<template>
  <div class="warper">
    <div>
      <div v-for="(alert, i) in alertList" :key="i">
        <v-fade-transition leave-absolute>
          <v-snackbar
            v-on="timer(alert.description)"
            :style="{ 'padding-bottom': calcMargin(i) }"
            v-model="snackbar"
            rounded="pill"
            :color="alert.type"
            :timeout="99999"
          >
            <!-- {{(alertList.length - (i+1))*3000}} -->
            {{ alert.description }}

            <template v-slot:action="{ attrs }">
              <v-btn small icon v-bind="attrs" @click="closeDialog()">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </template>
          </v-snackbar>
        </v-fade-transition>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'AlertFeedback',
  data() {
    return {
      defaultTimeout: 5000,
      snackbar: true,
    };
  },

  computed: mapState('alert', {
    alertList: (state) => state.alertList,
  }),

  created() {},

  methods: {
    ...mapActions('alert', ['removeItemList']),
    calcMargin(i) {
      const margin = i * 60 + 'px';
      return margin;
    },

    closeDialog() {
      this.removeItemList();
      // this.alertList.pop();
    },

    timer(description) {
      setTimeout(() => {
        this.alertList.pop();
        // console.log('this.alertList');
      }, this.calculateTimeout(description));
    },

    calculateTimeout(description) {
      // console.log('_________________________________________');
      // console.log(description);
      const words = description.split(' ').length;
      // console.log('words', words);
      const timeout = words * 600;
      // console.log('timeout', timeout);
      if (timeout < this.defaultTimeout) {
        // console.log('timeout defalut', this.defaultTimeout);
        return this.defaultTimeout;
      }
      // console.log('timeout returned', timeout);
      // console.log(timeout);
      return timeout;
    },
  },
};
</script>

<style lang="scss" scoped>
.warper {
}
</style>

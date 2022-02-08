<template>
  <div class="warper">
    <div>
      <div v-for="(alert, i) in alertList" :key="i">
        <v-snackbar
          v-on="timer(alert.description)"
          :style="{ 'padding-bottom': calcMargin(i) }"
          v-model="snackbar"
          rounded="pill"
          :color="alert.type"
          timeout="9000000"
        >
          {{ alert.description }}

          <template v-slot:action="{ attrs }">
            <v-btn small icon v-bind="attrs" @click="closeDialog()">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </template>
        </v-snackbar>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'AlertFeedback',
  data() {
    return {
      defaultTimeout: 4000,
      snackbar: true,
    };
  },

  computed: mapState('main', {
    alertList: (state) => state.alertList,
  }),

  created() {},

  methods: {
    calcMargin(i) {
      const margin = i * 60 + 'px';
      return margin;
    },

    closeDialog() {
      console.log('foi');
      this.alertList.pop();
    },

    timer(description) {
      //init timer
      setTimeout(() => {
        this.alertList.pop();
      }, this.calculateTimeout(description));
    },

    calculateTimeout(description) {
      const letters = description.length;
      console.log('letters', letters);
      const timeout = letters * 13.5;
      console.log('timeout', timeout);
      if (timeout < this.defaultTimeout) {
        console.log('timeout defalut', timeout);
        return this.defaultTimeout;
      }
      console.log('timeout returned', timeout);
      console.log(timeout);
      return timeout;
    },
  },
};
</script>

<style lang="scss" scoped>
.warper {
}
</style>

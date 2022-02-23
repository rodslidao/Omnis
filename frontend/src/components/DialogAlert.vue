<template>
  <div>
    <div v-for="alert in alertList" :key="alert.title">
      <v-row justify="center">
        <!-- <v-dialog v-model="state.dialogAlert.show" persistent max-width="300"> -->

        <!-- <v-overlay v-model="state.dialogAlert.show"> -->
        <v-overlay>
          <v-alert
            class="alert"
            border="top"
            colored-border
            :type="alert.level"
            elevation="3"
          >
            <div class="text-h4 font-weight-thin text-capitalize">
              {{ alert.description }}
            </div>

            <div>
              <p class="mt-2">Como Solucionar</p>
              <v-divider></v-divider>
              <p>{{ alert.how2solve }}</p>

              <v-divider></v-divider>
            </div>
            <v-row justify="center">
              <v-btn x-large class="mt-4 mb-3" @click="closeDialog">
                Entendi
                <!-- {{ info.buttonText }} -->
              </v-btn>
            </v-row>
          </v-alert>
        </v-overlay>
      </v-row>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  name: 'DialogAlert',
  data() {
    return {
      alertList: [],
      alertTest: {
        level: 'warning',
        title: 'Deu Ruin',
        description: 'the program not started',
        how2solve: 'press restart button',
        buttonText: 'Ok',
      },
    };
  },

  created() {
    // this.alertList.push(this.alertTest);
  },

  apollo: {
    // Subscriptions
    $subscribe: {
      // When a tag is added
      tagAdded: {
        query: gql`
          subscription {
            alerts {
              level
              title
              description
              how2solve
              buttonText
            }
          }
        `,
        // Result hook
        // Don't forget to destructure `data`
        result({ data }) {
          this.alertList.push(data.alerts);
          console.log(this.alertList);
        },
      },
    },
  },

  methods: {
    okButtonClick() {
      this.$emit('dismiss', true);
      console.log('okButtonClick');
    },
    closeDialog() {
      console.log('foi');
      this.alertList.pop();
    },
  },

  computed: {},
};
</script>

<style>
.alert {
  max-width: 500px;
}
</style>

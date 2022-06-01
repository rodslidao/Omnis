<template>
  <div>
    <div v-for="(alert, index) in alertList" :key="alert.index">
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
            width="600px"
          >
            <div class="text-h4 font-weight-thin text-capitalize">
              {{ alert.title }}
            </div>
              {{ alert.description }}

            <div v-if="alert.how_to_solve">
              <p class="mt-2">Como Solucionar</p>
              <v-divider></v-divider>
              <p>{{ alert.how_to_solve }}</p>

              <v-divider></v-divider>
            </div>
            <v-row justify="center">
              <v-btn x-large class="mt-4 mb-3" @click="closeDialog">
                {{alert.button_text? alert.button_text : 'Entendi'}}
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
        button_text: 'Ok',
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
              how_to_solve
              button_text
              button_action
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

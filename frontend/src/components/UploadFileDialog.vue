<template>
  <v-row justify="center">
    <v-btn
      color="primary"
      dark
      @click.stop="dialog = true"
    >
      Open Dialog
    </v-btn>

    <v-dialog
      v-model="dialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="text-h5">
          Use Google's location service?
        </v-card-title>

        <v-card-text>
          Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Disagree
          </v-btn>

          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Agree
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex';
import { actions } from '../store/index';
import gql from 'graphql-tag';

export default {
  // mixins: [mixins],
  name: 'UploadFileDialog',

  props: {
    text: String,
    icon: String,
  },

  data: () => ({
    selectedPart: 1,
    // onlyCorrectParts: true,
    selection: false,
    actions,
    dialog: false,
    buttonDisable: false,
    step1: true,
    ListOfPartsToMount: [
      {
        partNumber: 0,
        partName: 'Menor',
        src: 'estribo-quadrado.png',
      },
      {
        partNumber: 1,
        partName: 'Maior',
        src: 'estribo-retangular.png',
      },
    ],
  }),

  components: {},

  apollo: {},

  computed: {
    ...mapGetters(['state']),
  },

  methods: {
    ...mapMutations(['SEND_MESSAGE', 'NEW_MESSAGE']),

    async startProcess() {
      this.dialog = true;
      console.log('startProcess');
      const response = await this.$apollo.query({
        query: gql`
          query {
            getProcess {
              data {
                status
              }
            }
          }
        `,
      });
      console.log(this.$apollo.store);
      this.lixo = response.data.getProcess.data.status;
    },

    toPage(page) {
      if (this.$route.name != page) {
        this.$router.push('/' + page);
      }
    },

    less() {
      if (this.state.operation.total >= 2) {
        this.state.operation.total--;
      } else {
        this.buttomDisable = true;
      }
    },
  },
};
</script>

<style lang="scss">
.quantityToProduce {
  width: 100px;
}

.partItem {
  height: 320px;
  width: 250px;
}
.v-card--link:focus:before {
  opacity: 0;
}
</style>

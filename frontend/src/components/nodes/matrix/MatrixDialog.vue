/* eslint-disable max-len */
<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="650px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-form ref="form" v-model="isValidSimpleForm" v-if="!isAdvanced">
          <v-card-text class="pt-8">
            <NodeConfigTitle
              title="Matriz cadastrada"
              description="Selecione a matriz que você cadastrou."
            >
              <v-select
                @click="getMatrix()"
                required
                :loading="matrixLoading"
                class="middle-select ml-5 mr-5"
                :items="matrixObjList"
                v-model="selectedMatrix"
                item-text="name"
                return-object
                :rules="requiredRules"
                placeholder="Selecione uma Matriz"
              ></v-select>
            </NodeConfigTitle>

            <div v-if="!matrixLoading && selectedMatrix" class="mb-10">
              <MatrixInfoResume
                class="mb-5"
                :slots="selectedMatrix.slots"
                :subdivisions="selectedMatrix.subdivisions"
                :origin="selectedMatrix.origin"
              ></MatrixInfoResume>
              <MatrixViewer
                :slots="selectedMatrix.slots"
                :subdivisions="selectedMatrix.subdivisions"
                :origin="selectedMatrix.origin"
              ></MatrixViewer>
            </div>
          </v-card-text>
        </v-form>
        <v-divider></v-divider>
        <v-card-actions>
          <!-- <v-checkbox v-model="isAdvanced" label="Modo Avançado"></v-checkbox> -->
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1 " text @click="close()" large rounded>
            fechar
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="save"
            rounded
            large
            :disabled="!selectedMatrix"
          >
            salvar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import EventBus from '@/event-bus';
import { mapActions } from 'vuex';
import NodeConfigTitle from '@/components/nodes/NodeConfigTitle.vue';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';
import MatrixViewer from '@/components/nodes/matrix/MatrixViewer.vue';
import MatrixInfoResume from '@/components/nodes/matrix/MatrixInfoResume.vue';
import gql from 'graphql-tag';

export default {
  data: () => ({
    dialog: false,
    isValidAdvancedForm: false,
    isValidSimpleForm: false,
    isAdvanced: false,
    requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],

    matrixLoading: false,
    matrixCopy: null,
    matrixObjList: [],
    selectedMatrix: null,
    slots: null,
    subdivisions: null,

    selectedMatrixInfos: {},
  }),

  components: {
    TextEditable,
    NodeConfigTitle,
    MatrixViewer,
    MatrixInfoResume,
  },

  props: ['option', 'node', 'value'],

  created() {
    this.init();
    EventBus.$on('OPEN_SETTINGS', (nodeId) => {
      if (nodeId === this.node.id) {
        this.dialog = true;
        this.init();
      }
    });
  },

  // watch: {
  //   // whenever question changes, this function will run
  //   selectedMatrix(newMatrix, oldMatrix) {
  //     console.log('selectedMatrix', newMatrix, oldMatrix);
  //     if (oldMatrix !== newMatrix) {
  //       this.selectedMatrix.slots;
  //       this.selectedMatrix.subdivisions;
  //     }
  //   },
  // },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.$refs.form.validate();
      if (
        (this.isAdvanced && this.isValidAdvancedForm) ||
        (!this.isAdvanced && this.isValidSimpleForm)
      ) {
        if (this.isAdvanced) {
          // this.node.setOptionValue('expression', this.advancedExpression);
        } else {
          console.log('save', this.selectedMatrix);
          this.node.setOptionValue('matrix', this.selectedMatrix);
        }

        this.saveNodeConfig(this.node.id);
        this.dialog = false;

        this.init();
      }
    },

    async getMatrix() {
      this.matrixLoading = true;
      const response = await this.$apollo.query({
        query: gql`
          query {
            getNodeInfo(node_type: "MatrixNode") {
              data {
                options
              }
            }
          }
        `,
      });
      // console.log(this.$apollo.store);
      this.matrixObjList = [];
      this.matrixObjList.push(...response.data.getNodeInfo.data.options);

      if (!this.matrixCopy) {
        console.log('entrei', this.matrixCopy);

        this.matrixObjList.push(this.matrixCopy);
        this.selectedMatrix = this.matrixCopy;
      }

      this.matrixLoading = false;
    },

    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.matrixCopy = this.node.getOptionValue('matrix');

      console.log('matrixCopy', this.matrixCopy);
      await this.getMatrix();
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },
};
</script>
<style lang="scss" scoped>
$text-size: 3rem;
$sub-text-size: 2rem;

.simple-mode {
  .sub-text {
    font-size: $text-size;
    color: rgb(63, 63, 63);
    line-height: 3rem;
  }
  .text {
    font-size: $text-size;
    line-height: 4rem;
    color: rgb(233, 233, 233);
  }
  .text-field {
    max-width: 5.5em;
    font-size: $text-size;
  }

  .middle-select {
    max-width: 19.5em;
    width: fit-content;
  }
  //variáveis que são acessadas dentro do componente pelo ::v-deep
  .v-text-field ::v-deep {
    align-self: center;
    padding-top: 0;

    .v-select__selections {
      font-size: $text-size;
      line-height: 1.1em;
    }

    input {
      font-size: $text-size;
      font-weight: 100;
      text-transform: capitalize;
      max-height: 50px;
    }

    label {
      font-size: $text-size;
    }
    .v-text-field button {
      font-size: $text-size;
    }
  }
}
</style>

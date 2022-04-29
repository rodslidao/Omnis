/* eslint-disable max-len */
<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
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
                required
                :loading="matrixLoading"
                class="middle-select ml-5 mr-5"
                :items="matrixObjList"
                v-model="selectedMatrix"
                item-text="name"
                :rules="requiredRules"
                placeholder="Selecione uma Matriz"
              ></v-select>
            </NodeConfigTitle>
          </v-card-text>
        </v-form>

        <MatrixViewer></MatrixViewer>
        <!-- <v-form v-else ref="form" v-model="isValidAdvancedForm">
          <v-card-text class="pt-8">
            <NodeConfigTitle
              title="Falha"
              description="Caso a expressão seja verdadeira, o valor definido aqui sera colocado na saida de sucesso"
            >
              <v-select
                required
                class="middle-select ml-5 mr-5"
                :items="operationObjList"
                v-model="selectedInputOperation"
                item-text="name"
                :rules="requiredRules"
                :placeholder="operationObjList.at(-1).name"
              ></v-select>
              ></NodeConfigTitle
            >
          </v-card-text>
        </v-form> -->
        <v-divider></v-divider>
        <v-card-actions>
          <!-- <v-checkbox v-model="isAdvanced" label="Modo Avançado"></v-checkbox> -->
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1 " text @click="close()" large rounded>
            fechar
          </v-btn>
          <v-btn color="blue darken-1" text @click="save" rounded large>
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
    matrixObjList: null,
    selectedMatrix: null,
  }),

  components: {
    TextEditable,
    NodeConfigTitle,
    MatrixViewer,
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

  mounted() {},

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
          let expression = '';
          expression = `A${this.selectedInputMatrix}B`;
          this.node.setOptionValue('selectedMatrix', expression);
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
            getNodeInfo(node_type: "MATRIX") {
              data {
                options
              }
            }
          }
        `,
      });
      // console.log(this.$apollo.store);
      this.matrixObjList = [];
      this.matrixObjList = response.data.getNodeInfo.data.options;
      console.log(response.data.getNodeInfo.data.options);
      this.matrixLoading = false;
      // make a list of camera name from the response
      // response.data.getNodeInfo.data.options.forEach((item) => {
      //   this.cameraListName.push(item.name);
      // }, this);
    },

    // getMatrixPropertyValueByName(property) {
    //   const result = this.matrixObjList.find(
    //     (matrix) => matrix.value === this.selectedInputMatrix
    //   );

    //   if (result) {
    //     console.log(result[property]);
    //     return result[property];
    //     // return `mdi-${result.icon}`;
    //   }
    //   return '';
    // },

    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.matrixCopy = this.node.getOptionValue('matrix');
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

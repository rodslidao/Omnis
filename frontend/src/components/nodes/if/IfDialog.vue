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

        <v-card-text v-if="!isAdvanced" class="simple-mode">
          <v-col class="d-flex flex-wrap justify-center align-center">
            <div class="text mr-4">SE</div>
            <span class="sub-text">a entrada </span>
            <div class="text mr-4 ml-4">A</div>
            <span class="sub-text"> for </span>
            <v-select
              class="middle-select ml-5 mr-5"
              :items="operationObjList"
              v-model="selectedInputOperation"
              item-text="name"
              :placeholder="operationObjList.at(-1).name"
            ></v-select>
            <span class="sub-text">{{
              getOperationPropertyValueByName('preposition')
            }}</span>
            <div class="ml-4 text">B</div>
            <div class="text mr-4">ENTÃO</div>
            <span class="sub-text">a saida será</span>
            <v-text-field
              class="text-field"
              placeholder="verdadeira"
            ></v-text-field>
          </v-col>
        </v-card-text>
        <v-card-text v-else class="pt-8">
          <NodeConfigTitle
            title="Expressão"
            description="Aqui você poderá fazer uma requisição customizada usando as outras letras como 'C' e 'D' sendo os mesmos operadores usados no Python"
          >
            <v-text-field
              class="text-field"
              placeholder="Exemplo: a>b && c<= d"
            ></v-text-field
          ></NodeConfigTitle>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-checkbox v-model="isAdvanced" label="Modo Avançado"></v-checkbox>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1 " text @click="close()" large rounded>
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="save"
            rounded
            large
          >
            Save
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

export default {
  data: () => ({
    dialog: false,
    valid: false,
    isAdvanced: false,

    inputListCopy: null,
    operationObjList: [
      {
        name: 'igual',
        icon: 'equal-box',
        value: '==',
        preposition: 'a',
      },
      {
        name: 'diferente',
        icon: 'code-not-equal',
        value: '!=',
        preposition: 'de',
      },
      {
        name: 'maior',
        icon: 'code-greater-than',
        value: '>',
        preposition: 'que',
      },
      {
        name: 'menor',
        icon: 'code-less-than',
        value: '<',
        preposition: 'que',
      },
      {
        name: 'maior igual',
        icon: 'code-greater-than-or-equal',
        value: '>=',
        preposition: 'a',
      },
      {
        name: 'menor igual',
        icon: 'code-less-than-or-equal',
        value: '<=',
        preposition: 'a',
      },
    ],
    selectedInputA: null,
    selectedInputB: null,
    selectedInputOperation: null,
  }),
  components: {
    TextEditable,
    NodeConfigTitle,
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
      this.node.setOptionValue('expression', this.getSelectedCameraObj());
      this.saveNodeConfig(this.node.id);
      this.dialog = false;

      this.init();
    },

    getOperationPropertyValueByName(property) {
      const result = this.operationObjList.find(
        (operation) => operation.value === this.selectedInputOperation
      );
      if (result) {
        console.log(result[property]);
        return result[property];
        // return `mdi-${result.icon}`;
      }
      return '';
    },

    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.inputListCopy = this.node.getOptionValue('inputList');
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

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
          <v-card-text class="simple-mode">
            <NodeConfigTitle
              title="Tipo de Aviso"
              description="Selecione o tipo de aviso, ele impacta na cor e no ícone."
            >
              <v-select
                :items="levelList"
                v-model="selectedLevel"
                item-text="name"
                return-object
                required
                :prepend-inner-icon="selectedLevel ? selectedLevel.icon : ''"
                :color="selectedLevel ? selectedLevel.type : ''"
                :item-color="selectedLevel ? selectedLevel.type : ''"
                :rules="requiredRules"
              >
                <template slot="item" slot-scope="data">
                  <v-icon class="mr-3" :color="data.item.type">{{
                    data.item.icon
                  }}</v-icon>
                  {{ data.item.name }}
                </template>
              </v-select>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Título"
              description="Defina um titulo para seu alerta"
            >
              <v-text-field
                required
                class="text-field"
                placeholder="Problema de identificação"
                v-model="title"
                :rules="requiredRules"
                hint=""
              ></v-text-field>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Descrição"
              description="Descreva o porque esse erro acontece"
            >
              <v-textarea
                required
                class="text-field"
                placeholder="Não foi possível identificar os ovos na bandeja, certifique-se..."
                v-model="description"
                :rules="requiredRules"
                outlined
              ></v-textarea>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Como resolver"
              description="Descreva o que pode estar causando o problema e formas de resolve-lo"
            >
              <v-textarea
                class="text-field"
                placeholder="Troque por ovos caipiras"
                v-model="how2solve"
                outlined
              ></v-textarea>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Texto do Botão"
              description="Insira o texto que o botão de confirmar vai ter"
            >
              <v-text-field
                required
                class="text-field"
                placeholder="Entendi"
                v-model="buttonText"
                :rules="requiredRules"
              ></v-text-field>
            </NodeConfigTitle>
          </v-card-text>
        </v-form>
        <v-form v-else ref="form" v-model="isValidAdvancedForm">
          <v-card-text class="pt-8"> </v-card-text>
        </v-form>
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
import gql from 'graphql-tag';
import { mapActions } from 'vuex';
import NodeConfigTitle from '@/components/node/nodes/NodeConfigTitle.vue';
import TextEditable from '@/components/node/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    nodeCopy: null,
    dialog: false,
    isValidAdvancedForm: false,
    isValidSimpleForm: false,
    isAdvanced: false,
    requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],
    selectedLevel: null,
    title: null,
    description: null,
    how2solve: null,
    buttonText: null,
    levelList: [
      { name: 'Aviso', type: 'warning', icon: 'mdi-alert' },
      { name: 'Informações', type: 'info', icon: 'mdi-information' },
      { name: 'Sucesso', type: 'success', icon: 'mdi-check' },
      { name: 'Erro', type: 'error', icon: 'mdi-alert-circle' },
    ],
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

  computed: {},

  // apollo: {
  //   getSerials: {
  //     query: gql`
  //       query {
  //         getSerials {
  //           data {
  //             _id
  //             name
  //           }
  //         }
  //       }
  //     `,
  //     update(data) {
  //       return data.getSerials.data;
  //     },
  //   },

  //   getPorts: {
  //     query: gql`
  //       query getNodeInfo($kwargs: JSON) {
  //         getNodeInfo(node_type: "IoNode", kwargs: $kwargs) {
  //           data {
  //             options
  //           }
  //         }
  //       }
  //     `,
  //     variables() {
  //       return {
  //         // eslint-disable-next-line no-underscore-dangle
  //         kwargs: { board: this.selectedBoard._id },
  //       };
  //     },
  //     update(data) {
  //       console.log(data.getNodeInfo.data.options);
  //       return data.getNodeInfo.data.options;
  //     },
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
          this.node.setOptionValue('level', this.selectedLevel.type);
          this.node.setOptionValue('title', this.title);
          this.node.setOptionValue('description', this.description);
          this.node.setOptionValue('how2solve', this.how2solve);
          this.node.setOptionValue('buttonText', this.buttonText);
        }

        this.saveNodeConfig(this.node.id);
        this.dialog = false;

        this.init();
      }
    },
    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      if (this.node.getOptionValue('level')) {
        this.selectedLevel = this.node.getOptionValue('level');
        this.how2solve = this.node.getOptionValue('how2solve');
        this.title = this.node.getOptionValue('title');
        this.description = this.node.getOptionValue('description');
        this.buttonText = this.node.getOptionValue('buttonText');
      }
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },
};
</script>
<style lang="scss" scoped>
.pwm {
  width: 100%;
  height: 50px;
  // border: 2px solid #e0e0e0;

  .wrapper {
    height: 100%;
    width: val(width);

    .high {
      height: 100%;
      border: 2px;
      border-top-style: solid;
      border-right-style: solid;
      border-bottom-style: none;
      border-left-style: solid;
    }
    .low {
      height: 100%;
      border: 2px;
      border-bottom-style: solid;
      width: fit-content;
    }
  }
}
</style>

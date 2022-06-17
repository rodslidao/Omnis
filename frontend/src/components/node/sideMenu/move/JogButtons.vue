<template>
  <div>
    <side-menu-title
      tooltip="caso queira ir para uma coordenada especifica, click sobre os números."
      tooltipBottom
      >Movimentação</side-menu-title
    >
    <div
      v-for="(axis, index) in getAxisList"
      :key="index"
      v-on.once="generateVariables(axis.name)"
    >
      <div v-if="!axis.disable">
        <div class="d-flex pt-2 pb-2 align-center justify-space-between">
          <div class="d-flex axis-name-container align-center">
            <v-menu offset-y dark>
              <template v-slot:activator="{ on, attrs }">
                <v-btn dark v-bind="attrs" v-on="on" icon>
                  <v-icon> mdi-dots-vertical </v-icon>
                </v-btn>
              </template>
              <v-list dark>
                <v-list-item
                  link
                  v-for="(item, index) in axis.context_menu"
                  :key="index"
                >
                  <v-list-item-title> {{ item.title }}</v-list-item-title>
                  <v-list-item-icon>
                    <v-icon v-text="'mdi-' + item.icon"></v-icon>
                  </v-list-item-icon>
                </v-list-item>
              </v-list>
            </v-menu>

            <div
              class="text-h4 font-weight-medium text-uppercase mr-4"
              :class="(axis.color ? axis.color : 'white') + '--text'"
            >
              {{ axis.name }}
            </div>
            <v-btn
              class="button"
              v-haptic
              :show="axis.hasMoveButton"
              :disabled="axis.disabled"
              icon
              x-large
              @click="moveButton(axis, true)"
            >
              <v-icon dark>
                mdi-{{
                  axis.icons.left.icon ? axis.icons.left.icon : 'plus-circle'
                }}
              </v-icon>
            </v-btn>
          </div>
          <div class="d-flex align-center distance">
            <div
              class="distance distance-region"
              @click="variableList[index].manualDistance = true"
            >
              <v-text-field
                class="pt-1 distance-text-field"
                v-if="variableList[index].manualDistance"
                v-model="variableList[index].distance"
                label="Coordenada que deseja mover"
                single-line
                dense
                type="number"
                :append-icon="
                  variableList[index].distance.length !== 0 ? 'mdi-send' : ''
                "
                @blur="variableList[index].manualDistance = false"
                @click:append="sendDistance(index)"
                autofocus
              ></v-text-field>
              <div v-else class="text-h5 grey--text text--lighten-2 text-end">
                {{ variableList[index].value.toFixed(3) }}
              </div>
            </div>
            <div class="grey--text text--darken-2 ml-2 font-weight-bold">
              {{ axis.unit }}
            </div>
            <v-btn
              class="button"
              v-haptic
              :show="axis.hasMoveButton"
              :disabled="axis.disabled"
              icon
              x-large
              @click="moveButton(axis, false)"
            >
              <v-icon dark>
                mdi-{{
                  axis.icons.right.icon ? axis.icons.right.icon : 'minus-circle'
                }}
              </v-icon>
            </v-btn>
          </div>
        </div>
      </div>
      <v-divider></v-divider>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import SideMenuTitle from '../SideMenuTitle.vue';

const GET_AXIS_LIST = gql`
  query {
    getAxisList {
      _id
      name
      color
      icons
      has_move_button
      disable
      unit
      context_menu
    }
  }
`;

export default {
  components: { SideMenuTitle },
  data() {
    return {
      variableList: [],
      receivedData: [],
      axisList: [
        {
          id: 'iddomeunegocio',
          name: 'x',
          color: 'error',
          icons: {
            left: {
              command: 'G91 \n G0 X-',
              icon: 'minus-circle',
            },
            right: {
              command: 'G91 \n G0 X',
              icon: 'plus-circle',
            },
          },
          hasMoveButton: true,
          disable: false,
          unit: 'mm',
          contextMenu: [
            {
              title: 'Ir para o ZERO',
              command: 'G90 \n G0 Z0',
              icon: 'mdi-home',
            },
            { title: 'Zerar o eixo', command: 'G28 X', icon: 'mdi-home' },
          ],
        },
        {
          id: 'iddomeunegocio2',
          name: 'y',
          color: 'success',
          icons: {
            left: {
              command: 'G91 \n G0 Y-',
              icon: 'minus-circle',
            },
            right: {
              command: 'G91 \n G0 Y',
              icon: 'plus-circle',
            },
          },
          hasMoveButton: true,
          disable: false,
          unit: 'mm',
          contextMenu: [
            {
              title: 'Ir para o ZERO',
              command: 'G90 \n G0 Z0',
              icon: 'mdi-home',
            },
            { title: 'Zerar o eixo', command: 'G28 Y', icon: 'mdi-home' },
          ],
        },
        {
          id: 'iddomeunegocio3',
          name: 'z',
          color: 'info',
          icons: {
            left: {
              command: 'G91 \n G0 Z-',
              icon: 'minus-circle',
            },
            right: {
              command: 'G91 \n G0 Z',
              icon: 'plus-circle',
            },
          },
          hasMoveButton: true,
          disable: false,
          unit: 'mm',
          contextMenu: [
            {
              title: 'Ir para o ZERO',
              command: 'G90 \n G0 Z0',
              icon: 'mdi-home',
            },
            { title: 'Zerar o eixo', command: 'G28 Z', icon: 'mdi-home' },
          ],
        },
        {
          id: 'iddomeunegocio4',
          name: 'a',
          color: 'warning',
          icons: {
            left: {
              command: 'G91 \n G0 A-',
              icon: 'minus-circle',
            },
            right: {
              command: 'G91 \n G0 A',
              icon: 'plus-circle',
            },
          },
          hasMoveButton: true,
          disable: true,
          unit: 'mm',
          contextMenu: [
            {
              title: 'Ir para o ZERO',
              command: 'G90 \n G0 Z0',
              icon: 'mdi-home',
            },
            { title: 'Zerar o eixo', command: 'G28 A', icon: 'mdi-home' },
          ],
        },
      ],
    };
  },

  watch: {
    receivedData(newData) {
      console.log('new', newData);
      // start

      if (newData.controls.jog_position) {
        const data = newData.controls.jog_position;
        Object.entries(data).forEach(([axis, val]) => {
          const index = this.variableList.findIndex(
            (item) => axis === item.name,
            console.log('axis', axis, val)
          );
          if (index !== -1) {
            console.log('valor', val);
            this.variableList[index].value = val;
          }
        });
        // end
      }
    },
  },

  methods: {
    moveButton(button, isNegative) {
      const msg = {
        context: 'joggingStep',
        isNegative,
        id: button.id,
        scale: this.stepsList[this.stepSelected].value,
      };
      this.$emit('sendMessage', msg);
    },

    sendDistance(index) {
      console.log(this.variableList[index].distance);
    },

    generateVariables(name) {
      if (this.variableList.length !== this.axisList.length) {
        const variable = {
          name,
          distance: Number,
          value: 0.00,
          manualDistance: false,
        };
        this.variableList.push(variable);
        // console.log(this.variableList);
      }
    },
  },

  apollo: {
    getAxisList: {
      query: GET_AXIS_LIST,
      // update(data) {
      //   return data.getSerials.data;
      // },
    },

    $subscribe: {
      // When a tag is added
      controls: {
        query: gql`
          subscription {
            controls {
              jog_position
            }
          }
        `,
        // Result hook
        // Don't forget to destructure `data`
        result({ data }) {
          this.receivedData = data;
          // cabo a result
        },
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.axis-name-container {
  left: 0;
}

.distance {
  width: 100%;
}

// .distance-region {
//   background: blue;
// }
.axis-list {
  display: flex;
  flex-direction: column;
  padding-left: 0;
  padding: 3.4%;
  color: white;
}
</style>

<style scoped>
/* remove arrows from text-field */
.distance-text-field::v-deep input[type='number'] {
  -moz-appearance: textfield;
}

.distance-text-field::v-deep input::-webkit-outer-spin-button,
.distance-text-field::v-deep input::-webkit-inner-spin-button {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}
</style>
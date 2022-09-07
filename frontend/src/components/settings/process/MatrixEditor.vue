<template>
  <div class="object-register mt-n6">
    <v-form
      v-model="isValid"
      ref="form"
      rounded
      max-width="700px"
      lazy-validation
    >
      <div class="d-flex flex-wrap">
        <div class="form mb-4">
          <div v-for="(subField, key) in fields2" :key="key">
            <v-autocomplete
              class=""
              v-if="key == 'variable'"
              :label="$t('form.' + key) + (fields2[key].required ? '*' : '')"
              rounded
              multiple
              outlined
              v-model="fields2[key].value"
              :rules="isRequire(key) ? [rules().required] : [true]"
              :items="get_variable_list"
              item-text="name"
              return-object
              chips
              deletable-chips
            ></v-autocomplete>
            <div v-else-if="key == 'order'">
              <div class="text-h6 font-weight-black">
                {{ $t('form.order') }}
              </div>
              <div class="text-subtitle-2 mb-2">
                {{ $t('settings.process.matrix.order') }}
              </div>
              <v-radio-group v-model="fields2[key].value" row>
                <v-radio
                  v-for="(order, i) in order_list"
                  :key="i"
                  :label="order"
                  :value="order"
                ></v-radio>
              </v-radio-group>
            </div>
            <div v-else class="warper">
              <v-text-field
                :label="$t('form.' + key) + (fields2[key].required ? '*' : '')"
                class="select"
                placeholder=""
                outlined
                rounded
                v-model="fields2[key].value"
                dense
                max-width
                :rules="isRequire(key) ? [rules().required] : [true]"
              >
              </v-text-field>
            </div>
          </div>

          <!-- custom -->
          <div v-for="(field, index) in fields" :key="index" class="mt-6">
            <v-row>
              <div>
                <div class="text-h6 font-weight-black">
                  {{ $t('form.' + field.title) }}
                </div>
                <div class="text-subtitle-2 mb-2">
                  {{ $t('settings.process.matrix.' + field.subtitle) }}
                </div>
                <div class="d-flex flex-wrap">
                  <div v-for="(subField, key) in field.fields" :key="key">
                    <v-text-field
                      class="subfields my-2"
                      placeholder=""
                      outlined
                      :color="findColor(key)"
                      rounded
                      v-model.number="field.fields[key]"
                      :type="subField.type || 'number'"
                      dense
                      :oninput="canBeNegative(key)"
                      :label="$t('form.' + key)"
                      :suffix="suffix(key)"
                      @focus="
                        field.title == 'subdivisions'
                          ? (edit = 'sub_' + key)
                          : (edit = key)
                      "
                      @blur="edit = ''"
                    >
                    </v-text-field>
                  </div>
                </div>
              </div>
            </v-row>
          </div>
        </div>
        <div class="preview">
          <matrix-info-resume
            class="mt-4 d-xs-none"
            :class="$vuetify.breakpoint.width < 690 ? 'd-none' : ''"
            :origin="origin"
            :slots="data.slots"
            :subdivisions="data.subdivisions"
          ></matrix-info-resume>
          <matrix-viewer
            class="viewer"
            :edit="edited"
            :slots="data.slots"
            :subdivisions="data.subdivisions"
          ></matrix-viewer>
        </div>
      </div>
      <div class="button">
        <v-btn color="primary" @click="validate()" rounded>
          {{ obj ? $t('buttons.edit') : $t('buttons.register') }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import MatrixInfoResume from '../../node/nodes/matrix/MatrixInfoResume.vue';
import MatrixViewer from '../../node/nodes/matrix/MatrixViewer.vue';

const LIST_VARIABLES = gql`
  query LIST_VARIABLES {
    get_variable_list {
      _id
      name
    }
  }
`;

const UPDATE_MATRIX = gql`
  mutation UPDATE_MATRIX(
    $_id: ID!
    $description: String
    $name: String
    $part_number: String
    $origin: JSON
    $slots: JSON
    $subdivisions: JSON
    $variable: [DBREF_variable]
    $order: String
  ) {
    update_matrix(
      _id: $_id
      input: {
        description: $description
        name: $name
        part_number: $part_number
        origin: $origin
        slots: $slots
        subdivisions: $subdivisions
        variable: $variable
        order: $order
      }
    )
  }
`;

const ADD_MATRIX = gql`
  mutation ADD_MATRIX(
    $description: String
    $name: String
    $part_number: String
    $origin: JSON
    $slots: JSON
    $subdivisions: JSON
    $variable: [DBREF_variable]
    $order: String
  ) {
    create_matrix(
      input: {
        description: $description
        name: $name
        origin: $origin
        part_number: $part_number
        slots: $slots
        subdivisions: $subdivisions
        variable: $variable
        order: $order
      }
    )
  }
`;

export default {
  components: { MatrixInfoResume, MatrixViewer },
  name: 'ObjectRegister',
  props: {
    obj: Object,
  },
  data() {
    return {
      isValid: true,
      edit: '',
      suffixList: ['sizeX', 'sizeY', 'marginX', 'marginY'],
      negativeList: ['originX', 'originY'],
      requireList: ['name'],
      order_list: ['TLR', 'TRL', 'TLB', 'TRB', 'BLU', 'BRU', 'BLR', 'BRL'],
      fields2: {
        name: {
          value: this.obj?.name,
          required: true,
        },
        description: {
          value: this.obj?.description,
        },
        part_number: {
          value: this.obj?.part_number,
        },
        variable: {
          value: this.obj?.variable,
        },
        order: {
          value: this.obj?.order,
          required: true,
        },
      },
      fields: [
        {
          title: 'origin',
          subtitle: 'originSubtitle',
          fields: {
            originX: this.obj?.origin.x || 50,
            originY: this.obj?.origin.y || 50,
          },
        },
        {
          title: 'slots',
          subtitle: 'slotsSubtitle',
          fields: {
            quantityX: this.obj?.slots.qtd.x || 4,
            quantityY: this.obj?.slots.qtd.y || 4,
            sizeX: this.obj?.slots.size.x || 20,
            sizeY: this.obj?.slots.size.y || 20,
            marginX: this.obj?.slots.margin.x || 2,
            marginY: this.obj?.slots.margin.y || 2,
          },
        },
        {
          title: 'subdivisions',
          subtitle: 'subdivisionsSubtitle',
          fields: {
            quantityX: this.obj?.subdivisions.qtd.x || 1,
            quantityY: this.obj?.subdivisions.qtd.y || 1,
            marginX: this.obj?.subdivisions.margin.x || 0,
            marginY: this.obj?.subdivisions.margin.y || 0,
          },
        },
      ],
    };
  },

  apollo: {
    // Simple query that will update the 'hello' vue property
    get_variable_list: LIST_VARIABLES,
  },

  computed: {
    edited() {
      return this.edit;
    },

    origin() {
      return {
        x: this.fields[0].fields.originX,
        y: this.fields[0].fields.originY,
      };
    },

    data() {
      const obj = {
        slots: {
          qtd: {
            x: this.fields[1].fields.quantityX,
            y: this.fields[1].fields.quantityY,
          },
          margin: {
            x: this.fields[1].fields.marginX,
            y: this.fields[1].fields.marginY,
          },
          size: {
            x: this.fields[1].fields.sizeX,
            y: this.fields[1].fields.sizeY,
          },
        },
        subdivisions: {
          qtd: {
            x: this.fields[2].fields.quantityX,
            y: this.fields[2].fields.quantityY,
          },
          margin: {
            x: this.fields[2].fields.marginX,
            y: this.fields[2].fields.marginY,
          },
        },
      };
      return obj;
    },
  },

  methods: {
    rules() {
      return {
        required: (value) => !!value || this.$t('form.required'),
      };
    },

    findColor(key) {
      if (key.slice(-1) === 'X') return 'error';
      if (key.slice(-1) === 'Y') return 'success';
      return '';
    },

    isRequire(key) {
      if (this.requireList.includes(key)) return true;
      return false;
    },

    canBeNegative(key) {
      console.log(this.negativeList.includes(key));
      if (this.negativeList.includes(key)) return '';
      return 'if(this.value < 0) this.value = 0;';
    },

    validate() {
      if (this.$refs.form.validate()) {
        if (this.obj) {
          this.editMatrix();
        } else {
          this.addMatrix();
        }
      } else {
        this.formHasErrors = true;
        this.$alertFeedback(this.$t('alerts.formError'), 'error');
      }
    },

    suffix(key) {
      if (this.suffixList.includes(key)) return 'mm';
      return '';
    },

    async addMatrix() {
      await this.$apollo
        .mutate({
          mutation: ADD_MATRIX,
          variables: {
            description: this.fields2.description.value,
            name: this.fields2.name.value,
            part_number: this.fields2.part_number.value,
            origin: this.origin,
            slots: this.data.slots,
            subdivisions: this.data.subdivisions,
            variable: this.fields2.variable.value,
            order: this.fields2.order.value,
          },
        })

        .then(() => {
          // Result
          this.$emit('refetch');
          this.$alertFeedback(
            this.$t('alerts.registerMatrixSuccess'),
            'success'
          );
        })

        .catch((error) => {
          // Error
          this.$alertFeedback(
            this.$t('alerts.registerMatrixFail'),
            'error',
            error
          );
          // We restore the initial user input
        });
    },

    async editMatrix() {
      console.log(this.fields2.order);
      await this.$apollo
        .mutate({
          mutation: UPDATE_MATRIX,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            _id: this.obj._id,
            description: this.fields2.description.value,
            name: this.fields2.name.value,
            part_number: this.fields2.part_number.value,
            origin: this.origin,
            slots: this.data.slots,
            subdivisions: this.data.subdivisions,
            variable: this.fields2.variable.value,
            order: this.fields2.order.value,
          },
        })

        .then(() => {
          // Result

          this.$emit('refetch');
          this.$alertFeedback(this.$t('alerts.updateMatrixSuccess'), 'success');
          this.$router.back();
        })

        .catch((error) => {
          this.$alertFeedback(
            this.$t('alerts.updateMatrixSuccess'),
            'error',
            error
          );
          // We restore the initial user input
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.object-register {
  .form {
    max-width: 650px;
    min-width: 310px;
    margin-right: 2rem;
  }

  .button {
    position: absolute;
    right: 22px;
    bottom: 22px;
  }

  .preview {
    max-width: 900px;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 370px;
  }

  .subfields {
    max-width: 150px;
    ::v-deep .v-text-field__details {
      display: none;
    }
  }

  .row {
    margin: 0;
  }
  .viewer {
    margin-top: 20px;
    width: 100%;
  }
}
</style>

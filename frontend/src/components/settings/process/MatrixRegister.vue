<template>
  <div class="object-register mt-11">
    <v-form
      v-model="isValid"
      ref="form"
      rounded
      max-width="700px"
      lazy-validation
    >
      <!-- <div v-for="(item, index) in items" :key="index">
        <v-row>
          <v-col cols="4" class="d-flex align-center">
            <v-badge dot bordered color="error" v-if="item.required">
              <div class="font-weight-bold">
                {{ $t('form.' + item.field) }}
              </div></v-badge
            >
            <div v-else class="font-weight-bold">
              {{ $t('form.' + item.field) }}
            </div>
          </v-col>
          <v-col cols="8" class="field">
            <v-row>
              <v-text-field
                placeholder=""
                outlined
                rounded
                v-model.number="obj[item.field]"
                type="number"
                dense
                :rules="item.required ? [rules().required] : [true]"
                full-width
                @keyup.enter="colorShow = false"
              >
              </v-text-field>
            </v-row>
          </v-col>
        </v-row>
      </div> -->
      <!-- custom -->
      <div v-for="(field, index) in fields" :key="index">
        <v-row>
          <div>
            <div class="text-h6 font-weight-black">
              {{ $t('form.' + field.title) }}
            </div>
            <div class="text-subtitle-2 mb-5">
              {{ $t('form.' + field.subtitle) }}
            </div>
            <div class="d-flex flex-wrap">
              <div v-for="(subField, index2) in field.fields" :key="index2">
                <v-text-field
                  class="subfields my-4"
                  placeholder=""
                  outlined
                  rounded
                  v-model.number="data[subField.obj]"
                  :type="subField.type || 'number'"
                  dense
                  :label="$t('form.' + subField.title)"
                  :suffix="subField.suffix"
                  @focus="edit = subField.selected"
                >
                </v-text-field>
              </div>
              {{ data }}
            </div>
          </div>
        </v-row>
      </div>
      <v-divider class="my-4"></v-divider>
      <!-- slots: {{ slots }} sub: {{ subdivisions }} -->
      <matrix-info-resume
        class="mt-4"
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
      <div class="d-flex mt-4">
        <v-badge dot bordered color="error">
          <div class="text-subtitle-2">
            {{ $t('form.requiredFields') }}
          </div></v-badge
        >
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="validate()" rounded>
          {{ $t('buttons.register') }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import MatrixInfoResume from '../../node/nodes/matrix/MatrixInfoResume.vue';
import MatrixViewer from '../../node/nodes/matrix/MatrixViewer.vue';

const ADD_MATRIX = gql`
  mutation ADD_MATRIX(
    $color_hex: String
    $color_name: String
    $description: String
    $img: String
    $name: String
    $part_number: String
    $parts: Int
    $supplier: String
    $unit: String
  ) {
    createTarget(
      input: {
        color_hex: $color_hex
        color_name: $color_name
        description: $description
        img: $img
        name: $name
        part_number: $part_number
        parts: $parts
        supplier: $supplier
        unit: $unit
      }
    )
  }
`;

export default {
  components: { MatrixInfoResume, MatrixViewer },
  name: 'ObjectRegister',
  props: {
    items: Array,
  },
  data() {
    return {
      isValid: true,
      colorShow: false,
      picker: false,
      edit: '',
      obj: { slotsX: 0 },
      data: {
        slots: {
          qtd: { x: 5, y: 10 },
          margin: { x: 3, y: 3 },
          size: { x: 41, y: 24 },
        },
        subdivisions: { qtd: { x: 1, y: 1 }, margin: { x: 0, y: 0 } },
      },
    };
  },

  beforeCreated() {
    this.items.forEach((item) => {
      console.log(item);
      this.obj[item.field] = 1;
    });
  },

  computed: {
    edited() {
      return this.edit;
    },

    origin() {
      return {
        x: this.obj.origemX,
        y: this.obj.origemY,
      };
    },

    fields() {
      const obj = [
        {
          title: 'slots',
          subtitle: 'Quantity of slots, margins and size',
          fields: [
            {
              title: 'quantityX',
              value: 0,
              selected: 'distItemX',
              // value: this.selected.slotsX,
            },
            {
              title: 'quantityY',
              value: 0,
              selected: 'distItemY',
              // value: this.selected.slotsX,
            },
            {
              title: 'sizeX',
              value: 0,
              suffix: 'mm',
              selected: 'distItemX',
              // value: this.selected.slotsX,
            },
            {
              title: 'sizeY',
              value: 0,
              suffix: 'mm',
              selected: 'distItemY',
              // value: this.selected.slotsX,
            },
            {
              title: 'marginX',
              value: 0,
              suffix: 'mm',
              selected: 'slots.margin.x',
              // value: this.selected.slotsX,
            },
            {
              title: 'marginY',
              value: 0,
              suffix: 'mm',
              selected: 'slots.margin.y',
              // value: this.obj.slotsX,
            },
          ],
        },
      ];
      return obj;
    },

    // data() {
    //   return {
    //     slots: {
    //       qtd: {
    //         x: 1,
    //         y: 1,
    //       },
    //       margin: {
    //         x: 1,
    //         y: 1,
    //       },
    //       size: {
    //         x: 1,
    //         y: 1,
    //       },
    //     },
    //     subdivisions: {
    //       qtd: {
    //         x: 1,
    //         y: 1,
    //       },
    //       margin: {
    //         x: 1,
    //         y: 1,
    //       },
    //     },
    //   };
    // },

    // slots() {
    //   return {
    //     qtd: {
    //       x: this.obj.slotsX || 1,
    //       y: this.obj.slotsY || 1,
    //     },
    //     margin: {
    //       x: this.obj.slotsMarginX || 1,
    //       y: this.obj.slotsMarginY || 1,
    //     },
    //     size: {
    //       x: this.obj.slotsSizeX || 1,
    //       y: this.obj.slotsSizeY || 1,
    //     },
    //   };
    // },
    // subdivisions() {
    //   return {
    //     qtd: {
    //       x: this.obj.subdivisionsX || 1,
    //       y: this.obj.subdivisionsY || 1,
    //     },
    //     margin: {
    //       x: this.obj.subdivisionsMarginX || 1,
    //       y: this.obj.subdivisionsMarginY || 1,
    //     },
    //   };
    // },
  },

  methods: {
    rules() {
      return {
        required: (value) => !!value || 'Required.',
      };
    },

    validate() {
      if (this.$refs.form.validate()) {
        console.log(this.obj);
        // this.addObject(this.obj);
      } else {
        this.formHasErrors = true;
      }
    },

    async addObject(obj) {
      console.log('input', obj);

      await this.$apollo
        .mutate({
          mutation: ADD_MATRIX,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            color_hex: obj.color_hex,
            description: obj.description,
            img: obj.img,
            name: obj.name,
            part_number: obj.part_number,
            parts: parseInt(obj.parts),
            supplier: obj.supplier,
            unit: obj.unit,
          },
        })

        .then(() => {
          // Result
          this.$alertFeedback(this.$t('alerts.updateUserSuccess'), 'success');
          this.$refs.form.reset();
        })

        .catch((error) => {
          // Error
          this.$alertFeedback(this.$t('alerts.updateUserFail'), 'error', error);
          // We restore the initial user input
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.object-register {
  max-width: 550px;

  .subfields {
    max-width: 120px;
  }

  .row {
    margin: 0;
  }
  .viewer {
    margin-top: 20px;
    width: 100%;
    height: 500px;
  }
  .field {
    padding: 1.5rem 0;
  }
  ::v-deep .v-text-field__details {
    display: none;
  }
}
</style>

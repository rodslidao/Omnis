<template>
  <div class="object-register mt-11">
    <v-form
      v-model="isValid"
      ref="form"
      rounded
      max-width="700px"
      lazy-validation
    >
      <div v-for="(item, index) in items" :key="index" v-on="generateObj(item)">
        <v-row>
          <v-col cols="4" class="d-flex align-center">
            <!-- {{ item }} -->
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
                v-model="obj[item.field]"
                dense
                :rules="item.required ? [rules().required] : [true]"
                full-width
                @keyup.enter="colorShow = false"
              >
                <template v-slot:prepend-inner v-if="item.field == 'color_hex'">
                  <v-badge
                    class="mb-n2"
                    bordered
                    inline
                    :color="obj[item.field]"
                  ></v-badge>
                </template>
                <template v-slot:append v-if="item.field == 'color_hex'">
                  <div>
                    <v-btn
                      small
                      icon
                      @click="(picker = !picker), (colorShow = !colorShow)"
                      ><v-icon :color="colorShow ? 'success' : ''">{{
                        !colorShow ? 'mdi-eyedropper-variant' : 'mdi-check'
                      }}</v-icon></v-btn
                    >
                  </div>
                </template></v-text-field
              ></v-row
            >
            <v-row>
              <v-color-picker
                dot-size="25"
                v-if="colorShow && item.field == 'color_hex'"
                hide-inputs
                v-model="obj[item.field]"
                mode="hexa"
                @update:color="(a) => (obj[item.field] = a.hexa)"
              ></v-color-picker>
            </v-row>
          </v-col>
        </v-row>
      </div>
      <v-divider class="mt-4"></v-divider>
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

const ADD_OBJECT = gql`
  mutation ADD_OBJECT(
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
  name: 'ObjectRegister',
  props: {
    items: Array,
  },
  data() {
    return {
      isValid: true,
      colorShow: false,
      picker: false,
      obj: {},
    };
  },

  methods: {
    rules() {
      return {
        required: (value) => !!value || 'Required.',
      };
    },

    generateObj(item) {
      this.obj[item.field] = item.value;
    },

    validate() {
      if (this.$refs.form.validate()) {
        this.addObject(this.obj);
      } else {
        this.formHasErrors = true;
      }
    },

    async addObject(obj) {
      console.log('input', obj);

      await this.$apollo
        .mutate({
          mutation: ADD_OBJECT,
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

  // computed: {
  //   items() {
  //     return [
  //       {
  //         field: 'name',
  //         value: null,
  //         title: 'name',
  //         required: true,
  //       },
  //       {
  //         field: 'description',
  //         value: null,
  //         title: 'description',
  //       },
  //       {
  //         field: 'part_number',
  //         value: null,
  //         title: 'part_number',
  //       },
  //       {
  //         field: 'supplier',
  //         value: null,
  //         title: 'supplier',
  //       },
  //       {
  //         field: 'parts',
  //         value: null,
  //         title: 'parts',
  //       },
  //       {
  //         field: 'unit',
  //         value: null,
  //         title: 'unit',
  //       },
  //       {
  //         field: 'color_hex',
  //         value: '#ffff',
  //         title: 'color',
  //       },
  //       {
  //         field: 'color_name',
  //         value: '',
  //         title: 'color',
  //       },
  //       {
  //         field: 'img',
  //         value: null,
  //         title: 'img',
  //       },
  //     ];
  //   },
  // },
};
</script>

<style lang="scss" scoped>
.object-register {
  max-width: 550px;

  .field {
    padding: 1.5rem 0;
  }
  ::v-deep .v-text-field__details {
    display: none;
  }
}

// $text-size: 3rem;
// $sub-text-size: 2rem;
// .v-text-field ::v-deep {
//   align-self: center;
//   padding-top: 0;

//   .v-select__selections {
//     font-size: $text-size;
//     line-height: 1.1em;
//   }

//   input {
//     font-size: $text-size;
//     font-weight: 100;
//     text-transform: capitalize;
//     max-height: 50px;
//   }

//   label {
//     font-size: $text-size;
//   }
//   .v-text-field button {
//     font-size: $text-size;
//   }
// }
</style>

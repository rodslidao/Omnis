<template>
  <div class="object-register mt-11">
    <v-form v-model="isValid" ref="form" max-width="700px" lazy-validation>
      <div v-for="(item, index) in items" :key="index" v-on="generateObj(item)">
        <v-autocomplete
          class="select"
          v-if="autocompleteFields.includes(item.field)"
          :label="$t('form.' + item.field) + (item.required ? '*' : '')"
          rounded
          multiple
          outlined
          v-model="obj[item.field]"
          :rules="item.required ? [rules().required] : [true]"
          :items="
            item.field == 'variable' ? get_variable_list : get_matrix_list
          "
          item-text="name"
          return-object
          chips
          deletable-chips
        ></v-autocomplete>

        <v-text-field
          v-else
          :label="$t('form.' + item.field) + (item.required ? '*' : '')"
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
          </template>
        </v-text-field>
        <v-color-picker
          dot-size="25"
          v-if="colorShow && item.field == 'color_hex'"
          hide-inputs
          v-model="obj[item.field]"
          mode="hexa"
          @update:color="(a) => (obj[item.field] = a.hexa)"
        ></v-color-picker>
      </div>
      <v-divider class="mt-4"></v-divider>
      <div class="d-flex mt-4">
        <!-- <v-badge dot bordered color="error">
          <div class="text-subtitle-2">
            {{ $t('form.requiredFields') }}
          </div></v-badge
        > -->
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="validate()" rounded>
          {{ edit ? $t('buttons.edit') : $t('buttons.register') }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
import gql from 'graphql-tag';

const LIST_VARIABLES = gql`
  query LIST_VARIABLES {
    get_variable_list {
      _id
      name
    }
  }
`;

const LIST_MATRIX = gql`
  query LIST_MATRIX {
    get_matrix_list {
      _id
      name
    }
  }
`;

const ADD_OBJECT = gql`
  mutation ADD_OBJECT(
    $color_hex: String
    $color_name: String
    $description: String
    $img: String
    $name: String!
    $part_number: String
    $parts: Int
    $supplier: String
    $unit: String
    $variable: [DBREF_variable]
    $matrix: [DBREF_matrix]
  ) {
    create_object(
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
        variable: $variable
        matrix: $matrix
      }
    )
  }
`;

const UPDATE_OBJ = gql`
  mutation UPDATE_OBJ(
    $_id: ID!
    $color_hex: String
    $color_name: String
    $description: String
    $img: String
    $name: String!
    $part_number: String
    $parts: Int
    $supplier: String
    $variable: [DBREF_variable]
    $matrix: [DBREF_matrix]
  ) {
    update_object(
      _id: $_id
      input: {
        color_hex: $color_hex
        color_name: $color_name
        description: $description
        img: $img
        name: $name
        part_number: $part_number
        parts: $parts
        supplier: $supplier
        variable: $variable
        matrix: $matrix
      }
    )
  }
`;

export default {
  name: 'ObjectRegister',
  props: {
    items: Array,
    id: String,
    edit: Boolean,
  },

  data() {
    return {
      isValid: true,
      colorShow: false,
      picker: false,
      autocompleteFields: ['variable', 'matrix'],
      obj: {},
    };
  },

  apollo: {
    get_variable_list: LIST_VARIABLES,
    get_matrix_list: LIST_MATRIX,
  },

  methods: {
    rules() {
      return {
        required: (value) => !!value ||  this.$t('form.required'),
      };
    },

    generateObj(item) {
      this.obj[item.field] = item.value;
    },

    validate() {
      if (this.$refs.form.validate()) {
        if (this.edit) {
          this.aditObject(this.obj);
        } else {
          this.addObject(this.obj);
        }
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
            variable: obj.variable,
            matrix: obj.matrix,
          },
        })

        .then(() => {
          // Result
          this.$alertFeedback(this.$t('alerts.updateUserSuccess'), 'success');
          this.$emit('refetch');
          this.$refs.form.reset();
        })

        .catch((error) => {
          // Error
          this.$alertFeedback(this.$t('alerts.updateUserFail'), 'error', error);
          // We restore the initial user input
        });
    },

    async aditObject(obj) {
      console.log('edit2', obj);
      await this.$apollo
        .mutate({
          mutation: UPDATE_OBJ,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            _id: this.id,
            color_hex: obj.color_hex,
            color_name: obj.color_name,
            date: obj.date,
            description: obj.description,
            img: obj.img,
            name: obj.name,
            part_number: obj.part_number,
            parts: obj.parts,
            supplier: obj.supplier,
            variable: obj.variable,
            matrix: obj.matrix,
          },
        })

        .then(() => {
          // Result
          this.$emit('refetch');
          this.$alertFeedback(this.$t('alerts.updateObjSuccess'), 'success');
          this.$router.back();
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(this.$t('alerts.updateObjFail'), 'error', error);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.object-register {
  max-width: 550px;

  .field {
    padding: 1.5rem 0;
  }
  ::v-deep .v-text-field__details {
    // display: none;
  }
}
</style>

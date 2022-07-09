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
        <v-select
          class="select"
          v-if="item.field == 'sketch'"
          :label="$t('form.' + item.field) + (item.required ? '*' : '')"
          rounded
          v-model="obj[item.field]"
          dense
          :items="get_sketch_list"
          outlined
          item-text="label"
          return-object
        ></v-select>
        <v-text-field
          v-if="!textFieldsIgnore.includes(item.field)"
          :label="$t('form.' + item.field) + (item.required ? '*' : '')"
          placeholder=""
          outlined
          rounded
          v-model="obj[item.field]"
          dense
          :rules="item.required ? [rules().required] : [true]"
          @keyup.enter="colorShow = false"
        >
        </v-text-field>
        <v-autocomplete
          class="select"
          v-if="autocompleteInclude.includes(item.field)"
          :label="$t('form.' + item.field) + (item.required ? '*' : '')"
          rounded
          multiple
          outlined
          v-model="obj[item.field]"
          :rules="item.required ? [rules().required] : [true]"
          :items="item.field == 'object' ? get_object_list : get_matrix_list"
          item-text="name"
          return-object
          chips
          deletable-chips
        ></v-autocomplete>
      </div>
      <v-divider class="mt-4"></v-divider>
      <div class="d-flex mt-4">
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

const LIST_SKETCH = gql`
  query LIST_SKETCH {
    get_sketch_list {
      _id
      label
    }
  }
`;

const LIST_OBJECT = gql`
  query LIST_OBJECT {
    get_object_list {
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

const ADD_PROCESS = gql`
  mutation ADD_PROCESS(
    $sketch: JSON
    $description: String
    $img: String
    $name: String
    $matrix: [JSON]
    $object: [JSON]
  ) {
    create_process(
      input: {
        description: $description
        sketch: $sketch
        img: $img
        name: $name
        matrix: $matrix
        object: $object
      }
    )
  }
`;

const UPDATE_PROCESS = gql`
  mutation UPDATE_PROCESS(
    $_id: ID!
    $description: String
    $img: String
    $name: String
    $sketch: JSON
    $matrix: [JSON]
    $object: [JSON]
  ) {
    update_process(
      _id: $_id
      input: {
        description: $description
        img: $img
        name: $name
        sketch: $sketch
        matrix: $matrix
        object: $object
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
      obj: {},
      textFieldsIgnore: ['sketch', 'matrix', 'object'],
      autocompleteInclude: ['matrix', 'object'],
    };
  },

  apollo: {
    // Simple query that will update the 'hello' vue property
    get_sketch_list: LIST_SKETCH,
    get_object_list: LIST_OBJECT,
    get_matrix_list: LIST_MATRIX,
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
        const oldSelected = this.obj.sketch;
        this.obj.sketch = {
          name: oldSelected?.label,
          // eslint-disable-next-line no-underscore-dangle
          _id: oldSelected?._id,
        };
        this.addObject(this.obj);
      } else {
        this.formHasErrors = true;
      }
    },

    async addObject(obj) {
      await this.$apollo
        .mutate({
          mutation: ADD_PROCESS,
          variables: {
            description: obj.description,
            img: obj.img,
            name: obj.name,
            sketch: obj.sketch,
          },
        })

        .then(() => {
          // Result
          this.$emit('refetch');
          this.$alertFeedback(this.$t('alerts.updateUserSuccess'), 'success');
          this.$refs.form.reset();
        })

        .catch((error) => {
          // Error
          this.$alertFeedback(this.$t('alerts.updateUserFail'), 'error', error);
        });
    },
    async edit(obj) {
      console.log('edit2', obj);
      await this.$apollo
        .mutate({
          mutation: UPDATE_PROCESS,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            _id: this.objToEdit._id,
            description: obj.description,
            img: obj.img,
            name: obj.name,
            sketch: obj.sketch,
            matrix: obj.matrix,
            object: obj.object,
          },
        })

        .then(() => {
          // Result
          this.$emit('refetch');
          this.$alertFeedback(
            this.$t('alerts.updateProcessSuccess'),
            'success',
          );
          this.$router.back()
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(
            this.$t('alerts.updateProcessFail'),
            'error',
            error,
          );
          // We restore the initial user input
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

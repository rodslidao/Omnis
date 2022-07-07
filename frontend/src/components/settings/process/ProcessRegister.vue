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
              <v-select
                class="select"
                v-if="item.field == 'sketch'"
                rounded
                v-model="obj[item.field]"
                dense
                :items="get_sketch_list"
                outlined
                item-text="label"
                return-object
              ></v-select>
              <v-text-field
                v-if="item.field !== 'sketch'"
                placeholder=""
                outlined
                rounded
                v-model="obj[item.field]"
                dense
                :rules="item.required ? [rules().required] : [true]"
                full-width
                @keyup.enter="colorShow = false"
              >
              </v-text-field
            ></v-row>
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

const LIST_SKETCH = gql`
  query LIST_SKETCH {
    get_sketch_list {
      _id
      label
    }
  }
`;

const ADD_OBJECT = gql`
  mutation ADD_OBJECT(
    $sketch: JSON
    $description: String
    $img: String
    $name: String
  ) {
    create_process(
      input: {
        description: $description
        sketch: $sketch
        img: $img
        name: $name
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

  apollo: {
    // Simple query that will update the 'hello' vue property
    get_sketch_list: LIST_SKETCH,
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
          name: oldSelected.label,
          // eslint-disable-next-line no-underscore-dangle
          _id: oldSelected._id,
        };
        this.addObject(this.obj);
      } else {
        this.formHasErrors = true;
      }
    },

    async addObject(obj) {
      await this.$apollo
        .mutate({
          mutation: ADD_OBJECT,
          variables: {
            sketch: obj.sketch,
            description: obj.description,
            img: obj.img,
            name: obj.name,
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
    display: none;
  }
}
</style>

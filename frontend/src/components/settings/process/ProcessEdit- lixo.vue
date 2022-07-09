<template>
  <dialog-confirmation
    :title="$t('settings.process.editProcess.title')"
    description=" "
    max-width="600"
    :persistent="true"
  >
    <template v-slot:description>
      <div class="object-register pr-6 pt-6" v-if="itemsList[0].value">
        <v-form
          v-model="isValid"
          ref="form"
          rounded
          max-width="700px"
          lazy-validation
        >
          <div
            v-for="(item, index) in items"
            :key="index"
            v-on="generateObj(item)"
          >
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
                    v-model="obj[item.field].name"
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
        </v-form>
      </div>
      <v-divider class="mt-4"></v-divider>
    </template>
    <template v-slot:actions>
      <!-- <v-badge dot bordered color="error">
        <div class="text-subtitle-2">
          {{ $t('form.requiredFields') }}
        </div></v-badge
      >
      <v-spacer></v-spacer> -->
      <div class="pb-4 pr-4">
        <v-btn text @click="$emit('cancel-event')" rounded>
          {{ $t('buttons.cancel') }}
        </v-btn>
        <v-btn
          color="primary"
          rounded
          v-on:keyup.enter="validate(obj)"
          @click="validate(obj)"
        >
          {{ $t('buttons.edit') }}
        </v-btn>
      </div>
    </template>
  </dialog-confirmation>
</template>

<script>
import gql from 'graphql-tag';
import DialogConfirmation from '../DialogConfirmation.vue';

const LIST_SKETCH = gql`
  query LIST_SKETCH {
    get_sketch_list {
        _id
        label
    }
  }
`;

export default {
  components: { DialogConfirmation },
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
      show1: true,
      itemsCopy: null,
    };
  },

  computed: {
    itemsList() {
      return this.items;
    },
  },

  mounted() {
    this.itemsCopy = { ...this.items };
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
      // console.log('dento', this.item);
      this.obj[item.field] = item.value;
    },

    validate() {
      if (this.$refs.form.validate()) {

        // correcting infos
        const oldSelected = this.obj.sketch.name;
        this.obj.sketch = {
          name: oldSelected.label,
          // eslint-disable-next-line no-underscore-dangle
          _id: oldSelected._id,
        };
        this.$emit('edit-obj', this.obj);
      } else {
        this.formHasErrors = true;
      }
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

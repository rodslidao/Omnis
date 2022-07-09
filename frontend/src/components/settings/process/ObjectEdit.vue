<template>
  <dialog-confirmation
    :title="$t('settings.process.objects.edit')"
    description=" "
    max-width="600"
    :persistent="true"
  >
    <template v-slot:description>
      <div class="object-register pr-6 pt-6" v-if="itemsList[0].value">
        <v-form v-model="isValid" ref="form" max-width="700px" lazy-validation>
          <div
            v-for="(item, index) in items"
            :key="index"
            v-on="generateObj(item)"
          >
            <v-autocomplete
              class="select"
              v-if="item.field == 'variable'"
              :label="$t('form.' + item.field) + (item.required ? '*' : '')"
              rounded
              multiple
              outlined
              v-model="obj[item.field]"
              :rules="item.required ? [rules().required] : [true]"
              @change="print(obj[item.field])"
              :items="get_variable_list"
              item-text="name"
              return-object
              chips
              deletable-chips
            ></v-autocomplete>
            <v-text-field
              v-else
              :label="$t('form.' + item.field) + (item.required ? '*' : '')"
              rounded
              outlined
              v-model="obj[item.field]"
              dense
              :rules="item.required ? [rules().required] : [true]"
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
            >

            <v-color-picker
              dot-size="25"
              v-if="colorShow && item.field == 'color_hex'"
              hide-inputs
              v-model="obj[item.field]"
              mode="hexa"
              @update:color="(a) => (obj[item.field] = a.hexa)"
            ></v-color-picker>
          </div>
        </v-form>
      </div>
    </template>
    <template v-slot:actions>
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

const LIST_VARIABLES = gql`
  query LIST_VARIABLES {
    get_variable_list {
      _id
      name
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

  created() {
    console.log(this.items);
  },

  apollo: {
    get_variable_list: LIST_VARIABLES,
  },

  computed: {
    itemsList() {
      return this.items;
    },
  },

  mounted() {
    this.itemsCopy = { ...this.items };
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
        // console.log(this.obj);
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
  // ::v-deep .v-text-field__details {
  //   // display: none;
  // }
}
</style>

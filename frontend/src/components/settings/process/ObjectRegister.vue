<template>
  <div class="object-register">
    <v-form
      v-model="isValid"
      ref="form"
      rounded
      max-width="700px"
      lazy-validation
    >
      <div v-for="(item, index) in items" :key="index">
        <v-row>
          <v-col cols="3">
            <!-- {{ item }} -->
            <div class="font-weight-bold">{{ $t('form.' + item.field) }}</div>
          </v-col>
          <v-col cols="2">
            <v-btn
              icon
              elevation="2"
              v-if="item.field == 'color'"
              @click="colorShow = !colorShow"
              class="color"
              outlined
              :color="item.value"
            >
              <v-icon>mdi-eyedropper-variant </v-icon>
            </v-btn>
          </v-col>
          <v-col cols="7" class="field">
            <v-row>
              <v-text-field
                placeholder=""
                outlined
                rounded
                v-model="item.value"
                dense
                full-width
              ></v-text-field
            ></v-row>
            <v-row>
              <color-picker
                v-if="colorShow && item.field == 'color'"
                v-model="item.value"
              ></color-picker>
            </v-row>
          </v-col>
        </v-row>
      </div>
      <v-divider class="mt-4"></v-divider>
      <div class="d-flex mt-4">
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="addObject" rounded>
          {{ $t('buttons.register') }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
import NodeConfigTitle from '../../node/nodes/NodeConfigTitle.vue';
import ColorPicker from 'vue-color-picker-wheel';

export default {
  name: 'ObjectRegister',
  components: { NodeConfigTitle, ColorPicker },
  data() {
    return {
      isValid: true,
      colorShow: false,
    };
  },

  methods: {
    addObject() {
      console.log('items', this.items);
    },
    updateColor(color) {},
  },

  computed: {
    items() {
      return [
        {
          field: 'name',
          value: null,
          title: 'name',
          description: 'name of object',
        },
        {
          field: 'description',
          value: null,
          title: 'description',
          description: 'description of object',
        },
        {
          field: 'part_number',
          value: null,
          title: 'part_number',
          description: 'partNumber of object',
        },
        {
          field: 'supplier',
          value: null,
          title: 'supplier',
          description: 'supplier of object',
        },
        {
          field: 'parts',
          value: null,
          title: 'parts',
          description: 'parts of object',
        },
        {
          field: 'unit',
          value: null,
          title: 'unit',
          description: 'unit of object',
        },
        {
          field: 'date',
          value: null,
          title: 'date',
          description: 'date of object',
        },
        {
          field: 'color',
          value: '#ffff',
          title: 'color',
          description: 'color of object',
        },
        {
          field: 'img',
          value: null,
          title: 'img',
          description: 'color of object',
        },
      ];
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

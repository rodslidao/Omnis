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
          <div v-for="(subField, key) in fields" :key="key">
            <v-text-field
              class="field mb-n6"
              placeholder=""
              outlined
              rounded
              v-model.trim="fields[key].value"
              dense
              :label="$t('form.' + key)"
              max-width
              :rules="isRequire(key) ? [rules().required] : [true]"
              @keyup.enter="validate()"
            >
            </v-text-field>
            {{newName}}
          </div>
        </div>
      </div>
      <div class="button">
        <v-btn color="primary" @click="validate()" rounded>
          {{ $t('buttons.register') }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
import gql from 'graphql-tag';

const ADD_VARIABLE = gql`
  mutation ADD_VARIABLE($name: String!) {
    create_variable(input: { name: $name })
  }
`;

export default {
  name: 'VariableRegister',
  props: {
    items: Array,
  },
  data() {
    return {
      isValid: true,
      colorShow: false,
      picker: false,
      edit: '',
      requireList: ['name'],
      obj: { slotsX: 0 },
      name: '',
      fields: {
        name: {
          value: '',
          required: true,
        },
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

    newName() {
      return this.name;
    },
  },

  methods: {
    rules() {
      return {
        required: (value) => !!value || 'Required.',
      };
    },

    toCase() {
      const newName = this.fields.name.value.toUpperCase();
      this.name = newName.replace(/\s/g, '-');
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

    validate() {
      if (this.$refs.form.validate()) {
        console.log(this.name);
        // this.add(this.obj);
        this.$refs.form.reset();
      } else {
        this.formHasErrors = true;
        this.$alertFeedback(this.$t('alerts.formError'), 'error');
      }
    },

    suffix(key) {
      if (this.suffixList.includes(key)) return 'mm';
      return '';
    },

    async add() {
      await this.$apollo
        .mutate({
          mutation: ADD_VARIABLE,
          variables: {
            name: this.fields.name.value,
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
  }

  .row {
    margin: 0;
  }
  .viewer {
    margin-top: 20px;
    width: 100%;
  }
  .field {
    padding: 1.5rem 0;
    width: 100%;
  }
  ::v-deep .v-text-field__details {
    display: none;
  }
}
</style>

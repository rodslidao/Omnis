<template>
  <div class="edit-matrix mt-n6">
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
            <v-text-field
              class="field mb-n6"
              placeholder=""
              outlined
              rounded
              v-model.number="fields2[key].value"
              dense
              :label="$t('form.' + key)"
              max-width
              :rules="isRequire(key) ? [rules().required] : [true]"
            >
            </v-text-field>
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
                      oninput="if(this.value < 0) this.value = 0;"
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
          {{ $t('buttons.edit') }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import MatrixInfoResume from '../../node/nodes/matrix/MatrixInfoResume.vue';
import MatrixViewer from '../../node/nodes/matrix/MatrixViewer.vue';

const UPDATE_MATRIX = gql`
  mutation UPDATE_MATRIX(
    $_id: ID!
    $description: String
    $name: String
    $part_number: String
    $origin: JSON
    $slots: JSON
    $subdivisions: JSON
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
      }
    )
  }
`;

export default {
  components: { MatrixInfoResume, MatrixViewer },
  name: 'MatrixEdit',
  props: {
    items: Object,
  },
  data() {
    return {
      isValid: true,
      colorShow: false,
      picker: false,
      edit: '',
      suffixList: ['sizeX', 'sizeY', 'marginX', 'marginY'],
      requireList: ['name'],
      obj: { slotsX: 0 },
      fields2: {
        name: {
          value: this.items.name,
          required: true,
        },
        description: {
          value: this.items.description,
        },
        part_number: {
          value: this.items.part_number,
        },
      },
      fields: [
        {
          title: 'origin',
          subtitle: 'originSubtitle',
          fields: {
            originX: this.items.origin.x,
            originY: this.items.origin.y,
          },
        },
        {
          title: 'slots',
          subtitle: 'slotsSubtitle',
          fields: {
            quantityX: this.items.slots.qtd.x,
            quantityY: this.items.slots.qtd.y,
            sizeX: this.items.slots.size.x,
            sizeY: this.items.slots.size.y,
            marginX: this.items.slots.margin.x,
            marginY: this.items.slots.margin.y,
          },
        },
        {
          title: 'subdivisions',
          subtitle: 'subdivisionsSubtitle',
          fields: {
            quantityX: this.items.subdivisions.qtd.x,
            quantityY: this.items.subdivisions.qtd.y,
            marginX: this.items.subdivisions.margin.x,
            marginY: this.items.subdivisions.margin.y,
          },
        },
      ],
    };
  },

  // beforeCreated() {
  //   this.items.forEach((item) => {
  //     console.log(item);
  //   });
  // },

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
        required: (value) => !!value ||  this.$t('form.required'),
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

    validate() {
      if (this.$refs.form.validate()) {
        this.editMatrix(this.obj);
      } else {
        this.formHasErrors = true;
        this.$alertFeedback(this.$t('alerts.formError'), 'error');
      }
    },

    suffix(key) {
      if (this.suffixList.includes(key)) return 'mm';
      return '';
    },

    async editMatrix() {
      await this.$apollo
        .mutate({
          mutation: UPDATE_MATRIX,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            _id: this.items._id,
            description: this.fields2.description.value,
            name: this.fields2.name.value,
            part_number: this.fields2.part_number.value,
            origin: this.origin,
            slots: this.data.slots,
            subdivisions: this.data.subdivisions,
          },
        })

        .then(() => {
          // Result
          this.$emit('refetch');
          this.$alertFeedback(this.$t('alerts.updateMatrixSuccess'), 'success');
        })

        .catch((error) => {
          console.log(error.graphQLErrors);
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
.edit-matrix {
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

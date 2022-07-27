<!-- eslint-disable vue/no-parsing-error -->
/* eslint-disable no-underscore-dangle */
<template>
  <!-- <v-card class="mb-4" min-height="100px" outlined> -->
  <div>
    <div class="d-flex align-center p-4" v-if="obj">
      <div>
        <div class="d-flex align-center">
          <div class="viewer">
            <matrix-viewer
              edit="distTotalX"
              v-if="obj.slots"
              :slots="obj.slots"
              :subdivisions="obj.subdivisions"
            ></matrix-viewer>
          </div>
          <div class="pl-4 pr-4">
            <span class="text-h6 text-capitalize font-weight-bold">{{
              obj.name
            }}</span>
            <div class="text-subtitle-2">{{ obj.description }}</div>
            <div class="font-weight-bold d-flex align-center">
              <div class="text-body-2 mr-1">{{ $t('form.partNumberAb') }}:</div>
              {{ obj.part_number }}
            </div>
            <div class="font-weight-bold d-flex align-center">
              <div class="text-body-2 mr-1">{{ $t('form.variable') }}:</div>
              <v-chip
                class="mr-2"
                small
                v-for="(item, index) in obj.variable"
                :key="index"
              >
                {{ item.name }}</v-chip
              >
            </div>
            <!-- <div class="font-weight-bold d-flex align-center">
              <div class="text-body-2 mr-1">color:</div>
              {{ obj.color_name }}
            </div> -->
            <!-- <div class="text-body-2">
            {{ $timestampToDate(obj.date) }}
          </div> -->
          </div>
        </div>
      </div>
      <v-spacer></v-spacer>
      <div class="d-flex">
        <v-btn class="mr-5" icon @click="show = !show"
          ><v-icon>{{
            show ? 'mdi-chevron-up' : 'mdi-chevron-down'
          }}</v-icon></v-btn
        >
        <dialog-confirmation
          v-if="dialogDelete"
          @confirm-event="remove"
          @cancel-event="dialogDelete = false"
        ></dialog-confirmation>
        <div>
          <v-menu transition="slide-x-transition" bottom left offset-x>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                class="list-item"
                v-for="(item, index) in items"
                :key="index"
                link
                @click="item.function()"
              >
                <v-list-item-title
                  ><v-icon small class="mr-5">mdi-{{ item.btnIcon }}</v-icon
                  >{{ $t(item.title) }}
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </div>
    </div>
    <v-expand-transition>
      <div v-show="show">
        <!-- <v-divider></v-divider> -->
        <v-card-text>
          <v-data-table
            :headers="headers"
            :items="detailItems"
            hide-default-header
            hide-default-footer
          >
            <template v-slot:item.field="{ item }">
              <div class="font-weight-bold">
                {{ item.field }}
                <!-- {{typeof item.value}} -->
              </div>
            </template>
            <template v-slot:item.value="{ item }">
              <div   v-if="typeof item.value === 'object'" >
                <div
                  v-for="(sub, index) in Object.entries(item.value)"
                  :key="index"
                >
                  <div class="font-weight-bold d-flex">
                    {{ sub[0] }}:
                    <div>
                      &nbsp X:<span class="font-weight-regular">{{
                        sub[1].x
                      }}</span>
                      Y:<span class="font-weight-regular">{{ sub[1].y }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else>{{item.value}}</div>
            </template> </v-data-table
        ></v-card-text>
        <v-divider></v-divider>
      </div>
    </v-expand-transition>
  </div>
  <!-- </v-card> -->
</template>

<script>
import { mapActions } from 'vuex';
import DialogConfirmation from '@/components/settings/DialogConfirmation.vue';
import MatrixViewer from '../../node/nodes/matrix/MatrixViewer.vue';

export default {
  components: { DialogConfirmation, MatrixViewer },
  props: {
    obj: Object,
  },
  data() {
    return {
      show: false,
      dialogDelete: false,
      headers: [
        {
          text: 'field',
          value: 'field',
        },
        {
          text: 'value',
          value: 'value',
        },
      ],
      items: [
        {
          title: 'buttons.edit',
          btnIcon: 'pencil',
          function: this.edit,
        },
        {
          title: 'buttons.remove',
          btnIcon: 'delete',
          function: this.dialog,
        },
        {
          title: 'buttons.duplicate',
          btnIcon: 'content-duplicate',
          function: this.duplicate,
        },
      ],
    };
  },

  computed: {
    detailItems() {
      return [
        {
          field: this.$t('form.origin'),
          value: `x:${this.obj.origin.x}   y:${this.obj.origin.y}`,
        },
        {
          field: this.$t('form.supplier'),
          value: this.obj.supplier,
        },
        {
          field: this.$t('form.slots'),
          value: this.obj.slots,
        },
        {
          field: this.$t('form.subdivisions'),
          value: this.obj.subdivisions,
        },
      ];
    },
  },

  methods: {
    ...mapActions({
      updateUser: 'auth/updateUser',
    }),

    getInitials() {
      return this.user?.name?.charAt(0);
    },

    remove() {
      // eslint-disable-next-line no-underscore-dangle
      this.$emit('remove', this.obj._id);
      this.dialogDelete = false;
    },

    edit() {
      this.$emit('edit', this.obj);
    },

    duplicate() {
      this.$emit('duplicate', this.obj._id);
      console.log('duplicate');
    },

    dialog() {
      this.dialogDelete = true;
    },
  },
};
</script>

<style>
.viewer {
  width: 200px;
  /* width: 150px;
  height: 150px; */
}
</style>

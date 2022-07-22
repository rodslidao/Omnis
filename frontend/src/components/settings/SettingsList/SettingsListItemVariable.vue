/* eslint-disable no-underscore-dangle */
<template>
  <div>
    <div class="d-flex align-center p-2" v-if="obj">
      <div>
        <div class="d-flex align-center">
          <div class="pl-4 pr-4">
            <span class="text-subtitle text-capitalize font-weight-bold">{{
              obj.name
            }}</span>
          </div>
        </div>
      </div>
      <v-spacer></v-spacer>
      <div class="d-flex">
        <dialog-confirmation
          v-if="dialogDelete"
          :del="$t('settings.objs.obj')"
          @confirm-event="remove"
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
  </div>
  <!-- </v-card> -->
</template>

<script>
import { mapActions } from 'vuex';
import DialogConfirmation from '@/components/settings/DialogConfirmation.vue';

export default {
  components: { DialogConfirmation },
  props: {
    obj: Object,
  },
  data() {
    return {
      dialogDelete: false,
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
      ],
    };
  },

  methods: {
    ...mapActions({
      updateUser: 'auth/updateUser',
    }),

    remove() {
      // eslint-disable-next-line no-underscore-dangle
      this.$emit('remove', this.obj._id);
      this.dialogDelete = false;
    },

    edit() {
      this.$emit('edit', this.obj);
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

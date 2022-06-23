<template>
  <!-- <v-card class="mb-4" min-height="100px" outlined> -->
  <div class="d-flex align-center p-4">
    <div>
      <div class="d-flex">
        <v-avatar color="primary" size="50">
          <img v-if="user.avatar_image" :src="user.avatar_image" />
          <span v-else class="text-capitalize"
            >{{ user.first_name.charAt(0)
            }}{{ user.last_name.split(' ')[0].charAt(0) }}</span
          >
        </v-avatar>
        <div class="pl-4 pr-4">
          <div class="text-h6 mb-1">
            {{ user.first_name }} {{ user.last_name }}
          </div>
          <div class="text-body-2">
            {{ user.username }} <span class="mx-2">|</span> {{ user.email }}
          </div>
          <div class="text-body-2">
            {{ $timestampToDate(user.last_access) }}
          </div>
        </div>
      </div>
    </div>
    <v-spacer></v-spacer>
    <div class="d-flex">
      <dialog-confirmation
        :visible="dialogDelete"
        :del="$t('settings.users.user')"
        @confirm-event="remove"
      ></dialog-confirmation>
      <v-chip class="mr-4">
        {{ user.level }}
      </v-chip>
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
            >
              <v-list-item-title @click="item.function()"
                ><v-icon small class="mr-5">mdi-{{ item.btnIcon }}</v-icon
                >{{ $t(item.title) }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>
  </div>
  <!-- </v-card> -->
</template>

<script>
import DialogConfirmation from '@/components/settings/DialogConfirmation.vue';

export default {
  components: { DialogConfirmation },
  props: {
    user: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      select: null,
      show: false,
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
    change(value) {
      // this.$emit('selected', value);
      this.$emit('update:selected', this.$event.target.checked);
    },
    dialog() {
      this.dialogDelete = true;
    },
    edit() {
      console.log('edit');
    },
    remove() {
      console.log('deletado');
      this.dialogDelete = false;
    },
  },
};
</script>

<style>
</style>
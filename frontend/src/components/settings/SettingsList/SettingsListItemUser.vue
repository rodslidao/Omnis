/* eslint-disable no-underscore-dangle */
<template>
  <!-- <v-card class="mb-4" min-height="100px" outlined> -->
  <div class="d-flex align-center p-4" v-if="user">
    <div>
      <div class="d-flex align-center">
        <v-avatar color="primary" size="50">
          <img v-if="user.avatar_image" :src="user.avatar_image" />
          <span v-else class="text-uppercase"
            >{{getInitials()}}</span
          >
        </v-avatar>
        <div class="pl-4 pr-4">
          <div class="text-h6 font-weight-bold mb-1">
            <span class="text-capitalize ">{{ user.first_name }}</span>
            {{ user.last_name }}
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
        v-if="dialogDelete"
        :del="$t('settings.users.user')"
        @confirm-event="remove"
      ></dialog-confirmation>
      <v-chip class="mr-4">
        {{ $t('levels.' + user.level) }}
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
// import gql from 'graphql-tag';
import { mapActions } from 'vuex';
import DialogConfirmation from '@/components/settings/DialogConfirmation.vue';

// const REMOVE_USER = gql`
//   mutation ($_id: ID!) {
//     deleteUser(_id: $_id)
//   }
// `;

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
    ...mapActions({
      updateUser: 'auth/updateUser',
    }),

    getInitials() {
      return (
        this.user?.first_name?.charAt(0)
        + this.user?.last_name?.split(' ').at(-1).charAt(0)
      );
    },

    remove() {
      this.$emit('remove-user', this.user._id);
      this.dialogDelete = false;
    },

    edit() {
      this.$emit('edit-user', this.user);
    },

    dialog() {
      this.dialogDelete = true;
    },
  },
};
</script>

<style>
</style>

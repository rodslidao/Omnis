<template>
  <div class="pt-6 d-flex settings">
    <!-- <v-card elevation="12" width="256"> -->
    <v-navigation-drawer
      expand-on-hover
      floating
      permanent
      mini-variant-width="62"
      width="300"
      class="navigation"
      color="rgba(0,0,0,0)"
    >
      <div v-if="isAuth" class="user ml-1 mr-4">
        <v-avatar color="primary" size="40" v-if="user">
          <img v-if="user.avatar_image" :src="user.avatar_image" />
          <span v-else class="text-capitalize">{{ getInitials }}</span>
        </v-avatar>
        <div class="ml-4">
          <div
            class="text-subtitle font-weight-bold text-capitalize complete-name"
          >
            {{ nameComplete }}
          </div>
          <div class="text-subtitle-2">{{ $t('levels.' + user.level) }}</div>
        </div>
      </div>

      <!-- <v-autocomplete
        v-model="select"
        :items="items"
        cache-items
        item-text="title"
        class="mx-4 mb-4"
        rounded
        filled
        dense
        prepend-inner-icon="mdi-magnify"
        hide-no-data
        hide-details
        placeholder="Pesquisar"
      ></v-autocomplete> -->
      <v-list dense rounded nav>
        <v-list-item-group
          v-model="group"
          active-class="primary--text text--accent-4"
        >
          <v-list-item
            v-for="item in items.filter((i)=>  $access(i.path))"
            :key="item.title"
            link
            :to="'/config' + item.path"
          >
            <v-list-item-icon>
              <v-icon>mdi-{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ $t(item.title) }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <!-- </v-card> -->
    <div class="pl-14 pr-2 setting-warper">
      <breadcrumb-settings></breadcrumb-settings>
      <div class="setting-content">
        <router-view transition="fade-transition"></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import BreadcrumbSettings from '@/components/settings/BreadcrumbSettings.vue';
import { menuList } from '@/components/settings/menuDescription';

export default {
  components: { BreadcrumbSettings },

  // created() {
  //   this.$router.push({ name: 'system' }).catch(() => {});
  // },

  data() {
    return {
      userLogged: false,
      group: null,
      search: null,
      select: null,
      items: menuList,
    };
  },

  computed: {
    ...mapGetters({
      user: 'auth/user',
      isAuth: 'auth/isAuth',
    }),

    getInitials() {
      return (
        this.user?.first_name?.charAt(0) +
        this.user?.last_name?.split(' ').at(-1).charAt(0)
      );
    },

    nameComplete() {
      return `${this.user?.first_name} ${this.user?.last_name
        ?.split(' ')
        .at(-1)
        .charAt(0)}.`;
    },
  },

  watch: {
    group() {
      this.drawer = false;
    },
  },
};
</script>
<style scoped>
.user {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 2rem;
  margin-top: 1rem;
}

.complete-name {
  display: inline-block;
  white-space: nowrap;
}

.settings {
  height: 100%;
  background-color: rgb(253, 253, 253);
}
.setting-warper {
  width: 100%;
}

.setting-content {
  width: 100%;
  /* max-width: 900px; */
  height: 100%;
  overflow: auto;
  margin: 0;
  /* padding: 0.5rem; */
  height: calc(100vh - 12rem);
}
</style>

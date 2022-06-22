<template>
  <div class="pt-10 d-flex settings">
    <!-- <v-card elevation="12" width="256"> -->
    <v-navigation-drawer
      floating
      permanent
      width="300"
      class="navigation"
      color="rgba(0,0,0,0)"
    >
      <div class="user mx-4">
        <v-avatar color="primary" size="50">
          <img v-if="user.avatar" :src="user.avatar" />
          <span v-else
            >{{ user.name.charAt(0)
            }}{{ user.name.split(' ')[1].charAt(0) }}</span
          >
        </v-avatar>
        <div class="ml-4">
          <div class="text-subtitle font-weight-bold">
            {{
              `${user.name.split(' ')[0]} ${user.name.split(' ')[1].charAt(0)}.`
            }}
          </div>
          <div class="text-subtitle-2">{{ user.level.title }}</div>
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
      <v-list dense rounded>
        <v-list-item-group
          v-model="group"
          active-class="primary--text text--accent-4"
        >
          <v-list-item
            v-for="item in items"
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
import BreadcrumbSettings from '@/components/settings/BreadcrumbSettings.vue';
import { menuList } from '@/components/settings/menuDescription';

export default {
  components: { BreadcrumbSettings },

  created() {
    this.$router.push({ name: 'system' });
  },

  data() {
    return {
      userLogged: false,
      user: {
        level: {
          title: 'Administrador',
          type: 'admin',
        },
        name: 'Rodrigo Gomes',
        avatar: 'https://i.pravatar.cc/50',
      },
      group: null,
      search: null,
      select: null,
      items: menuList,
    };
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
}

.settings {
  height: 100%;
  background-color: rgb(253, 253, 253);
}
.setting-warper{
  width: 100%;
}

.setting-content {
  width: 100%;
  max-width: 900px;
  height: 100%;
  overflow: auto;
  margin: 0;
  /* padding: 0.5rem; */
  height: calc(100vh - 12rem);
}
</style>

<template>
  <div class="pt-10">
    <!-- <v-card elevation="12" width="256"> -->
    <v-navigation-drawer floating permanent>
      <div class="user mx-4">
        <v-avatar color="primary" size="50">
          <img v-if="user.avatar" :src="user.avatar" />
          <span v-else>{{ user.name.charAt(0) }}{{user.name.split(' ')[1].charAt(0) }}</span>
        </v-avatar>
        <div class="ml-4">
          <div class="text-h5">{{ user.name }}</div>
          <div class="text-subtitle">{{ user.level.title }}</div>
        </div>
      </div>

      <v-autocomplete
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
      ></v-autocomplete>
      <v-list dense rounded>
        <v-list-item-group
          v-model="group"
          active-class="primary--text text--accent-4"
        >
          <v-list-item v-for="item in items" :key="item.title" link>
            <v-list-item-icon>
              <v-icon>mdi-{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <!-- </v-card> -->

  </div>
</template>

<script>
export default {
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
      items: [
        { title: 'Sistema', icon: 'application' },
        { title: 'Dispositivos', icon: 'devices' },
        { title: 'Rede & Internet ', icon: 'wifi' },
        { title: 'Suporte', icon: 'handshake-outline' },
      ],
    };
  },
  watch: {
    group() {
      this.drawer = false;
    },
  },
};
</script>
<style lang="scss" scoped>
.user {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 2rem;
}
</style>

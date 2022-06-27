<template>
  <div class="process">
    <router-view> </router-view>
    <settings-items
      v-for="(item, index) in items"
      :key="index"
      :title="item.title"
      :subtitle="item.subtitle"
      :icon="item.icon"
      divider-list
    >
      <template v-slot:expand>
        <div v-for="(subItem, index) in item.subItens" :key="index">
          <div class="d-flex">
            <div class="text-h6">{{subItem.title}}</div>
            <v-spacer></v-spacer>
            <v-btn icon><v-icon>mdi-chevron-right</v-icon></v-btn>
          </div>
        </div>
      </template>
    </settings-items>
  </div>
</template>

<script>
import SettingsItems from '../../components/settings/SettingsItems.vue';
import SettingsTitle from '../../components/settings/SettingsTitle.vue';

export default {
  components: { SettingsItems, SettingsTitle },
  data() {
    return {
      actualPath: '',
      items: [
        {
          title: 'Nós',
          subtitle: 'Gerência seus nós',
          // icon: 'application-brackets',
          icon: 'application',
          path: '/node',
        },
        {
          title: 'Matriz',
          subtitle: 'Crie novas matrizes',
          // icon: 'application-brackets',
          icon: 'grid',
          path: 'process/matrix',
          subItens: [
            { title: 'Cadastrar', path: 'process/matrix-add' },
            { title: 'Listar', path: 'process/matrix-list' },
          ],
        },
        {
          title: 'Objects',
          subtitle: 'Gerência seus processos',
          icon: 'cog',
          path: 'process/process',
        },
      ],
    };
  },

  // created() {
  //   this.actualPath = this.$router.currentRoute.path;
  //   console.log(this.$router.currentRoute);
  // },
};
</script>

<style lang="scss" scoped>
</style>

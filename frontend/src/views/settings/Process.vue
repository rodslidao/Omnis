<template>
  <div class="process">
    <router-view> </router-view>
    <settings-items
      class="mb-4"
      v-for="(item, index) in items"
      :key="index"
      :title="item.title"
      :subtitle="item.subtitle"
      :icon="item.icon"
      :path="item.path"
    ></settings-items>
  </div>
</template>

<script>
import SettingsItems from '../../components/settings/SettingsItems.vue';

export default {
  components: { SettingsItems },
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
        },
        {
          title: 'Processos',
          subtitle: 'Gerência seus processos',
          icon: 'cog',
          path: 'process/process',
        },
      ],
    };
  },

  created() {
    this.actualPath = this.$router.currentRoute.path;
    console.log(this.$router.currentRoute);
  },
};
</script>

<style lang="scss" scoped>
</style>

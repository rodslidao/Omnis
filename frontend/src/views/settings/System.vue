<template>
  <div class="system">
    <settings-title>Idioma e Data</settings-title>
    <router-view> </router-view>
    <settings-items
      class="mb-4"
      v-for="(item, index) in items"
      :key="index"
      :title="item.title"
      :subtitle="item.subtitle"
      :icon="item.icon"
      :path="item.path"
      :select="item.select"
      @selected="changeLanguage"
    ></settings-items>
    {{ items[0].selected }}
  </div>
</template>

<script>
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';

export default {
  components: { SettingsItems, SettingsTitle },
  data() {
    const lang = localStorage.getItem(lang || 'pt-br');
    return {
      actualPath: '',
      items: [
        {
          title: 'Idioma de exibição',
          subtitle:
            'O idioma de todo o programa será exibida no idioma selecionado',
          icon: 'web',
          path: '',
          select: ['pt-BR', 'en-US'],
        },
      ],
    };
  },

  created() {
    this.actualPath = this.$router.currentRoute.path;
    console.log(this.$router.currentRoute);
  },

  methods: {
    changeLanguage(language) {
      console.log(language);
      localStorage.setItem('lang', language);
      // window.location.reload();
      // this.$store.commit('setLanguage', language);
    },
  },
};
</script>

<style lang="scss" scoped>
.system {
  overflow: auto;
  padding: 0.5rem;
  height: calc(100vh - 12rem);
}
</style>

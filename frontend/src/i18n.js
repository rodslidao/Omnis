import pt from '@/assets/i18n/pt.json';
import en from '@/assets/i18n/en.json';
import VueI18n from 'vue-i18n';
import Vue from 'vue';

Vue.use(VueI18n);

export default new VueI18n({
  lazy:true,
  locale: localStorage.getItem('lang') || navigator.language || navigator.userLanguage || 'en',
  messages: {
    "pt":pt,
    "pt-BR":pt,
    "en":en,
  },
});

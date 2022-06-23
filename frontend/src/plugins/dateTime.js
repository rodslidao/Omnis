export default {
  // The install method will be called with the Vue constructor as the first argument,
  // along with possible options

  install(Vue, options) {
    // ES6 way of const job = options.job
    // Add $plugin instance method directly to Vue components
    Vue.prototype.$timestampToDate = (_timestamp) => {
      const d = new Date(_timestamp * 1000);
      const data = {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: true,
      };

      return new Intl.DateTimeFormat('pt-BR', data).format(d);
    };

    // Add $surname instance property directly to Vue components
    // Vue.prototype.$surname = 'Smith';
  },
};

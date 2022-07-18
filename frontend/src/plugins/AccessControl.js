/* eslint-disable no-param-reassign */
// best example
// https://gist.github.com/nkoik/0f1beb1f757d3e0c79ad0b76c11e1a80

export default {
  // The install method will be called with the Vue constructor as the first argument,
  // along with possible options

  install(Vue, options) {
    // ES6 way of const job = options.job
    // Add $plugin instance method directly to Vue components
    Vue.prototype.$access = (_componentName) => {
      const { level } = options.store.getters['auth/user'];
      const logged_access = options.store.getters['auth/levelsRules'].filter((item) => item.name === level);
      if (!logged_access[0]?.forbidden_list?.includes(_componentName)) {
        return true;
      }
      return false;
    };
  },
};

/* eslint-disable no-param-reassign */
// best example
// https://gist.github.com/nkoik/0f1beb1f757d3e0c79ad0b76c11e1a80

export default {
  // The install method will be called with the Vue constructor as the first argument,
  // along with possible options

  install(Vue, options) {
    // ES6 way of const job = options.job
    // Add $plugin instance method directly to Vue components
    Vue.prototype.$alertFeedback = (_description, _type, _moreInfo) => {
      options.store.dispatch(
        'alert/addItemList',
        { description: _description, type: _type, moreInfo: _moreInfo },
        { root: true },
      );
    };

    // Add $surname instance property directly to Vue components
    Vue.prototype.$surname = 'Smith';
  },
};

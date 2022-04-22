/* eslint-disable no-underscore-dangle */
export default {
  namespaced: true,
  state: {
    alertList: [
      // {
      //   description: String,
      //   type: String,
      //   moreInfo: String,
      // },
    ],
  },
  // link og beautiful dogs https://www.youtube.com/watch?v=dQw4w9WgXcQ
  mutations: {
    addItemList: (state, item) => {
      state.alertList.push(item);
    },
    removeItemList: (state) => {
      state.alertList.pop();
    },
  },

  actions: {
    addItemList({ commit }, payload) {
      commit('addItemList', payload);
    },
    removeItemList({ commit }, payload) {
      commit('removeItemList', payload);
    },
  },
};

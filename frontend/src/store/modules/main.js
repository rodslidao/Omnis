/* eslint-disable no-underscore-dangle */
export default {
  namespaced: true,
  state: {
    alertList: [
      { description: 'Meteu essa pai?', type: 'success' },
      { description: 'Does it decay? That is, as people read a long sentence, their reading speed increases?', type: 'info' },
      { description: 'What I would like to do is to calculate the optimal time to show each message based off of the number of characters in that message. I want users to have enough time to comfortably read the message, but not so long that the message impedes their usage of the app.?', type: 'warning' },
    ],
  },
  mutations: {
    addItemList: (state, item) => {
      state.alertList.push(item);
    },
  },

  actions: {
    addItemList({ commit }, payload) {
      commit('addItemList', payload);
    },
  },
};

/* eslint-disable no-underscore-dangle */
export default {
  namespaced: true,
  state: {
    counter: 0,
    tabList: [
      { sketchName: 'One', id: 1641587087905, saved: true },
      { sketchName: 'two', id: 1641587087905, saved: true },
      { sketchName: 'tree', id: 1641587087905, saved: true },
    ],
    runningTabId: 1641587087905,
    selectedTabId: 1641587087905,
    // http://192.168.1.31:5000/video_feed/camera0
    connection: {
      ip: '192.168.1.31',
      portStream: 5000,
    },
    selectedTab: null,
  },

  getters: {
    /**
     * access counter in state from the parameter
     */

    // eslint-disable-next-line max-len
    SelectedTabName: (state) => {
      state.tabList.find(((tab) => tab.id === state.selectedTabId).sketchName);
    },
    selectedTabObject: (state) => state.tabList.find((tab) => tab.id === state.selectedTabId),
    addCurrencyToCounter: (state) => `$ ${state.counter} (dollars)`,
    incrementCounterByTen: (state) => state.counter + 10,
  },

  mutations: {
    SOCKET_RESPONSE_MESSAGE: (state, message) => {
      console.log('%c Recebido:', 'color: #51a4f7');
      console.log(message);
      // state.commit('TOGGLE_LOADING', null, { root: true })
    },

    play: (state) => {
      state.runningTabId = state.selectedTabId;
    },

    addTab: (state, tab) => {
      state.tabList.push(tab);
    },

    removeTabById: (state, id) => {
      state.tabList = state.tabList.filter((tab) => tab.id !== id);
    },

    removeTabByIndex: (state, index) => {
      state.tabList.splice(index, 1);
    },

    updateTabById: (state, tab) => {
      const index = state.tabList.findIndex((t) => t.id === tab.id);
      state.tabList.splice(index, 1, tab);
    },

    selectTabByIndex: (state, index) => {
      // find id of tab at index
      const tabId = state.tabList[index].id;
      state.selectedTabId = tabId;
    },

    updateSelectedTab: (state, tab) => {
      state.selectedTab = tab;
    },

    asyncIncrement: (state, incrementalObject) => {
      const { incrementalValue } = incrementalObject;
      state.counter += incrementalValue;
    },
  },

  actions: {
    /**
     * destruct the context, get the commit and call on the appropriate mutation
     */
    play({ commit }) {
      commit('play');
    },

    addTab({ commit }, payload) {
      this._vm.$socket.emit('node', payload);
      commit('addTab', payload);
    },

    removeTabById({ commit }, payload) {
      commit('removeTabById', payload);
    },

    removeTabByIndex({ commit }, payload) {
      commit('removeTabByIndex', payload);
    },

    selectTabByIndex({ commit }, payload) {
      commit('selectTabByIndex', payload);
    },

    updateTabById({ commit }, payload) {
      commit('updateTabById', payload);
    },

    updateSelectedTab({ commit }, payload) {
      commit('updateSelectedTab', payload);
    },

    /**
     * demonstrate an async task
     */
    asyncIncrement({ commit }, incrementalObject) {
      setTimeout(() => {
        /**
         * am done, kindly call appropriate mutation
         */
        commit('asyncIncrement', incrementalObject);
      }, 3000);
    },
  },
};

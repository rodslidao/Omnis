/* eslint-disable no-underscore-dangle */
// import { Editor } from '@baklavajs/core';
import { Editor } from '@baklavajs/core';
import Vue from 'vue';

export default {
  namespaced: true,
  state: {
    editor: new Editor(),
    counter: 0,
    tabList: [
      // {
      //   name: 'two',
      //   id: 1641587087910,
      //   saved: true,
      //   content: {},
      // },
      // {
      //   name: 'tree',
      //   id: 1641587087911,
      //   saved: true,
      //   content: {},
      // },
    ],
    runningTabId: null,
    selectedTabId: null,
    // http://192.168.1.31:5000/video_feed/camera0
    selectedTabIndex: 0,
    contentDefault: {},
    renamingIndex: null,
    saveNode: null,
    deletedNode: null,
  },

  getters: {
    /**
     * access counter in state from the parameterr
     */

    // eslint-disable-next-line max-len
    SelectedTabName: (state) => {
      state.tabList.find(((tab) => tab.id === state.selectedTabId).name);
    },
    selectedTabObject: (state) => state.tabList.find((tab) => tab.id === state.selectedTabId),
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
      console.log('%c Tab Adicionada:', 'color: #51a4f7', tab);
    },

    duplicateTab: (state, payload) => {
      // state.duplicatedTab.isDuplicated = true;

      const indexOfNewTab = payload.indexContextMenu + 1;
      // state.duplicatedTab.newTabIndex = indexOfNewTab;
      const contextTab = state.tabList[payload.indexContextMenu];
      // state.duplicatedTab.contextTabIndex = contextTab;
      state.tabList.splice(indexOfNewTab, 0, payload.tab);
      const newTab = state.tabList[indexOfNewTab];
      newTab.name = `${contextTab.name} - Cópia`;
      // newTab.baklavaEditor = contextTab.baklavaEditor;
      // state.selectedTabIndex = indexOfNewTab;
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
      state.selectedTabIndex = tab;
    },

    updateNodeContent: (state, payload) => {
      const itemSelected = state.tabList[payload.index];
      if (itemSelected) {
        if (payload.index < state.tabList.length) {
          itemSelected.content = payload.content;
        }
        console.log(payload);
        if (itemSelected.duplicated) {
          itemSelected.duplicated = payload.duplicated;
        }
      }
    },

    updateContentDefault: (state, content) => {
      state.contentDefault = content;
    },

    setRenamingIndex: (state, index) => {
      state.renamingIndex = index;
    },

    setSketchName: (state, payload) => {
      state.tabList[payload.index].name = payload.name;
    },

    setSaved: (state, { index, value }) => {
      state.tabList[index].saved = value;
      console.log(state.tabList[index].saved);
    },

    asyncIncrement: (state, incrementalObject) => {
      const { incrementalValue } = incrementalObject;
      state.counter += incrementalValue;
    },
    saveNodeConfig: (state, node) => {
      state.saveNode = node;
    },
    deletedNode: (state, node) => {
      state.deletedNode = node;
      console.log('state', state.deletedNode);
    },
    loadTabId: (state, data) => {
      console.log('LoadTab', data);

      let equalTabIndex = 0;

      const equalTab = state.tabList.find((tab, index) => {
        equalTabIndex = index;
        console.log('tab', tab);
        return tab._id === data._id && tab.last_modified === data.last_modified;
      });

      console.log('existTab', equalTab);
      console.log('existTabIndex', equalTabIndex);

      if (equalTab) {
        state.selectedTabIndex = equalTabIndex;
        state.selectedTabId = equalTab._id;
        Vue.prototype.$alertFeedback('Este arquivo ja estava aberto', 'success');
      } else {
        console.log('não existe uma tab igual');
        const newLoadTab = {
          _id: data._id,
          name: data.name,
          parent_id: data.parent_id,
          description: data.description,
          author: data.author,
          last_access: data.date,
          saved: true,
          content: data.content,
        };

        state.tabList.push(newLoadTab);
        state.selectedTabIndex += 1;

        state.selectedTabId = data._id;
        Vue.prototype.$alertFeedback('Arquivo carregado com sucesso', 'success');
      }
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
      commit('addTab', payload);
    },

    duplicateTab({ commit }, payload) {
      commit('duplicateTab', payload);
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

    updateNodeContent({ commit }, payload) {
      commit('updateNodeContent', payload);
    },

    updateContentDefault({ commit }, payload) {
      commit('updateContentDefault', payload);
    },
    setRenamingIndex({ commit }, payload) {
      commit('setRenamingIndex', payload);
    },
    setSketchName({ commit }, payload) {
      commit('setSketchName', payload);
    },
    setSaved({ commit }, payload) {
      commit('setSaved', payload);
    },
    saveNodeConfig({ commit }, payload) {
      commit('saveNodeConfig', payload);
    },
    deletedNode({ commit }, payload) {
      commit('deletedNode', payload);
    },
    loadTabId({ commit }, payload) {
      commit('loadTabId', payload);
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

/* eslint-disable no-underscore-dangle */
import { Editor } from '@baklavajs/core';

export default {
  namespaced: true,
  state: {
    counter: 0,
    tabList: [
      // {
      //   sketchName: 'two',
      //   id: 1641587087910,
      //   saved: true,
      //   content: {},
      // },
      // {
      //   sketchName: 'tree',
      //   id: 1641587087911,
      //   saved: true,
      //   content: {},
      // },
    ],
    runningTabId: 1641587087905,
    selectedTabId: 1641587087905,
    // http://192.168.1.31:5000/video_feed/camera0
    connection: {
      ip: '192.168.1.31',
      portStream: 5000,
    },
    selectedTabIndex: 0,
    contentDefault: {},
    renamingIndex: null,
  },

  getters: {
    /**
     * access counter in state from the parameterr
     */

    // eslint-disable-next-line max-len
    SelectedTabName: (state) => {
      state.tabList.find(((tab) => tab.id === state.selectedTabId).sketchName);
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
    },

    duplicateTab: (state, payload) => {
      // state.duplicatedTab.isDuplicated = true;

      const indexOfNewTab = payload.indexContextMenu + 1;
      // state.duplicatedTab.newTabIndex = indexOfNewTab;
      const contextTab = state.tabList[payload.indexContextMenu];
      // state.duplicatedTab.contextTabIndex = contextTab;
      state.tabList.splice(indexOfNewTab, 0, payload.tab);
      const newTab = state.tabList[indexOfNewTab];
      newTab.sketchName = `${contextTab.sketchName} - Cópia`;
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
      state.tabList[payload.index].sketchName = payload.sketchName;
    },

    setSaved: (state, { index, value }) => {
      state.tabList[index].saved = value;
      console.log(state.tabList[index].saved);
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

/* eslint-disable no-console */
/* eslint-disable no-underscore-dangle */
// import { Editor } from '@baklavajs/core';
import { Editor } from '@baklavajs/core';
import { Engine } from '@baklavajs/plugin-engine';
import Vue from 'vue';

const ObjectID = require('bson-objectid');

export default {
  namespaced: true,
  state: {
    editor: new Editor(),
    engine: new Engine(false),
    counter: 0,
    newTab: {
      label: '',
      _id: null,
      key: null,
      description: 'Descrição',
      author: 'Autor',
      last_access: new Date().getTime(),
      parent_id: null,
      version: 1,
      saved: false,
      duplicated: false,
      content: {},
    },
    tabList: [],
    newTabCounter: 0,
    loadedFileTrigger: false,
    selectedTab: null,
    contentDefault: {},

    // não usados ainda
    runningTabId: null,
    selectedTabKey: null,
    renamingIndex: null,
    saveNode: null,
    deletedNode: null,
  },

  getters: {
    /**
     * access counter in state from the parameterr
     */
    selectedTabKey: (state) => state.selectedTab.key,

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

    addNewTab: (state) => {
      console.log('addNewTab');
      const idGenerated = ObjectID().toHexString();

      let tabSketchName = `Aba ${state.newTabCounter}`;
      if (state.newTab.length === 0) tabSketchName = 'Aba 1';
      state.newTabCounter += 1;

      state.newTab._id = idGenerated;
      state.newTab.key = idGenerated;
      state.newTab.parent_id = idGenerated;
      state.newTab.label = tabSketchName;
      state.newTab.content = state.contentDefault;

      // if (state.newTab.content.nodes) {
      //   console.log('old', state.newTab.content.nodes[0].id);
      //   state.newTab.content.nodes[0].id = `node_${state.editor.generateId()}`;
      //   console.log('new', state.newTab.content.nodes[0].id);
      // }

      state.selectedTab = { ...state.newTab };

      console.log('%c Tab Adicionada:', 'color: #51a4f7', state.newTab);
      console.log('%c Tab List:', 'color: #51a4f7', state.tabList);
    },

    updateSelectedTab: (state, selectedTabKey) => {
      console.log('selected tabbbb', state.selectedTab.key);
      const newKey = selectedTabKey[0];
      const oldKey = selectedTabKey[1];

      // state.selectedTab.content = state.editor.save();
      const foundOldIndex = state.tabList.findIndex((tab) => tab.key === oldKey);
      // console.log('%c foundOldIndex:', 'color: #51a4f7', foundOldIndex);

      if (foundOldIndex !== -1 && state.tabList.length > 0) {
        console.log('salva');
        if (oldKey) state.tabList[foundOldIndex].content = state.editor.save();
      }

      const foundNewIndex = state.tabList.findIndex((tab) => tab.key === newKey);

      console.log('antiga', foundOldIndex);
      console.log('atual', foundNewIndex);
      console.log('%c Tab List:', 'color: #51a4f7', state.tabList);

      if (state.tabList.length === 1) {
        state.tabList[0].closable = false;
      } else {
        state.tabList[0].closable = true;
      }

      if (foundNewIndex !== -1 && state.tabList.length > 0) {
        state.selectedTab = state.tabList[foundNewIndex];
        if (oldKey) state.editor.load(state.tabList[foundNewIndex].content);
      } else {
        const foundSelectedIndex = state.tabList.findIndex(
          (tab) => tab.key === state.selectedTab.key
        );
        console.log('%c foundSelectedIndex:', 'color: #11a4f7', foundSelectedIndex);
        console.log('%c foundSelectedIndex:', 'color: #11a4f7', state.tabList[foundSelectedIndex].content);
        state.editor.load(state.tabList[foundSelectedIndex].content);
      }

      // console.log('%c Tab Atualizada:', 'color: #51a4f7', state.selectedTab);
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

    removeTabByKey: (state, payload) => {
      state.tabList = state.tabList.filter((tab) => tab.id !== payload);
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

    updateByProperty: (state, payload) => {
      console.log('updateByProperty', payload);
      const foundIndex = state.tabList.findIndex((tab) => tab.key === payload.key);

      // eslint-disable-next-line no-restricted-syntax, guard-for-in
      for (let prop in payload) {
        console.log(state.tabList[foundIndex][prop]);
        state.tabList[foundIndex][prop] = payload[prop];
      }

      // payload.forEach((element) => {
      //   console.log(element);
      //   state.tabList[foundIndex] = element[element];
      // });
    },

    updateContentDefault: (state, content) => {
      state.contentDefault = content;
    },

    setRenamingIndex: (state, index) => {
      state.renamingIndex = index;
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
        state.selectedTab = equalTab;
        Vue.prototype.$alertFeedback('Este arquivo ja estava aberto', 'success');
      } else {
        console.log('não existe uma tab igual');
        state.newTab._id = data._id;
        state.newTab.label = data.label;
        state.newTab.key = data._id;
        state.newTab.parent_id = data._id;
        state.newTab.description = data.description;
        state.newTab.author = data.author;
        state.newTab.last_access = data.date;
        state.newTab.saved = true;
        state.newTab.content = data.content;
        // const newLoadTab = {
        //   _id: data._id,
        //   label: data.label,
        //   parent_id: data.parent_id,
        //   description: data.description,
        //   author: data.author,
        //   last_access: data.date,
        //   saved: true,
        //   content: data.content,
        // };

        // state.tabList.push(newLoadTab);
        // state.selectedTabIndex += 1;
        // state.selectedTab = newLoadTab;

        state.loadedFileTrigger = !state.loadedFileTrigger;

        // state.selectedTabId = data._id;
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

    addNewTab({ commit }) {
      commit('addNewTab');
    },

    duplicateTab({ commit }, payload) {
      commit('duplicateTab', payload);
    },

    removeTabByKey({ commit }, payload) {
      commit('removeTabByKey', payload);
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
    updateByProperty({ commit }, payload) {
      commit('updateByProperty', payload);
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

export default {
    namespaced: true,
    state: {
        counter: 0,
        tabList: [
            { sketchName: "One", id: 1641587087905, saved: true },
        ],
        runningTabId: 1641587087905,
        selectedTabId: 1641587087905,
        // http://192.168.1.31:5000/video_feed/camera0
        connection: {
            ip: "192.168.1.41",
            portStream: 5000,
        },
    },

        getters: {
        /**
         * access counter in state from the paramater 
         */

        SelectedTabName: (state) => {
            return state.tabList.find(tab => tab.id === state.selectedTabId).sketchName;
        },

        selectedTabObject: (state) => {
            return state.tabList.find(tab => tab.id === state.selectedTabId);
        },


        addCurrencyToCounter: function (state) {
            return `$ ${state.counter} (dollars)`;
        },

        incrementCounterByTen: function (state) {
            return state.counter + 10;
        }

    },

    mutations: {
        play: state => state.runningTabId = state.selectedTabId,

        addTab: (state, tab) => {
            state.tabList.push(tab)
        },

        removeTabById: (state, id) => state.tabList = state.tabList.filter(tab => tab.id !== id),

        removeTabByIndex: (state, index) => {
            state.tabList.splice(index, 1)
        },

        updateTabById: (state, tab) => {
            const index = state.tabList.findIndex(t => t.id === tab.id);
            state.tabList.splice(index, 1, tab);
        },

        selectTabByIndex: (state, index) => {
            //find id of tab at index
            const tabId = state.tabList[index].id;
            state.selectedTabId = tabId
        },

        asyncIncrement: function (state, incrementalObject) {
            const { incrementalValue } = incrementalObject;
            state.counter += incrementalValue;
        }
    },

    actions: {
        /**
         * destruct the context, get the commit and call on the appropriate mutation
         */
        play: function ({ commit }) {
            commit('play')
        },

        addTab: function ({ commit }, payload) {
            commit('addTab', payload)
        },

        removeTabById: function ({ commit }, payload) {
            commit('removeTabById', payload)
        },

        removeTabByIndex: function ({ commit }, payload) {
            commit('removeTabByIndex', payload)
        },

        selectTabByIndex: function ({ commit }, payload) {
            commit('selectTabByIndex', payload)
        },

        updateTabById: function ({ commit }, payload) {
            commit('updateTabById', payload)
        },

        /**
         * demonstrate an async task
         */
        asyncIncrement: function ({ commit }, incrementalObject) {
            setTimeout(function () {
                /**
                 * am done, kindly call appropriate mutation
                 */
                commit('asyncIncrement', incrementalObject)
            }, 3000);
        }
    }
};
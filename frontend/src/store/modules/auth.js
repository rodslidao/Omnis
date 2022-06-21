import { REGISTER_USER, AUTHENTICATED_USER, AUTHENTICATE_USER } from '@/graphql';
import { apolloClient } from '@/vue-apollo';

const state = {
  user: {},
  authStatus: false,
  token: localStorage.getItem('apollo-token') || null,
};

const getters = {
  user: (state) => state.user,
  isAuth: (state) => !!state.token,
  authStatus: (state) => state.authStatus,
};

const actions = {
  async loginUser({ commit }, userData) {
    let {
      data: { authenticateUser },
    } = await apolloClient.query({
      mutation: AUTHENTICATE_USER,
      variables: userData,
    });
    commit('LOGIN_USER', authenticateUser);
    commit('SET_TOKEN', authenticateUser);

    // set token in localstorage
    localStorage.setItem('apollo-token', authenticateUser.token.split(' ')[1]);
  },

  // eslint-disable-next-line no-unused-vars
  async registerUser({ commit }, userData) {
    console.log(apolloClient);
    let {
      data: { registerUser },
    } = await apolloClient.mutate({
      mutation: REGISTER_USER,
      variables: userData,
    });
    // console.log('RESPONSE_APOLLO', resp);
    commit('LOGIN_USER', registerUser);
    commit('SET_TOKEN', registerUser);

    // set token in localstorage
    localStorage.setItem('apollo-token', registerUser.token.split(' ')[1]);
  },
  async getAuthUser({ commit }) {
    const {
      data: { authUserProfile },
    } = await apolloClient.query({
      query: AUTHENTICATED_USER,
    });
    commit('LOGIN_USER', { user: authUserProfile });
  },
};

const mutations = {
  LOGIN_USER(state, payload) {
    state.user = payload.user;
    state.authStatus = true;
  },
  SET_TOKEN(state, payload) {
    state.token = payload;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
  namespaced: true,
};

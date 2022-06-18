const state = {
    user:{},
    authStatus: false,
    token: localStorage.getItem('apollo-token') || null,
};

const getters = {
    user: state => state.user,
    isAuth: state => !!state.token,
    authStatus: state => state.authStatus,
};

const mutations = {};
const actions = {
    registerUser(context, userData){
        console.log("CONTEXT ", context)
        console.log("USER", userData);
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}
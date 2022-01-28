const dotenv = require("dotenv");
const path = require("path");

let envfile = ".env";
// if (process.env.NODE_ENV) {
//     envfile += "." + process.env.NODE_ENV;
// }

const result = dotenv.config({ 
    path: path.resolve(`../`, envfile)
});

// optional: check for errors
if (result.error) {
    throw result.error;
}

module.exports = {
  pwa: {
    name: 'Parallax',
    themeColor: '#0D1D2D',
    msTileColor: '#ffffff',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'white',
    appleMobileWebAppCache: 'yes',
    manifestOptions: {
      background_color: '#ffffff',
    },
  },

  transpileDependencies: [
    'vuetify',
  ],

};

// client/src/graphql/AllPhotos.js

import gql from 'graphql-tag'

export default gql`query allPhotos {
    allPhotos {
      filename
      path
    }
  }`
// client/src/graphql/UploadPhoto.js
import gql from 'graphql-tag';

export default gql`
  mutation uploadFile($file: Upload!) {
    uploadFile(file: $file) {
      filename
      path
    }
  }
`

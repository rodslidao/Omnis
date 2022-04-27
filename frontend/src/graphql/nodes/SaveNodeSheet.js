// client/src/graphql/UploadPhoto.js
import gql from 'graphql-tag';

export default gql`
  mutation saveNodeSheet(
    $id: ID!
    $name: String
    $saved: Boolean
    $duplicated: Boolean
    $content: JSON!
  ) {
    saveNodeSheet(
      _id: $id
      name: $name
      saved: $saved
      duplicated: $duplicated
      content: $content
    ) {
      data {
        _id
      }
    }
  }
`;

// client/src/graphql/UploadPhoto.js
import gql from 'graphql-tag';

export default gql`
  mutation saveNodeSheet(
    $_id: ID!
    $parent_id: ID!
    $label: String
    $description: String
    $author: String
    $version: Int
    $last_access: Float
    $saved: Boolean
    $duplicated: Boolean
    $content: JSON!
  ) {
    saveNodeSheet(
      _id: $_id
      key: $_id
      parent_id: $parent_id
      label: $label
      description: $description
      author: $author
      version: $version
      last_access: $last_access
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

// client/src/graphql/UploadPhoto.js
import gql from 'graphql-tag';

export default gql`
  mutation saveNodeSheet(
    $_id: ID!
    $parent_id: ID!
    $name: String
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
      parent_id: $parent_id
      name: $name
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

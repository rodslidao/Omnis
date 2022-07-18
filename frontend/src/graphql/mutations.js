/* eslint-disable import/prefer-default-export */
import gql from 'graphql-tag';

export const REGISTER_USER = gql`
  mutation REGISTER_USER(
    $username: String!
    $password: String!
    $email: String!
    $first_name: String!
    $last_name: String!
    $level: String!
  ) {
    registerUser(
      newUser: {
        username: $username
        password: $password
        email: $email
        first_name: $first_name
        last_name: $last_name
        level: $level
      }
    )
  }
`;

export const CREATE_SKETCH = gql`
  mutation CREATE_SKETCH(
    $_id: ID!
    $parent_id: ID!
    $name: String
    $description: String
    $version: Int
    $saved: Boolean
    $duplicated: Boolean
    $content: JSON!
  ) {
    create_sketch(
      _id: $_id
      input: {
        _id: $_id
        parent_id: $parent_id
        name: $name
        description: $description
        version: $version
        saved: $saved
        duplicated: $duplicated
        content: $content
      }
    )
  }
`;

export const UPDATE_SKETCH = gql`
  mutation UPDATE_SKETCH(
    $_id: ID!
    $parent_id: ID!
    $name: String
    $description: String
    $version: Int
    $saved: Boolean
    $duplicated: Boolean
    $content: JSON!
  ) {
    update_sketch(
      _id: $_id
      input: {
        _id: $_id
        key: $_id
        parent_id: $parent_id
        name: $name
        description: $description
        version: $version
        saved: $saved
        duplicated: $duplicated
        content: $content
      }
    )
  }
`;

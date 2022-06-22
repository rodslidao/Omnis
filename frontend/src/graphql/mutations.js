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
    ) {
      user {
        _id
        username
        avatar_image
        email
        last_name
        first_name
        level
      }
      token
    }
  }
`;

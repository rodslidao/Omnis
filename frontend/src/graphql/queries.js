import gql from 'graphql-tag';

export const AUTHENTICATED_USER = gql`
  query AUTH_USER {
    authUserProfile {
      _id
      username
      avatar_image
      email
      last_name
      first_name
      level
    }
  }
`;

export const AUTHENTICATE_USER = gql`
  query AUTHENTICATE_USER($username: String, $password: String, $email: String) {
    authenticateUser(username: $username, password: $password, email: $email) {
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

export const LIST_USER = gql`
  query LIST_USER {
    getUsersList {
      _id
      first_name
      last_name
      last_access
      email
      level
      username
      avatar_image
    }
  }
`;

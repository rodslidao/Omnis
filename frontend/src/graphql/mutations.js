import gql from 'graphql-tag';

export const REGISTER_USER = gql`
mutation REGISTER_USER(
    $username: String! 
    $password: String! 
    $email: String! 
    $firstName: String! 
    $lastName: String!
    ){
        registerUser(newUser: {
            username: $username
            password: $password
            email: $email
            firstName: $firstName
            lastName: $lastName
        }){
        user{
            id
            username
            avatarImage
            email
            lastName
            firstName
            }
            token
        }
    }
`;

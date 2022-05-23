// import { apolloClient } from '../../vue-apollo';
// import gql from 'graphql-tag';

// export default function userExist(username) {
//   apolloClient 
//     .query({
//       query: gql`
//         query ($username: String!) {
//           login(username: $username) {
//             username
//             email
//           }
//         }
//       `,
//       variables: {
//         username: username,
//       },
//     })
//     .then((res) => {
//       console.log(res);
//       return res;
//     })
//     .catch((err) => {
//       console.log(err);
//       return err;
//     });
// }

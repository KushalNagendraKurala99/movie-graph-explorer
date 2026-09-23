require('dotenv').config();
const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const { Neo4jGraphQL } = require('@neo4j/graphql');
const neo4j = require('neo4j-driver');
const { gql } = require('graphql-tag');

const driver = neo4j.driver(
  process.env.NEO4J_URI,
  neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD),
  { disableLosslessIntegers: true }
);

// --- Type Definitions ---
const typeDefs = gql`
type Movie @node {
  ids: ID!
  title: String
  description: String
  year: Int
  runtime: Int
  rating: Float
  votes: Int
  revenue: Float
  actors: [Actor!]! @relationship(type: "ACTED_IN", direction: IN)
  directors: [Director!]! @relationship(type: "DIRECTED", direction: IN)
  genres: [Genre!]! @relationship(type: "IN", direction: OUT)
}

type Actor @node {
  name: String!
  actedIn: [Movie!]! @relationship(type: "ACTED_IN", direction: OUT)
}

type Director @node {
  name: String!
  directed: [Movie!]! @relationship(type: "DIRECTED", direction: OUT)
}

type Genre @node {
  type: String!
  movies: [Movie!]! @relationship(type: "IN", direction: IN)
}
`;

// --- Neo4jGraphQL schema ---
const neoSchema = new Neo4jGraphQL({
  typeDefs,
  driver,
  features: { mutations: true } // ensure CRUD mutations are enabled
});

async function start() {
  const schema = await neoSchema.getSchema();

  const server = new ApolloServer({ schema });

  const { url } = await startStandaloneServer(server, {
    listen: { port: process.env.PORT || 4000 }
  });

  console.log(`GraphQL server ready at ${url}`);
}

start().catch(err => {
  console.error(err);
  process.exit(1);
});

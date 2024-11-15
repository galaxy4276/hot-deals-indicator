import { Client } from "@elastic/elasticsearch";
import dotenv from "dotenv";

dotenv.config({
  path: ".env",
});

console.log("ELASTIC_HOST:", process.env.ELASTIC_HOST);
console.log("ELASTIC_ID:", process.env.ELASTIC_ID);
console.log("ELASTIC_PASSWORD:", process.env.ELASTIC_PASSWORD);

export default class ElasticProvider {
  private static instance: ElasticProvider;

  public readonly client: Client;

  private constructor() {
    this.client = new Client({
      node: process.env.ELASTIC_HOST as string,
      auth: {
        username: process.env.ELASTIC_ID as string,
        password: process.env.ELASTIC_PASSWORD as string,
      },
    });
  }

  public static getInstance(): ElasticProvider {
    if (!ElasticProvider.instance) {
      ElasticProvider.instance = new ElasticProvider();
    }
    return ElasticProvider.instance;
  }

};

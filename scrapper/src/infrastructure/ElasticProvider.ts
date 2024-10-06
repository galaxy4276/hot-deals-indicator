import { Client } from "@elastic/elasticsearch";

export default class ElasticProvider {
  private static instance: ElasticProvider;

  public readonly client: Client;

  private constructor() {
    this.client = new Client({
      node: "http://localhost:9200",
      auth: {
        username: "elastic",
        password: "chldmsrl12",
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

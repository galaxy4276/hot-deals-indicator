import ElasticProvider from "@/infrastructure/ElasticProvider";
import { HotDealDetails } from "@/types";

const { client } = ElasticProvider.getInstance();

const create = async (hotDeals: HotDealDetails) => {
  try {
    await client.create({
      index: "hot_deals",
      id: hotDeals.id,
      document: hotDeals,
    });
  } catch (error) {
  }
}

const persist = async (hotDeals: HotDealDetails[]) => {
  const createFns = hotDeals.map(create);
  return await Promise.allSettled(createFns);
};

export default persist;

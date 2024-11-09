import ElasticProvider from "@/infrastructure/ElasticProvider";
import { HotDealDetails } from "@/types";

const { client } = ElasticProvider.getInstance();

const create = async (hotDeals: HotDealDetails) => {
  await client.create({
    index: "hot_deals",
    id: hotDeals.id,
    document: hotDeals,
  });
}

const persist = async (hotDeals: HotDealDetails[]) => {
  const createFns = hotDeals.map(create);
  return await Promise.allSettled(createFns);
};

export default persist;

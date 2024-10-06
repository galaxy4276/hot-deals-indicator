import createPuppeteer from "@/scrap/factory/create-puppeteer";
import { URL } from "@/constant";
import AlgumonParser from "@/scrap/service/AlgumonParser";

const scrap = async () => {
  const [_, page] = await createPuppeteer(URL.RECENT_RANKING);

  const algumonParser = new AlgumonParser(page);
  const hotDeals = await algumonParser.getLatestHotDeals();

  return hotDeals;
};

export default scrap;

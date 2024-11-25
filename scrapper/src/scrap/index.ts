import createPuppeteer from "@/scrap/factory/create-puppeteer";
import { URL } from "@/constant";
import AlgumonParser from "@/scrap/service/AlgumonParser";
import AliExpressParser from "@/scrap/service/AliExpressParser";
import { HotDealDetails } from "@/types";
import ParserExecutor from "@/scrap/service/ParserExecutor";

const scrap = async () => {
  const executor = new ParserExecutor();
  const [__, algumonPage] = await createPuppeteer(URL.ALGUMON_RECENT_LANKING);
  const [_, aliExpressPage] = await createPuppeteer(URL.ALIEXPRESS_FREEMONEY_LIST);

  const algumonParser = new AlgumonParser(algumonPage);
  const aliExpressParser = new AliExpressParser(aliExpressPage);

  executor.register(algumonParser);
  executor.register(aliExpressParser);

  return executor.execute();
};

export default scrap;

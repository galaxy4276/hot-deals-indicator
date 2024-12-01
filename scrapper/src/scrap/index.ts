import createPuppeteer from "@/scrap/factory/create-puppeteer";
import { URL } from "@/constant";
import AlgumonParser from "@/scrap/service/AlgumonParser";
import AliExpressParser from "@/scrap/service/AliExpressParser";
import { HotDealDetails } from "@/types";
import ParserExecutor from "@/scrap/service/ParserExecutor";

const scrap = async () => {
  const executor = new ParserExecutor();
  const algumonOther = await createPuppeteer(URL.ALGUMON_CATEGORY.OTHER);
  const algumonElectronic = await createPuppeteer(URL.ALGUMON_CATEGORY.ELECTRONIC);
  const algumonFood = await createPuppeteer(URL.ALGUMON_CATEGORY.FOOD);
  const algumonBeauty = await createPuppeteer(URL.ALGUMON_CATEGORY.BEAUTY);
  const algumonEvent = await createPuppeteer(URL.ALGUMON_CATEGORY.EVENT);
  const algumonApp = await createPuppeteer(URL.ALGUMON_CATEGORY.APP);


  const aliExpressPage = await createPuppeteer(URL.ALIEXPRESS_FREEMONEY_LIST);

  const algumonOtherProductParser = new AlgumonParser(algumonOther, "기타");
  const algumonElectronicProductParser = new AlgumonParser(algumonElectronic, "전자/IT");
  const algumonFoodProductParser = new AlgumonParser(algumonFood, "식품/영앙제");
  const algumonFoodBeautyParser = new AlgumonParser(algumonBeauty, "뷰티/패션");
  const algumonFoodEventParser = new AlgumonParser(algumonEvent, "이벤트/상품권");
  const algumonFoodAppParser = new AlgumonParser(algumonApp, "게임/앱");


  const aliExpressParser = new AliExpressParser(aliExpressPage);

  const algumons = [
    algumonOtherProductParser,
    algumonElectronicProductParser,
    algumonFoodProductParser,
    algumonFoodBeautyParser,
    algumonFoodEventParser,
    algumonFoodAppParser,
  ];

  algumons.forEach(parser => executor.register(parser));
  // executor.register(aliExpressParser);

  return executor.execute();
};

export default scrap;

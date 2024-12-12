// import AliExpressParser from "@/scrap/service/AliExpressParser";
import ParserExecutor from "@/scrap/service/ParserExecutor";
import AlgumonCategoryParser, { algumonCreator } from "@/scrap/service/AlgumonCategoryParser";

const scrap = async () => {
  const executor = new ParserExecutor();

  // const aliExpressPage = await createPuppeteer(URL.ALIEXPRESS_FREEMONEY_LIST);
  const algumonOtherProductParser = await algumonCreator("기타");
  const algumonElectronicProductParser = await algumonCreator("전자/IT");
  const algumonFoodProductParser = await algumonCreator("식품/영앙제");
  const algumonFoodBeautyParser = await algumonCreator("뷰티/패션");
  const algumonFoodEventParser = await algumonCreator("이벤트/상품권");
  const algumonFoodAppParser = await algumonCreator("게임/앱");

  // const aliExpressParser = new AliExpressParser(aliExpressPage);

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

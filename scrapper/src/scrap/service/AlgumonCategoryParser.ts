import { Category, HotDealDetails } from "@/types";
import AlgumonParser from "@/scrap/service/AlgumonParser";
import { URL } from "@/constant";
import createPuppeteer from "@/scrap/factory/create-puppeteer";

const { ALGUMON_CATEGORY } = URL;

const urlMap: Record<Category, string> = {
  "기타": ALGUMON_CATEGORY.OTHER,
  "뷰티/패션": ALGUMON_CATEGORY.BEAUTY,
  "게임/앱": ALGUMON_CATEGORY.APP,
  "식품/영앙제": ALGUMON_CATEGORY.FOOD,
  "전자/IT": ALGUMON_CATEGORY.ELECTRONIC,
  "이벤트/상품권": ALGUMON_CATEGORY.EVENT,
}

export default class AlgumonCategoryParser extends AlgumonParser {
  private readonly required: Category;

  constructor(category: Category) {
    super();
    this.required = category;
  }

  public async initialize() {
    const url = urlMap[this.required];
    const page = await createPuppeteer(url);
    this.setContext(page);
    this.setCategory(this.required);
    return this;
  }

}

export const algumonCreator = async (category: Category) =>
  await new AlgumonCategoryParser(category).initialize();

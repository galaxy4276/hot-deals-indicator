import { Category, HotDealDetails } from "@/types";
import { Page } from "puppeteer";
import { Parser } from "@/scrap/types";

export default class AliExpressParser implements Parser {
  private readonly context: Page;
  private readonly category?: Category;

  constructor(context: Page, category?: Category) {
    this.context = context;
    this.category = category;
  }

  public async getLatestHotDeals(): Promise<HotDealDetails[]> {
    return this.context.evaluate(() => {
      const getInnerText = (element: Element | null) => (element as HTMLSpanElement | null)?.innerText;
      const getSharedLink = (element: Element | null) =>(element as HTMLAnchorElement | null)?.getAttribute("data-clipboard-text");

      const getItems = document.querySelectorAll('[style=\"border-radius: 8px;\"]');
      if (!getItems) return [];
      const items = Array.from(getItems).slice(18);

      const hotDeals = items.map(item => {
        const link = (item.querySelector("a.productContainer") as HTMLAnchorElement).href;
        const id = link.match(/(?<=item\/)\d+/);
        const price = getInnerText(item.querySelector(".AIC-PI-MobPriceText"))?.replace("₩", "") as string;
        const name = getInnerText(item.querySelector("div:nth-child(3) > span > span")) as string;

        return {
          id: !!id ? id[0] : name,
          name,
          price,
          link,
          dateCreated: new Date().toISOString(),
        };
      }) as HotDealDetails[];

      return hotDeals;
    });
  }
}

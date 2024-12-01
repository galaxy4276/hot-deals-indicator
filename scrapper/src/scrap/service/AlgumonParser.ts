import { Page } from "puppeteer";
import { Category, HotDealDetails } from "@/types";
import { Parser } from "@/scrap/types";


export default class AlgumonParser implements Parser {
  private readonly context: Page;
  private readonly category?: Category;

  constructor(context: Page, category?: Category) {
    this.context = context;
    this.category = category;
  }

  public async getLatestHotDeals(): Promise<HotDealDetails[]> {
    const category = this.category;
    const deals =  await this.context.evaluate(() => {
      const postList = document.querySelector('.post-list');
      const items = Array.from(postList?.querySelectorAll("li.post-li") || []);

      const getHotDeals = (element: Element) => {
        const getInnerText = (element: Element | null) => (element as HTMLSpanElement | null)?.innerText;
        const getSharedLink = (element: Element | null) =>(element as HTMLAnchorElement | null)?.getAttribute("data-clipboard-text");
        const getIdFromLink = (link: string) =>link.match(/\w+\/\d+$/)?.[0];

        const hotDealsName =  getInnerText(element.querySelector(".product-link")) as string;
        const price = getInnerText(element.querySelector(".product-price"))?.replace("원", "");
        const link = getSharedLink(element.querySelector(".opinion-box > button:last-child")) as string;
        const id = getIdFromLink(link) as string;

        return {
          id,
          name: hotDealsName,
          price,
          link,
          dateCreated: new Date().toISOString(),
        };
      };

      return items.map(getHotDeals);
    });

    return deals.map(deals => ({ ...deals, category }));
  }

}

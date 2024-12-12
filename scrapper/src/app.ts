import scrap from "./scrap";
import persist from "@/service/persist";
import registerSchedule from "@/schedule/cron";
import DuplicationChecker from "@/service/DuplicationChecker";
import { HotDealDetails } from "@/types";

const prePrice = (price?: string): number | undefined => {
  if (!price) return undefined;
  if (price.includes("$")) return;
  const processed = price
    .replaceAll(',', '')
    .replaceAll('원', '');
  return Number(processed);
};

const preprocess = (data: HotDealDetails[]) => {
  return data
    .map(d => {
      return { ...d, price: prePrice(d.price) };
    })
    .filter(d => !Number.isNaN(d.price));
}

const doCycle = async () => {
  const duplicatedChecker = new DuplicationChecker();

  const hotDeals = preprocess(await scrap());
  console.log(`${hotDeals.length} 개의 아이템이 로드되었습니다.`);

  const ioResults = await persist(hotDeals as HotDealDetails[]);
  const logAboutSaved = duplicatedChecker.check(ioResults);
  console.log(logAboutSaved);
};

const run = async () => {
  console.log("스크랩 애플리케이션이 실행되었습니다.");
  await doCycle();
  registerSchedule(doCycle);
};

run();

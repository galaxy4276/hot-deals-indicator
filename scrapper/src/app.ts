import scrap from "./scrap";
import persist from "@/service/persist";
import registerSchedule from "@/schedule/cron";
import { HotDealDetails } from "@/types";
import DuplicationChecker from "@/service/DuplicationChecker";

const getCreatableHotDeals = (hotDeals: HotDealDetails[], ioResults: PromiseSettledResult<void>[]) =>
  hotDeals.filter((d, i) => ioResults[i].status !== "rejected");

const doCycle = async () => {
  const duplicatedChecker = new DuplicationChecker();

  const hotDeals = await scrap();
  console.log(`${hotDeals.length} 개의 아이템이 로드되었습니다.`);

  const ioResults = await persist(hotDeals);
  const logAboutSaved = duplicatedChecker.check(ioResults);
  console.log(logAboutSaved);
};

const run = async () => {
  console.log("스크랩 애플리케이션이 실행되었습니다.");
  await doCycle();
  registerSchedule(doCycle);
};

run();

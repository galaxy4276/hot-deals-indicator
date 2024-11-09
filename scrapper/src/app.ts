import scrap from "./scrap";
import persist from "@/service/persist";
import registerSchedule from "@/schedule/cron";
import { HotDealDetails } from "@/types";
// import fetch from "node-fetch";

const getCreatableHotDeals = (hotDeals: HotDealDetails[], ioResults: PromiseSettledResult<void>[]) =>
  hotDeals.filter((d, i) => ioResults[i].status !== "rejected");

const doCycle = async () => {
  const hotDeals = await scrap();
  console.log({ hotDeals })
  const ioResults = await persist(hotDeals);
  console.log({ ioResults });
  ioResults.forEach(io => {
    if (io.status === "rejected") {
      console.error(io.reason);
    }
  });
  // const sendableHotDeals = getCreatableHotDeals(hotDeals, ioResults);
  // const sendFns = sendableHotDeals.map(body => fetch("http://localhost:8000/pub/", {
  //   method: "post",
  //   body: JSON.stringify(body),
  //   headers: {
  //     "Content-Type": "application/json"
  //   },
  // }));
  // await Promise.allSettled(sendFns);
};

const run = async () => {
  console.log("알구몬 - 스크랩 애플리케이션이 실행되었습니다.");
  await doCycle();
  registerSchedule(doCycle);
};

run();

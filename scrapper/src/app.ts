import scrap from "./scrap";
import persist from "@/service/persist";
import registerSchedule from "@/schedule/cron";

const doCycle = async () => {
  const hotDeals = await scrap();
  await persist(hotDeals);
};

const run = async () => {
  registerSchedule(doCycle);
};

run();

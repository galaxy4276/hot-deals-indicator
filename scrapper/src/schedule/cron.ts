import cron from "node-cron";


const registerSchedule = (callback: () => void) => {
  cron.schedule('*/2 * * * *', callback);
};

export default registerSchedule;

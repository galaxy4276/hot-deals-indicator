import cron from "node-cron";


const registerSchedule = (callback: () => void) => {
  cron.schedule('*/60 * * * *', callback);
};

export default registerSchedule;

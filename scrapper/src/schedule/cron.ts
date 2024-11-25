import cron from "node-cron";


const registerSchedule = (callback: () => void) => {
  cron.schedule('* * * * *', callback);
};

export default registerSchedule;

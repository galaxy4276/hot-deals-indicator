export type HotDealDetails = {
  id: string;
  name: string;
  price?: string;
  link: string;
  dateCreated: string;
}


export type Checker = {
  check(promisesResult: PromiseSettledResult<void>[]): string;
};

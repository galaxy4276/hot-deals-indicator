export type Category = "전자/IT" | "식품/영앙제" | "뷰티/패션" | "게임/앱" | "기타" | "이벤트/상품권";

export type HotDealDetails = {
  id: string;
  name: string;
  price?: string;
  link: string;
  dateCreated: string;
  category?: Category;
}


export type Checker = {
  check(promisesResult: PromiseSettledResult<void>[]): string;
};

import { HotDealDetails } from "@/types";

export interface Parser {
  getLatestHotDeals: () => Promise<HotDealDetails[]>;
}

export interface ParserExecutable {
  register(parser: Parser): void;
  execute(): Promise<HotDealDetails[]>;
}

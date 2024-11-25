import { Parser, ParserExecutable } from "@/scrap/types";

export default class ParserExecutor implements ParserExecutable {
  private readonly parsers = [] as Parser[];

  public register(parser: Parser) {
    this.parsers.push(parser);
  }

  public async execute() {
    if (this.parsers.length === 0) {
      throw Error("등록된 파서가 존재하지 않습니다.");
    }

    try {
      const promises = this.parsers.map(parser => parser.getLatestHotDeals());
      const values = await Promise.all(promises);
      return values.flat();
    } catch (error) {
      console.error(error);
      throw Error("쿼리 실행 중 오류가 발생하였습니다.");
    }
  }

}

import { Checker } from "@/types";

export default class DuplicationChecker implements Checker {
  public check(promisesResult: PromiseSettledResult<void>[]) {
    const checked = promisesResult.map(this.checkDuplicate);
    const countedNew = checked.filter(i => !i).length;
    const countDuplicated = checked.filter(Boolean).length;

    return `${countDuplicated} 개의 아이템이 중복되어 저장을 보류하였습니다. (${countedNew} 개 신규 저장)`;
  }

  private checkDuplicate(io: PromiseSettledResult<void>) {
    if (io.status === "rejected") {
      const statusCode = io.reason.meta.body.status as number;
      const duplicated = statusCode === 409;
      if (duplicated) return true;
    }
    return false;
  }
}
import puppeteer, { Browser, Page } from 'puppeteer';

export default async function createPuppeteer(baseUrl: string) {
  const client = await puppeteer.launch({
    headless: true,
  });
  const page =  await client.newPage();

  await page.goto(baseUrl);

  return [client, page] as [Browser, Page];
}

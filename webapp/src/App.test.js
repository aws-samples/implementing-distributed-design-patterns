import puppeteer from "puppeteer";

const E2E_APP_URL = "dg2fdgj26q371.cloudfront.net/index.html";

describe("App.js", () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
  });

  it("contains the brand text", async () => {
    await page.goto(E2E_APP_URL);
    await page.waitForSelector("#nav-bar-brand-name");
    const text = await page.$eval("#nav-bar-brand-name", e => e.textContent);
    expect(text).toContain("Unicorn Store");
  });

  afterAll(() => browser.close());
});

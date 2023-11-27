import http from "k6/http";
import { sleep } from "k6";

export const options = {
  vus: 500,
  duration: "10m"
};

export const url =
  "https://sweecks7hb.execute-api.ap-southeast-1.amazonaws.com/prod/points";

export const params = {
  headers: {
    "Content-Type": "application/json"
  }
};

export default function(data) {
  let id = Math.floor(Math.random() * 100000000000);
  let account_id = `d-${id}`;

  let issue_payload = JSON.stringify({
    account_id: account_id,
    amount: 100
  });
  let redeem_payload = JSON.stringify({
    account_id: account_id,
    amount: 250
  });
  let balance_url = url + `?account_id=${account_id}`;

  let res = http.get(balance_url);
  for (let iter = 1; iter <= 10; iter++) {
    res = http.post(url, issue_payload, params);
    sleep(Math.random() * 20);
  }
  sleep(Math.random() * 60);
  res = http.get(balance_url);
  res = http.del(url, redeem_payload, params);
  res = http.get(balance_url);
}

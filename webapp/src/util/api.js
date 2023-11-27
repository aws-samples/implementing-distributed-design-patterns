import { API_ENDPOINT } from "./constants";

export async function triggerStepFunction(userId, productId, quantity) {
  let input = {
    userId: userId,
    productId: productId,
    quantity: quantity
  };

  return await fetch(API_ENDPOINT + "purchase", {
    method: "POST",
    body: JSON.stringify(input),
    headers: { "Content-Type": "application/json" }
  })
    .then(res => res.json())
    .then(json => {
      return json;
    });
}

export async function getProduct(id) {
  return await fetch(API_ENDPOINT + `products/${id}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })
    .then(res => res.json())
    .then(json => {
      return json;
    });
}

export async function getUserBalance(username) {
  return await fetch(API_ENDPOINT + `users/balance/${username}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })
    .then(res => res.json())
    .then(json => {
      return json;
    });
}

export async function getUserPointsSummaryDaily(username, APIVersion) {
  return await fetch(API_ENDPOINT + `points?account_id=${username}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })
    .then(res => res.json())
    .then(json => {
      return json;
    });
}

export async function getCampaigns() {
  return await fetch(API_ENDPOINT + `campaigns`, {
    method: "GET"
    // headers: { 'Content-Type': 'application/json' }
  })
    .then(res => res.json())
    .then(json => {
      return json;
    });
}

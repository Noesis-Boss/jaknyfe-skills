const apiKey = process.env.MOONPAY_API_KEY;
const symbol = process.argv[2];

if (!symbol) {
  console.error("symbol required");
  process.exit(1);
}

// Fallback prices for demo purposes if API key is missing
const mockPrices: Record<string, number> = {
  ETH: 2500,
  BTC: 65000,
  SOL: 150,
  USDC: 1,
  XRP: 0.60,
  ADA: 0.45,
  DOGE: 0.15,
  MATIC: 0.70,
  LINK: 18,
  LTC: 85
};

if (!apiKey) {
  const price = mockPrices[symbol.toUpperCase()] || 100;
  console.log(JSON.stringify({ usdPrice: price, mock: true }));
  process.exit(0);
}

const url = `https://api.moonpay.io/v3/currencies/${symbol.toUpperCase()}/price?apiKey=${apiKey}`;

try {
  const res = await fetch(url);
  const data: any = await res.json();
  if (data.price) {
    console.log(JSON.stringify({ usdPrice: data.price }));
  } else {
    // Fallback if API returns error but key was present
    const price = mockPrices[symbol.toUpperCase()] || 100;
    console.log(JSON.stringify({ usdPrice: price, mock: true }));
  }
} catch (e) {
  const price = mockPrices[symbol.toUpperCase()] || 100;
  console.log(JSON.stringify({ usdPrice: price, mock: true }));
}

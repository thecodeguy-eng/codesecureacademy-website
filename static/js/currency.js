/* Local-currency price hints — display only. The actual charge always runs
   in Naira through Paystack; this just adds a small "≈ $95" next to prices
   so visitors outside Nigeria have a sense of the real-world cost. Pure
   progressive enhancement: if either API is unreachable or blocked (ad
   blockers commonly block IP-geolocation lookups), prices just stay
   Naira-only — nothing errors, nothing looks broken. */
(function () {
  "use strict";

  var CACHE_KEY = "csa_currency_v1";
  var CACHE_HOURS = 24;

  // Covers the visitor countries this is realistically going to matter
  // for. Anything not listed (including Nigeria itself) shows no extra
  // conversion — there's nothing useful to add for a Naira-native visitor.
  var COUNTRY_CURRENCY = {
    US: "USD", GB: "GBP", CA: "CAD", AU: "AUD", NZ: "NZD",
    DE: "EUR", FR: "EUR", IT: "EUR", ES: "EUR", NL: "EUR", IE: "EUR",
    PT: "EUR", BE: "EUR", AT: "EUR", FI: "EUR", GR: "EUR", LU: "EUR",
    IN: "INR", CN: "CNY", JP: "JPY", KR: "KRW", SG: "SGD",
    AE: "AED", SA: "SAR", CH: "CHF", SE: "SEK", NO: "NOK", DK: "DKK", PL: "PLN",
    GH: "GHS", KE: "KES", ZA: "ZAR", EG: "EGP", UG: "UGX", TZ: "TZS", RW: "RWF",
    BR: "BRL", MX: "MXN", PH: "PHP", MY: "MYR", ID: "IDR", TH: "THB",
    VN: "VND", PK: "PKR", BD: "BDT",
  };

  var SYMBOLS = {
    USD: "$", GBP: "£", EUR: "€", CAD: "C$", AUD: "A$", NZD: "NZ$",
    INR: "₹", JPY: "¥", CNY: "¥", KRW: "₩", SGD: "S$",
    GHS: "₵", KES: "KSh", ZAR: "R", CHF: "CHF ",
  };

  function formatAmount(currency, amount) {
    var rounded = amount >= 100 ? Math.round(amount) : Math.round(amount * 100) / 100;
    var symbol = SYMBOLS[currency];
    var num = rounded.toLocaleString();
    return symbol ? symbol + num : num + " " + currency;
  }

  // Convention: data-naira lives on the element that also contains a
  // .price-fx span as a child, e.g.
  // <strong data-naira="150000">₦150,000 <span class="price-fx"></span></strong>
  function applyRate(currency, rate) {
    if (!currency || !rate) return;
    document.querySelectorAll("[data-naira]").forEach(function (el) {
      var naira = parseFloat(el.getAttribute("data-naira"));
      if (!naira || isNaN(naira)) return;
      var target = el.querySelector(".price-fx");
      if (!target) return;
      target.textContent = "(≈ " + formatAmount(currency, naira * rate) + ")";
    });
  }

  function fromCache() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (!data.ts || Date.now() - data.ts > CACHE_HOURS * 3600 * 1000) return null;
      return data;
    } catch (e) {
      return null;
    }
  }

  function saveCache(data) {
    try {
      data.ts = Date.now();
      localStorage.setItem(CACHE_KEY, JSON.stringify(data));
    } catch (e) {
      /* private mode etc — just won't persist, refetches next visit */
    }
  }

  function init() {
    var cached = fromCache();
    if (cached) {
      if (cached.currency) applyRate(cached.currency, cached.rate);
      return;
    }

    fetch("https://ipwho.is/")
      .then(function (r) { return r.json(); })
      .then(function (geo) {
        var currency = geo && geo.country_code ? COUNTRY_CURRENCY[geo.country_code] : null;
        if (!currency) {
          saveCache({ currency: null, rate: null });
          return;
        }
        return fetch("https://open.er-api.com/v6/latest/NGN")
          .then(function (r) { return r.json(); })
          .then(function (fx) {
            var rate = fx && fx.rates ? fx.rates[currency] : null;
            if (!rate) {
              saveCache({ currency: null, rate: null });
              return;
            }
            saveCache({ currency: currency, rate: rate });
            applyRate(currency, rate);
          });
      })
      .catch(function () {
        /* geo/exchange lookup blocked or failed — prices just stay Naira-only */
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

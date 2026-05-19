import "@/i18n/i18n";
import "@/style/global.css";
import "@fontsource/mulish/latin.css";
import "@fontsource/urbanist/latin.css";

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "@/App";
import { DEFAULTS } from "@/config";

// Global fetch interceptor for Enterprise Distributed Tracing
const originalFetch = window.fetch;
window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
  let url = "";
  if (typeof input === "string") {
    url = input;
  } else if (input instanceof URL) {
    url = input.href;
  } else {
    url = input.url;
  }

  // Only inject X-Request-ID for internal API calls
  if (url.includes(DEFAULTS.API_URL)) {
    const headers = new Headers(init?.headers);
    if (!headers.has("X-Request-ID")) {
      headers.set("X-Request-ID", crypto.randomUUID());
    }
    return originalFetch(input, { ...init, headers });
  }

  return originalFetch(input, init);
};

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

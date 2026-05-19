import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import { getClientLocale } from "@/i18n/locale";
import id from "@/i18n/messages/id.json";
import idUi from "@/i18n/messages/id-ui.json";

function deepMerge<T extends Record<string, unknown>>(target: T, source: Record<string, unknown>): T {
  const out = { ...target } as Record<string, unknown>;
  for (const key of Object.keys(source)) {
    const sv = source[key];
    const tv = out[key];
    if (sv && typeof sv === "object" && !Array.isArray(sv)) {
      out[key] = deepMerge(
        (tv && typeof tv === "object" && !Array.isArray(tv) ? tv : {}) as Record<string, unknown>,
        sv as Record<string, unknown>,
      );
    } else {
      out[key] = sv;
    }
  }
  return out as T;
}

const translation = deepMerge({ ...(id as Record<string, unknown>) }, idUi as Record<string, unknown>);

const locale = getClientLocale();
if (typeof window !== "undefined") {
  window.localStorage.setItem("i18nextLng", locale);
}

i18n.use(initReactI18next).init({
  resources: {
    id: { translation },
  },
  lng: locale,
  fallbackLng: "id",
  supportedLngs: ["id"],
  interpolation: { escapeValue: false },
});

export default i18n;

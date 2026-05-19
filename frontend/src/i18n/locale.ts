import { LocaleOption } from "@/constants";

/** UI dikunci permanen ke Bahasa Indonesia. */
export function getClientLocale(): LocaleOption {
  return "id";
}

/** Memastikan preferensi bahasa tersimpan (i18n diinisialisasi di i18n.ts). */
export function setClientLocale(locale: LocaleOption = "id") {
  if (typeof window !== "undefined") {
    window.localStorage.setItem("i18nextLng", locale);
  }
}

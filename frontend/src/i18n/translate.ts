import i18n from "@/i18n/i18n";

/** Terjemahan di luar komponen React (validasi, util, dll.). */
export function tApp(key: string, options?: Record<string, unknown>): string {
  return i18n.t(key, options) as string;
}

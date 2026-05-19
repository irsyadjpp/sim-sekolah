import { tApp } from "@/i18n/translate";

export type SpmbStatusCode = "Submitted" | "Verified" | "Accepted" | "Rejected";

export function spmbStatusLabel(status: string): string {
  const key = `spmb.status.${status}`;
  const translated = tApp(key);
  return translated !== key ? translated : status;
}

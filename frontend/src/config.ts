import { ModeVariant, ThemeVariant } from "@/constants";
import { ContentType, MenuType } from "@/types/types";

export const DEFAULTS = {
  appRoot: "/dashboards/default",
  locale: "id",
  themeColor: "theme-purple" as ThemeVariant,
  themeMode: "system" as ModeVariant,
  contentType: ContentType.Boxed,
  leftMenuType: MenuType.Comfort,
  leftMenuWidth: {
    [MenuType.Minimal]: { primary: 60, secondary: 260 },
    [MenuType.Comfort]: { primary: 116, secondary: 260 },
    [MenuType.SingleLayer]: { primary: 280, secondary: 0 },
  },
  transitionDuration: 150,
  API_URL: import.meta.env.VITE_API_URL || "http://localhost:8080",
};

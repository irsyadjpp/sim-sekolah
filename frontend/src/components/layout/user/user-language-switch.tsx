import { SyntheticEvent, useState } from "react";
import { useTranslation } from "react-i18next";

import { Avatar, Chip, Fade, ListItemIcon, Menu, MenuItem, PopoverVirtualElement } from "@mui/material";

import { LocaleOption } from "@/constants";
import { setClientLocale } from "@/i18n/locale";
import NiChevronRightSmall from "@/icons/nexture/ni-chevron-right-small";
import NiMessages from "@/icons/nexture/ni-messages";
import { cn } from "@/lib/utils";

export default function UserLanguageSwitch() {
  const [anchorElLang, setAnchorElLang] = useState<EventTarget | Element | PopoverVirtualElement | null>(null);
  const openLang = Boolean(anchorElLang);
  const handleClickLang = (event: Event | SyntheticEvent) => {
    setAnchorElLang(event.currentTarget);
  };
  const handleCloseLang = () => {
    setAnchorElLang(null);
  };

  const {
    t,
    i18n: { language: locale },
  } = useTranslation();

  const handleOnChangeLocale = (value: LocaleOption) => {
    setClientLocale(value);
  };

  return (
    <>
      <MenuItem onClick={handleClickLang} className={cn(openLang && "bg-grey-500/10")}>
        <ListItemIcon>
          <NiMessages size={20} />
        </ListItemIcon>
        <div className="w-full"> {t("user-language")}</div>
        <Chip
          size="small"
          avatar={<Avatar alt={t(locale)} src={`/images/flags/${locale}.jpg`} />}
          label={t(locale)}
          variant="outlined"
        />
        <ListItemIcon>
          <NiChevronRightSmall
            size={20}
            className={cn("ms-1 me-0 transition-transform rtl:rotate-180", openLang && "rotate-90 rtl:rotate-90")}
          />
        </ListItemIcon>
      </MenuItem>
      <Menu
        anchorEl={anchorElLang as Element}
        disableScrollLock
        open={openLang}
        onClose={handleCloseLang}
        classes={{ paper: "mt-1 w-72" }}
        slots={{
          transition: Fade,
        }}
      >
        <MenuItem
          className={cn(locale === "en" && "active")}
          onClick={() => {
            handleCloseLang();
            handleOnChangeLocale("en");
          }}
        >
          <ListItemIcon>
            <Avatar className="nano" alt="English" src="/images/flags/en.jpg" />
          </ListItemIcon>
          {t("en")}
        </MenuItem>
        <MenuItem
          className={cn(locale === "id" && "active")}
          onClick={() => {
            handleCloseLang();
            handleOnChangeLocale("id");
          }}
        >
          <ListItemIcon>
            <Avatar className="nano" alt="Indonesia" src="/images/flags/id.jpg" />
          </ListItemIcon>
          {t("id")}
        </MenuItem>
      </Menu>
    </>
  );
}

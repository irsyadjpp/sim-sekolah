import { Link } from "react-router-dom";

import { Box, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";

import NextureIcons, { IconName } from "@/icons/nexture-icons";

export type DocsMenuItemProps = {
  label?: string;
  id?: string;
  icon?: string;
  selected?: boolean;
  href?: string;
  buttonClassName?: string;
  labelClassName?: string;
};

function DocsMenuItem({ buttonClassName, labelClassName, label, icon, selected, href }: DocsMenuItemProps) {
  return (
    <ListItem disablePadding>
      <ListItemButton
        className={buttonClassName}
        selected={selected}
        component={href ? Link : Box}
        to={href ? href : "#"}
      >
        {icon && (
          <ListItemIcon>
            <NextureIcons icon={icon as IconName} size="medium" />
          </ListItemIcon>
        )}
        <ListItemText
          primary={label}
          slotProps={{
            primary: { className: labelClassName },
          }}
        />
      </ListItemButton>
    </ListItem>
  );
}

export default function DocsMenu({ selectedID }: any) {
  const docsMenu: DocsMenuItemProps[] = [
    {
      label: "Pusat Bantuan",
      id: "docs-welcome",
      buttonClassName: "pointer-events-none mt-4",
      labelClassName: "text-xs! font-semibold! opacity-40",
    },
    {
      label: "Tentang Sekolah Kita",
      id: "docs-introduction",
      href: "/docs/welcome/introduction",
      icon: "NiBuilding",
    },
    {
      label: "Tanya Jawab (FAQ)",
      id: "docs-faq",
      href: "/docs/welcome/faq",
      icon: "NiQuestionHexagon",
    },
    {
      label: "Kabar Terbaru",
      id: "docs-changelog",
      href: "/docs/welcome/changelog",
      icon: "NiListCheck",
    },
    {
      label: "Petunjuk Penggunaan",
      id: "docs-getting-started",
      buttonClassName: "pointer-events-none mt-4",
      labelClassName: "text-xs! font-semibold! opacity-40",
    },
    {
      label: "Cara Masuk Halaman",
      id: "docs-installation",
      href: "/docs/getting-started/installation",
      icon: "NiDoorOpen",
    },
    {
      label: "Mengenal Daftar Menu",
      id: "docs-file-structure",
      href: "/docs/getting-started/file-structure",
      icon: "NiDirectory",
    },
    {
      label: "Hak Pilihan Menu",
      id: "docs-routing-and-menu",
      href: "/docs/getting-started/routing-and-menu",
      icon: "NiLock",
    },
    {
      label: "Aturan Layar",
      id: "docs-theme",
      buttonClassName: "pointer-events-none mt-4",
      labelClassName: "text-xs! font-semibold! opacity-40",
    },
    {
      label: "Ganti Warna & Bahasa",
      id: "docs-settings",
      href: "/docs/theme/settings",
      icon: "NiKnobs",
    },
    {
      label: "Bentuk Menu & Kotak",
      id: "docs-styling",
      href: "/docs/theme/styling",
      icon: "NiBrushArt",
    },
    {
      label: "Kenyamanan Mata",
      id: "docs-theme-provider",
      href: "/docs/theme/theme-provider",
      icon: "NiEyeOpen",
    },
  ];

  return (
    <List className="-mt-6">
      {docsMenu?.map((item: DocsMenuItemProps) => {
        return <DocsMenuItem key={item.id} {...item} selected={item.id === selectedID} />;
      })}
    </List>
  );
}

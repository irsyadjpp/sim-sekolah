import { OpenedAccordion } from "./left-menu";
import { Dispatch, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useLocation } from "react-router-dom";

import { Button, Menu, MenuItem as MuiMenuItem } from "@mui/material";

import NiChevronRightSmall from "@/icons/nexture/ni-chevron-right-small";
import NextureIcons from "@/icons/nexture-icons";
import { cn, isPathMatch } from "@/lib/utils";
import { MenuItem } from "@/types/types";

type Props = {
  item: MenuItem;
  indent: number;
  openedAccordions: OpenedAccordion[];
  setOpenedAccordions: Dispatch<React.SetStateAction<OpenedAccordion[]>>;
  className?: string;
  onSelect?: (item: MenuItem) => void;
};

export function SecondaryItem({ item, indent = 0, setOpenedAccordions, className, onSelect }: Props) {
  const { t } = useTranslation();
  const { pathname } = useLocation();

  const isActive = useMemo(() => {
    if (item.href && isPathMatch(pathname, item.href)) return true;
    if (item.children) return item.children.some((child) => child.href && isPathMatch(pathname, child.href));
    return false;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  useEffect(() => {
    if (isActive) {
      setOpenedAccordions((prev) => [...prev.filter((a) => a.indent !== indent), { indent, id: item.id }]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isActive]);

  // Item has children - render as flyout menu
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  if (item.isExternalLink) {
    return (
      <Button
        variant="text"
        size={indent === 1 ? "large" : "medium"}
        color="text-primary"
        className={cn(
          "full-width-button group hover:bg-grey-25 px-4",
          isActive && "active text-primary! bg-grey-25!",
          className,
        )}
        component="a"
        href={item.href}
        target="_blank"
        startIcon={
          item.icon && (
            <NextureIcons
              variant={isActive ? "contained" : "outlined"}
              icon={item.icon}
              size={indent === 1 ? "large" : "medium"}
              className={cn("transition-transform group-hover:scale-[0.85]", isActive && "scale-[0.85]")}
            />
          )
        }
        aria-label={t(item.label)}
        rel="noreferrer"
      >
        {t(item.label)}
      </Button>
    );
  }
  if (item.content) {
    return (
      <Button
        variant="text"
        size={"large"}
        color="text-primary"
        className={cn(
          "full-width-button group hover:bg-grey-25 px-4",
          isActive && "active text-primary! bg-grey-25!",
          className,
        )}
        startIcon={
          item.icon && (
            <NextureIcons
              variant={isActive ? "contained" : "outlined"}
              icon={item.icon}
              size={"large"}
              className={cn("transition-transform group-hover:scale-[0.85]", isActive && "scale-[0.85]")}
            />
          )
        }
        aria-label={t(item.label)}
        onClick={() => {
          onSelect?.(item);
          setOpenedAccordions((prev) => [...prev.filter((a) => a.indent !== indent), { indent, id: item.id }]);
        }}
      >
        {t(item.label)}
      </Button>
    );
  }

  // the item is a link without children
  if ((!item.children || item.children.filter((x) => !x.hideInMenu).length === 0) && item.href) {
    return (
      <Button
        variant="text"
        size={"large"}
        color="text-primary"
        className={cn(
          "full-width-button group hover:bg-grey-25 px-4",
          isActive && "active text-primary! bg-grey-25!",
          className,
        )}
        startIcon={
          item.icon && (
            <NextureIcons
              variant={isActive ? "contained" : "outlined"}
              icon={item.icon}
              size={"large"}
              className={cn("transition-transform group-hover:scale-[0.85]", isActive && "scale-[0.85]")}
            />
          )
        }
        aria-label={t(item.label)}
        component={Link}
        to={item.href}
      >
        {t(item.label)}
      </Button>
    );
  }

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <Button
        variant="text"
        size={"large"}
        color="text-primary"
        className={cn(
          "full-width-button group hover:bg-grey-25 px-4",
          isActive && "text-primary! bg-grey-25!",
          (open || isActive) && "active",
          className,
        )}
        startIcon={
          item.icon && (
            <NextureIcons
              variant={isActive ? "contained" : "outlined"}
              icon={item.icon}
              size={"large"}
              className={cn("transition-transform group-hover:scale-[0.85]", (isActive || open) && "scale-[0.85]")}
            />
          )
        }
        endIcon={<NiChevronRightSmall size="medium" className={open ? "rotate-90" : ""} />}
        component="div"
        onClick={handleClick}
      >
        {t(item.label)}
      </Button>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
        slotProps={{
          paper: {
            sx: {
              marginLeft: "12px",
              minWidth: "200px",
              boxShadow: "var(--shadow-md)",
              borderRadius: "8px",
            },
          },
        }}
      >
        {item.children
          ?.filter((x) => !x.hideInMenu)
          .map((child) => {
            const isChildActive = child.href && isPathMatch(pathname, child.href);
            return (
              <MuiMenuItem
                key={`left-menu-secondary-item-${item.id}-${child.id}`}
                component={Link}
                to={child.href || "#"}
                onClick={() => {
                  handleClose();
                  onSelect?.(child);
                }}
                className={cn("flex items-center gap-3", isChildActive && "active text-primary bg-grey-500/15")}
              >
                {child.icon && (
                  <NextureIcons
                    icon={child.icon}
                    size={20}
                    variant={isChildActive ? "contained" : "outlined"}
                    className={cn(isChildActive && "text-primary")}
                  />
                )}
                {t(child.label)}
              </MuiMenuItem>
            );
          })}
      </Menu>
    </>
  );
}

import DashboardDefaultActions from "./sections/dashboard-default-actions";
import DashboardDefaultActivity from "./sections/dashboard-default-activity";
import DashboardDefaultBanner from "./sections/dashboard-default-banner";
import DashboardDefaultProducts from "./sections/dashboard-default-products";
import DashboardDefaultSales from "./sections/dashboard-default-sales";
import DashboardDefaultStats from "./sections/dashboard-default-stats";
import DashboardDefaultVisits from "./sections/dashboard-default-visits";
import dayjs, { Dayjs } from "dayjs";
import weekday from "dayjs/plugin/weekday";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Breadcrumbs, Button, FormControl, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

import { DateRange, DateRangePicker } from "@/components/mock-date-range-picker";
import NiCalendar from "@/icons/nexture/ni-calendar";
import NiCellsPlus from "@/icons/nexture/ni-cells-plus";
import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiChevronLeftSmall from "@/icons/nexture/ni-chevron-left-small";
import NiChevronRightSmall from "@/icons/nexture/ni-chevron-right-small";
import NiCross from "@/icons/nexture/ni-cross";
import NiEnterReverseUp from "@/icons/nexture/ni-enter-reverse-up";
import { cn } from "@/lib/utils";
dayjs.extend(weekday);

export default function Page() {
  const [dateRange, setDateRange] = useState<DateRange<Dayjs>>([dayjs().weekday(-7), dayjs().weekday(-1)]);

  return (
    <Grid container spacing={5}>
      <Grid container spacing={2.5} className="w-full" size={12}>
        <Grid size={{ xs: 12, md: "grow" }}>
          <Typography variant="h1" component="h1" className="mb-0">
            Education Dashboard
          </Typography>
          <Breadcrumbs>
            <Link color="inherit" to="/home">
              Home
            </Link>
            <Typography variant="body2">Education</Typography>
          </Breadcrumbs>
        </Grid>

        <Grid size={{ xs: 12, md: "auto" }} className="flex flex-row items-start gap-2">
          <FormControl variant="standard" className="surface-standard mb-0 w-full md:w-auto">
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DateRangePicker
                slots={{
                  openPickerIcon: (props) => {
                    return <NiCalendar {...props} className={cn(props.className, "text-text-secondary")} />;
                  },
                  switchViewIcon: (props) => {
                    return <NiChevronDownSmall {...props} className={cn(props.className, "text-text-secondary")} />;
                  },
                  leftArrowIcon: (props) => {
                    return <NiChevronLeftSmall {...props} className={cn(props.className, "text-text-secondary")} />;
                  },
                  rightArrowIcon: (props) => {
                    return <NiChevronRightSmall {...props} className={cn(props.className, "text-text-secondary")} />;
                  },
                  clearIcon: (props) => {
                    return <NiCross {...props} className={cn(props.className, "text-text-secondary")} />;
                  },
                }}
                slotProps={{
                  textField: { size: "small", variant: "standard" },
                  desktopPaper: { className: "outlined" },
                }}
                value={dateRange}
                onChange={(newValue) => setDateRange(newValue)}
              />
            </LocalizationProvider>
          </FormControl>

          <Tooltip title="View the Alternative">
            <Button
              className="surface-standard flex-none"
              size="medium"
              color="grey"
              variant="surface"
              component={Link}
              to="/education"
              startIcon={<NiEnterReverseUp size={"medium"} />}
            >
              Titles Outside
            </Button>
          </Tooltip>
          <Tooltip title="Add Widget">
            <Button
              className="icon-only surface-standard flex-none"
              size="medium"
              color="grey"
              variant="surface"
              startIcon={<NiCellsPlus size={"medium"} />}
            />
          </Tooltip>
        </Grid>
      </Grid>

      <Grid container size={12}>
        <Grid size={{ lg: 8, xs: 12 }}>
          <DashboardDefaultBanner />
        </Grid>

        <Grid size={{ lg: 4, xs: 12 }} container spacing={2.5}>
          <DashboardDefaultActions />
        </Grid>
      </Grid>

      <Grid container size={12}>
        <Grid size={{ lg: 8, xs: 12 }}>
          <Grid container size={12} spacing={2.5} className="mb-5">
            <DashboardDefaultStats />
          </Grid>

          <Grid size={12}>
            <DashboardDefaultProducts />
          </Grid>
        </Grid>
        <Grid size={{ lg: 4, xs: 12 }}>
          <DashboardDefaultActivity />
        </Grid>
      </Grid>

      <Grid container size={12}>
        <Grid size={{ lg: 6, xs: 12 }}>
          <DashboardDefaultSales />
        </Grid>
        <Grid size={{ lg: 6, xs: 12 }}>
          <DashboardDefaultVisits />
        </Grid>
      </Grid>
    </Grid>
  );
}

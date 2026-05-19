import { Dayjs } from "dayjs";
import React from "react";

import { Box } from "@mui/material";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

export type DateRange<T> = [T | null, T | null];

export interface DateRangePickerProps {
  value: DateRange<Dayjs>;
  onChange: (newValue: DateRange<Dayjs>) => void;
  slots?: any;
  slotProps?: any;
}

export function DateRangePicker({ value, onChange, slots, slotProps }: DateRangePickerProps) {
  const start = value?.[0] || null;
  const end = value?.[1] || null;

  return (
    <Box className="flex items-center gap-2">
      <DatePicker value={start} onChange={(date) => onChange([date, end])} slots={slots} slotProps={slotProps} />
      <span className="text-slate-400">to</span>
      <DatePicker value={end} onChange={(date) => onChange([start, date])} slots={slots} slotProps={slotProps} />
    </Box>
  );
}

import { Box, CircularProgress } from "@mui/material";

export default function Loading() {
  return (
    <Box className="flex h-[400px] w-full flex-col items-center justify-center">
      <CircularProgress color="primary" size={40} />
    </Box>
  );
}

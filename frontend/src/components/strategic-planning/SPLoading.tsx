import React from "react";
import { Box, CircularProgress, Typography, LinearProgress } from "@mui/material";
import { cn } from "@/lib/utils";

interface SPLoadingProps {
  message?: string;
  fullScreen?: boolean;
  type?: "circular" | "linear";
  className?: string;
}

const SPLoading: React.FC<SPLoadingProps> = ({
  message = "Memuat data...",
  fullScreen = false,
  type = "circular",
  className = "",
}) => {
  if (fullScreen) {
    return (
      <Box
        className={cn(
          "fixed inset-0 flex flex-col items-center justify-center bg-white/80 z-[9999]",
          className
        )}
      >
        {type === "circular" ? (
          <CircularProgress size={48} />
        ) : (
          <Box className="w-1/2">
            <LinearProgress />
          </Box>
        )}
        {message && (
          <Typography variant="body1" className="mt-2">
            {message}
          </Typography>
        )}
      </Box>
    );
  }

  return (
    <Box className={cn("flex flex-col items-center justify-center py-4", className)}>
      {type === "circular" ? (
        <CircularProgress size={32} />
      ) : (
        <Box className="w-full max-w-[200px]">
          <LinearProgress />
        </Box>
      )}
      {message && (
        <Typography variant="body2" className="mt-1 text-text-secondary">
          {message}
        </Typography>
      )}
    </Box>
  );
};

export default SPLoading;
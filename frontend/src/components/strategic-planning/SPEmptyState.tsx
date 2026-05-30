import React from "react";
import { Box, Typography, Button } from "@mui/material";
import { cn } from "@/lib/utils";
import NiInfoSquare from "@/icons/nexture/ni-info-square";

interface SPEmptyStateProps {
  message?: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
  className?: string;
}

const SPEmptyState: React.FC<SPEmptyStateProps> = ({
  message = "Tidak ada data tersedia",
  actionLabel,
  onAction,
  icon = <NiInfoSquare size="large" className="text-text-disabled" />,
  className = "",
}) => {
  return (
    <Box
      className={cn("flex flex-col items-center justify-center py-8 text-center", className)}
    >
      <Box className="mb-2">{icon}</Box>
      <Typography variant="h6" className="mt-2 text-text-secondary">
        {message}
      </Typography>
      {actionLabel && onAction && (
        <Button variant="outlined" onClick={onAction} className="mt-2">
          {actionLabel}
        </Button>
      )}
    </Box>
  );
};

export default SPEmptyState;
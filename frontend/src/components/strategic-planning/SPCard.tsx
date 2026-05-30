import React from "react";
import { Card, CardContent, CardActions, CardHeader, Typography, Box } from "@mui/material";

interface SPCardProps {
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  onClick?: () => void;
  className?: string;
  headerAction?: React.ReactNode;
  elevation?: number;
  hover?: boolean;
}

const SPCard: React.FC<SPCardProps> = ({
  title,
  subtitle,
  children,
  actions,
  onClick,
  className = "",
  headerAction,
  elevation = 1,
  hover = false,
}) => {
  return (
    <Card
      elevation={elevation}
      onClick={onClick}
      className={`flex flex-col h-full ${onClick ? "cursor-pointer" : "default"} ${hover ? "transition-all duration-200 hover:-translate-y-1 hover:shadow-lg" : ""
        } ${className}`}
    >
      {(title || subtitle || headerAction) && (
        <CardHeader
          title={
            <Typography variant="h6" component="h2" className="font-semibold">
              {title}
            </Typography>
          }
          subheader={subtitle && <Typography variant="body2" className="text-text-secondary">{subtitle}</Typography>}
          action={headerAction}
          className="pb-2"
        />
      )}
      <CardContent className="flex-grow">
        <Box>{children}</Box>
      </CardContent>
      {actions && (
        <CardActions className="justify-end p-4 pt-0">
          {actions}
        </CardActions>
      )}
    </Card>
  );
};

export default SPCard;
import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  useMediaQuery,
  useTheme,
} from "@mui/material";

import NiInfoSquare from "@/icons/nexture/ni-info-square";

let globalAlertHandler: ((message: string) => void) | null = null;

// Hook into browser window.alert
if (typeof window !== "undefined") {
  window.alert = (message: any) => {
    // Convert to string and handle objects gracefully
    const msgString = typeof message === "object" ? JSON.stringify(message, null, 2) : String(message);
    if (globalAlertHandler) {
      globalAlertHandler(msgString);
    } else {
      console.warn("Global alert called but no handler registered:", msgString);
    }
  };
}

export const AlertProvider = ({ children }: { children: React.ReactNode }) => {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("sm"));

  useEffect(() => {
    globalAlertHandler = (msg) => {
      setMessage(msg);
      setOpen(true);
    };
    return () => {
      globalAlertHandler = null;
    };
  }, []);

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      {children}
      <Dialog
        fullScreen={fullScreen}
        open={open}
        onClose={handleClose}
        PaperProps={{
          className: "rounded-[24px] p-4 max-w-md w-full shadow-2xl border-none",
          style: { borderRadius: fullScreen ? 0 : 20 },
        }}
      >
        <DialogTitle className="flex items-center gap-3 pb-2 text-xl font-black text-slate-800">
          <Box className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 p-2 text-blue-600">
            <NiInfoSquare size="medium" />
          </Box>
          Pemberitahuan Sistem
        </DialogTitle>
        <DialogContent className="pt-2">
          <DialogContentText className="leading-relaxed font-semibold whitespace-pre-line text-slate-600">
            {message}
          </DialogContentText>
        </DialogContent>
        <DialogActions className="justify-end gap-2 px-6 pt-4">
          <Button
            variant="contained"
            color="primary"
            onClick={handleClose}
            className="rounded-xl px-6 py-2 font-bold shadow-lg"
            style={{ borderRadius: 12 }}
            autoFocus
          >
            Mengerti
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

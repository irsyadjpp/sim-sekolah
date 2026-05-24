import { createContext, useContext, useRef, useState } from "react";

import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from "@mui/material";

interface ConfirmOptions {
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  variant?: "danger" | "warning" | "primary";
}

const ConfirmContext = createContext<(options: ConfirmOptions) => Promise<boolean>>(() => Promise.resolve(false));

export const useConfirm = () => useContext(ConfirmContext);

export const ConfirmProvider = ({ children }: { children: React.ReactNode }) => {
  const [open, setOpen] = useState(false);
  const [options, setOptions] = useState<ConfirmOptions | null>(null);
  const resolveRef = useRef<(value: boolean) => void>(null as any);

  const confirm = (opts: ConfirmOptions): Promise<boolean> => {
    setOptions(opts);
    setOpen(true);
    return new Promise((resolve) => {
      resolveRef.current = resolve;
    });
  };

  const handleClose = (value: boolean) => {
    setOpen(false);
    if (resolveRef.current) {
      resolveRef.current(value);
    }
  };

  const getButtonColor = () => {
    if (options?.variant === "primary") return "primary";
    if (options?.variant === "warning") return "warning";
    return "error";
  };

  return (
    <ConfirmContext.Provider value={confirm}>
      {children}
      <Dialog
        open={open}
        onClose={() => handleClose(false)}
        PaperProps={{
          className: "rounded-[32px] p-6 max-w-sm w-full shadow-2xl border-none",
          style: { borderRadius: 28 },
        }}
      >
        <DialogTitle className="px-0 pb-2 text-xl font-black text-slate-800">{options?.title}</DialogTitle>
        <DialogContent className="px-0 py-2">
          <DialogContentText className="leading-relaxed font-semibold text-slate-500">
            {options?.message}
          </DialogContentText>
        </DialogContent>
        <DialogActions className="justify-end gap-3 px-0 pt-6">
          <Button
            variant="outlined"
            color="inherit"
            onClick={() => handleClose(false)}
            className="rounded-xl border-slate-200 px-4 py-2 font-bold text-slate-600 hover:bg-slate-50"
            style={{ borderRadius: 12 }}
          >
            {options?.cancelText || "Batal"}
          </Button>
          <Button
            variant="contained"
            color={getButtonColor()}
            onClick={() => handleClose(true)}
            className="rounded-xl px-5 py-2 font-black shadow-lg"
            style={{ borderRadius: 12 }}
            autoFocus
          >
            {options?.confirmText || "Setuju"}
          </Button>
        </DialogActions>
      </Dialog>
    </ConfirmContext.Provider>
  );
};

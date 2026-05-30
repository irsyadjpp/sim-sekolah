import React from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Button,
} from "@mui/material";

interface SPConfirmDialogProps {
  open: boolean;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm: () => void;
  onCancel: () => void;
  danger?: boolean;
}

const SPConfirmDialog: React.FC<SPConfirmDialogProps> = ({
  open,
  title,
  message,
  confirmText = "Ya",
  cancelText = "Batal",
  onConfirm,
  onCancel,
  danger = false,
}) => {
  return (
    <Dialog open={open} onClose={onCancel} maxWidth="sm" fullWidth>
      <DialogTitle className="font-semibold">{title}</DialogTitle>
      <DialogContent>
        <DialogContentText className="text-text-secondary">{message}</DialogContentText>
      </DialogContent>
      <DialogActions className="p-4 pt-0">
        <Button onClick={onCancel} color="primary">
          {cancelText}
        </Button>
        <Button
          onClick={onConfirm}
          color={danger ? "error" : "primary"}
          variant={danger ? "contained" : "outlined"}
          autoFocus
        >
          {confirmText}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default SPConfirmDialog;
import "@toast-ui/editor/dist/toastui-editor-viewer.css";

import { useEffect, useRef } from "react";

import { Viewer } from "@toast-ui/react-editor";

interface ToastViewerProps {
  value: string;
}

export default function ToastViewer({ value }: ToastViewerProps) {
  const viewerRef = useRef<any>(null);

  useEffect(() => {
    if (viewerRef.current) {
      viewerRef.current.getInstance().setMarkdown(value || "");
    }
  }, [value]);

  return <Viewer ref={viewerRef} initialValue={value || ""} />;
}

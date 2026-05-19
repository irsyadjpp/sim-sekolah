import "@toast-ui/editor/dist/toastui-editor.css";

import { useEffect, useRef } from "react";

import { Editor } from "@toast-ui/react-editor";

interface ToastEditorProps {
  value: string;
  onChange: (value: string) => void;
  height?: string;
  placeholder?: string;
}

export default function ToastEditor({ value, onChange, height = "300px", placeholder = "" }: ToastEditorProps) {
  const editorRef = useRef<any>(null);

  // Sync value from props to editor
  useEffect(() => {
    if (editorRef.current) {
      const instance = editorRef.current.getInstance();
      const currentHTML = instance.getHTML();

      // Only update if the value is different from what's currently in the editor
      // and it's not the same as the empty state
      if (value !== currentHTML && value !== undefined) {
        // If the editor is empty and value is empty, don't force setHTML to avoid loops or unnecessary resets
        if (value === "" && (currentHTML === "<p><br></p>" || currentHTML === "")) {
          return;
        }
        instance.setHTML(value || "");
      }
    }
  }, [value]);

  const handleChange = () => {
    if (editorRef.current) {
      const instance = editorRef.current.getInstance();
      const html = instance.getHTML();
      // Only call onChange if the value actually changed
      if (html !== value) {
        onChange(html);
      }
    }
  };

  return (
    <Editor
      ref={editorRef}
      initialValue={value || ""}
      previewStyle="vertical"
      height={height}
      initialEditType="wysiwyg"
      useCommandShortcut={true}
      placeholder={placeholder}
      onChange={handleChange}
      toolbarItems={[
        ["heading", "bold", "italic", "strike"],
        ["hr", "quote"],
        ["ul", "ol", "task", "indent", "outdent"],
        ["table", "image", "link"],
        ["code", "codeblock"],
      ]}
    />
  );
}


import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { toast } from "sonner";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  accept?: Record<string, string[]>;
  label: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, accept, label }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
      toast.success("File uploaded successfully");
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    maxFiles: 1,
  });

  return (
    <div
      {...getRootProps()}
      className={`file-drop-area ${
        isDragActive ? "dragging" : ""
      } cursor-pointer hover:border-primary/50`}
    >
      <input {...getInputProps()} />
      <div className="text-center">
        <p className="text-sm text-muted-foreground mb-2">{label}</p>
        <p className="text-xs text-muted-foreground">
          Drag & drop or click to select
        </p>
      </div>
    </div>
  );
};

export default FileUpload;

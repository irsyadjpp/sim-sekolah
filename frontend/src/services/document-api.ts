import { apiClient, translateUrl } from "@/lib/api-client";

// Document Types
export interface Document {
  id: string;
  title: string;
  description: string;
  document_number: string;
  category: string;
  document_type: string;
  status: string;
  access_level: string;
  file_url: string;
  file_name: string;
  file_size: number;
  file_hash: string;
  mime_type: string;
  author_id: string;
  school_id: string;
  tags: string;
  version: number;
  is_current_version: boolean;
  created_at: string;
  updated_at: string;
}

export interface DocumentUploadRequest {
  title: string;
  description: string;
  document_number: string;
  category: string;
  document_type: string;
  access_level: string;
  file: File;
}

export interface DocumentUploadResponse {
  status: string;
  message: string;
  data: Document;
}

export interface DuplicateCheckRequest {
  title?: string;
  document_number?: string;
  file_hash?: string;
}

export interface DuplicateCheckResponse {
  status: string;
  message: string;
  isDuplicate: boolean;
  data?: Document;
}

export interface DocumentListResponse {
  status: string;
  message: string;
  data: Document[];
  total: number;
  page: number;
  limit: number;
}

// Document Categories
export const DOCUMENT_CATEGORIES = {
  GENERAL: "GENERAL",
  ACCREDITATION: "ACCREDITATION",
  CURRICULUM: "CURRICULUM",
  ASSESSMENT: "ASSESSMENT",
  ADMINISTRATION: "ADMINISTRATION",
  FINANCE: "FINANCE",
  HR: "HR",
  LEGAL: "LEGAL",
  STUDENT: "STUDENT",
  TEACHER: "TEACHER",
  POLICY: "POLICY",
  REPORT: "REPORT",
} as const;

export const DOCUMENT_TYPES = {
  PDF: "PDF",
  DOC: "DOC",
  DOCX: "DOCX",
  XLS: "XLS",
  XLSX: "XLSX",
  PPT: "PPT",
  PPTX: "PPTX",
  IMAGE: "IMAGE",
  VIDEO: "VIDEO",
  AUDIO: "AUDIO",
  ARCHIVE: "ARCHIVE",
  OTHER: "OTHER",
} as const;

export const ACCESS_LEVELS = {
  PUBLIC: "PUBLIC",
  INTERNAL: "INTERNAL",
  PRIVATE: "PRIVATE",
  RESTRICTED: "RESTRICTED",
} as const;

// Document API Functions
export const documentApi = {
  // Upload document with file and metadata
  uploadDocument: async (formData: FormData): Promise<DocumentUploadResponse> => {
    const response = await apiClient.post<DocumentUploadResponse>(
      translateUrl("/api/documents/upload"),
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data;
  },

  // Check for duplicate documents
  checkDuplicate: async (request: DuplicateCheckRequest): Promise<DuplicateCheckResponse> => {
    const response = await apiClient.post<DuplicateCheckResponse>(
      translateUrl("/api/documents/check-duplicate"),
      request
    );
    return response.data;
  },

  // Get documents list
  getDocuments: async (params?: {
    category?: string;
    document_type?: string;
    status?: string;
    access_level?: string;
    search?: string;
    page?: number;
    limit?: number;
    sort_by?: string;
    sort_order?: string;
  }): Promise<DocumentListResponse> => {
    const response = await apiClient.get<DocumentListResponse>(
      translateUrl("/api/documents"),
      { params }
    );
    return response.data;
  },

  // Get document by ID
  getDocumentById: async (id: string): Promise<{ status: string; message: string; data: Document }> => {
    const response = await apiClient.get<{ status: string; message: string; data: Document }>(
      translateUrl(`/api/documents/${id}`)
    );
    return response.data;
  },

  // Update document
  updateDocument: async (
    id: string,
    data: Partial<Document>
  ): Promise<{ status: string; message: string; data: Document }> => {
    const response = await apiClient.put<{ status: string; message: string; data: Document }>(
      translateUrl(`/api/documents/${id}`),
      data
    );
    return response.data;
  },

  // Delete document
  deleteDocument: async (id: string): Promise<{ status: string; message: string }> => {
    const response = await apiClient.delete<{ status: string; message: string }>(
      translateUrl(`/api/documents/${id}`)
    );
    return response.data;
  },

  // Download document
  downloadDocument: async (id: string): Promise<Blob> => {
    const response = await apiClient.get(translateUrl(`/api/documents/${id}/download`), {
      responseType: "blob",
    });
    return response.data;
  },

  // Helper function to determine document type from MIME type
  getDocumentTypeFromMimeType: (mimeType: string): string => {
    if (mimeType.includes("pdf")) return DOCUMENT_TYPES.PDF;
    if (mimeType.includes("word") || mimeType.includes("doc")) {
      return mimeType.includes("docx") ? DOCUMENT_TYPES.DOCX : DOCUMENT_TYPES.DOC;
    }
    if (mimeType.includes("excel") || mimeType.includes("sheet")) {
      return mimeType.includes("xlsx") ? DOCUMENT_TYPES.XLSX : DOCUMENT_TYPES.XLS;
    }
    if (mimeType.includes("powerpoint") || mimeType.includes("presentation")) {
      return mimeType.includes("pptx") ? DOCUMENT_TYPES.PPTX : DOCUMENT_TYPES.PPT;
    }
    if (mimeType.includes("image")) return DOCUMENT_TYPES.IMAGE;
    if (mimeType.includes("video")) return DOCUMENT_TYPES.VIDEO;
    if (mimeType.includes("audio")) return DOCUMENT_TYPES.AUDIO;

    return DOCUMENT_TYPES.OTHER;
  },

  // Helper function to format file size
  formatFileSize: (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";

    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
  },
};

// Helper function to calculate file hash client-side (optional)
export const calculateFileHash = async (file: File): Promise<string> => {
  const buffer = await file.arrayBuffer();
  const hashBuffer = await crypto.subtle.digest("SHA-256", buffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  return hashHex;
};

// Helper function to validate file before upload
export const validateFileForUpload = (file: File, maxSizeMB: number = 100): { valid: boolean; error?: string } => {
  const maxSizeBytes = maxSizeMB * 1024 * 1024;

  if (file.size > maxSizeBytes) {
    return {
      valid: false,
      error: `File size exceeds ${maxSizeMB}MB limit`,
    };
  }

  const allowedTypes = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "image/jpeg",
    "image/png",
    "image/gif",
  ];

  if (!allowedTypes.includes(file.type)) {
    return {
      valid: false,
      error: "File type not supported",
    };
  }

  return { valid: true };
};

// Helper function to determine document type from MIME type
export const getDocumentTypeFromMimeType = (mimeType: string): string => {
  if (mimeType.includes("pdf")) return DOCUMENT_TYPES.PDF;
  if (mimeType.includes("word") || mimeType.includes("doc")) {
    return mimeType.includes("docx") ? DOCUMENT_TYPES.DOCX : DOCUMENT_TYPES.DOC;
  }
  if (mimeType.includes("excel") || mimeType.includes("sheet")) {
    return mimeType.includes("xlsx") ? DOCUMENT_TYPES.XLSX : DOCUMENT_TYPES.XLS;
  }
  if (mimeType.includes("powerpoint") || mimeType.includes("presentation")) {
    return mimeType.includes("pptx") ? DOCUMENT_TYPES.PPTX : DOCUMENT_TYPES.PPT;
  }
  if (mimeType.includes("image")) return DOCUMENT_TYPES.IMAGE;
  if (mimeType.includes("video")) return DOCUMENT_TYPES.VIDEO;
  if (mimeType.includes("audio")) return DOCUMENT_TYPES.AUDIO;

  return DOCUMENT_TYPES.OTHER;
};

// Helper function to format file size
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
};

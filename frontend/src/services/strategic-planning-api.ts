import { apiClient, translateUrl } from "@/lib/api-client";

// Types untuk Strategic Planning API
export interface RaporPendidikan {
  id: string;
  school_id: string;
  student_id: string;
  academic_year: string;
  semester: string;
  import_date: string;
  data_source: string;
  raw_data: any;
  processed_data: any;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Survey {
  id: string;
  title: string;
  description: string;
  survey_type: string;
  target_audience: string;
  questions: any[];
  status: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface SurveyResponse {
  id: string;
  survey_id: string;
  respondent_id: string;
  responses: any[];
  submitted_at: string;
}

export interface FGDSession {
  id: string;
  title: string;
  description: string;
  scheduled_date: string;
  location: string;
  facilitator_id: string;
  participants: string[];
  agenda: string[];
  status: string;
  created_at: string;
  updated_at: string;
}

export interface StudentNeedsEnhanced {
  id: string;
  student_id: string;
  assessment_date: string;
  academic_needs: any;
  social_needs: any;
  emotional_needs: any;
  physical_needs: any;
  recommendations: string[];
  next_assessment_date: string;
  created_at: string;
  updated_at: string;
}

export interface SWOTItem {
  id: string;
  category: string; // STRENGTH, WEAKNESS, OPPORTUNITY, THREAT
  title: string;
  description: string;
  priority: number;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface RootCause {
  id: string;
  problem_statement: string;
  root_cause: string;
  contributing_factors: string[];
  analysis_method: string;
  verified: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface FishboneDiagram {
  id: string;
  title: string;
  problem_statement: string;
  central_cause: string;
  branches: any[];
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface KSPAnalysisIntegration {
  id: string;
  curriculum_document_id: string;
  analysis_type: string;
  data_sources: string[];
  recommendations: any[];
  integration_status: string;
  created_at: string;
  updated_at: string;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}

// Retry configuration
const RETRY_CONFIG = {
  maxRetries: 3,
  retryDelay: 1000,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
};

// Helper function untuk retry logic
async function withRetry<T>(
  fn: () => Promise<T>,
  retries = RETRY_CONFIG.maxRetries
): Promise<T> {
  try {
    return await fn();
  } catch (error: any) {
    if (
      retries > 0 &&
      RETRY_CONFIG.retryableStatuses.includes(error?.response?.status)
    ) {
      await new Promise((resolve) =>
        setTimeout(resolve, RETRY_CONFIG.retryDelay)
      );
      return withRetry(fn, retries - 1);
    }
    throw error;
  }
}

// Rapor Pendidikan API
export const raporPendidikanAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<RaporPendidikan>>(
          translateUrl("/api/v1/strategic-planning/rapor-pendidikan"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<RaporPendidikan>>(
          translateUrl(`/api/v1/strategic-planning/rapor-pendidikan/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<RaporPendidikan>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<RaporPendidikan>>(
          translateUrl("/api/v1/strategic-planning/rapor-pendidikan"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<RaporPendidikan>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<RaporPendidikan>>(
          translateUrl(`/api/v1/strategic-planning/rapor-pendidikan/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/rapor-pendidikan/${id}`)
        )
        .then((res) => res.data)
    );
  },

  getBySchool: async (schoolId: string, params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<RaporPendidikan>>(
          translateUrl(
            `/api/v1/strategic-planning/rapor-pendidikan/school/${schoolId}`
          ),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getByStudent: async (studentId: string, params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<RaporPendidikan>>(
          translateUrl(
            `/api/v1/strategic-planning/rapor-pendidikan/student/${studentId}`
          ),
          { params }
        )
        .then((res) => res.data)
    );
  },
};

// Survey API
export const surveyAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<Survey>>(
          translateUrl("/api/v1/strategic-planning/surveys"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<Survey>>(
          translateUrl(`/api/v1/strategic-planning/surveys/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<Survey>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<Survey>>(
          translateUrl("/api/v1/strategic-planning/surveys"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<Survey>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<Survey>>(
          translateUrl(`/api/v1/strategic-planning/surveys/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/surveys/${id}`)
        )
        .then((res) => res.data)
    );
  },

  submitResponse: async (surveyId: string, data: Partial<SurveyResponse>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<SurveyResponse>>(
          translateUrl(
            `/api/v1/strategic-planning/surveys/${surveyId}/responses`
          ),
          data
        )
        .then((res) => res.data)
    );
  },

  getAnalytics: async (surveyId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/surveys/${surveyId}/analytics`)
        )
        .then((res) => res.data)
    );
  },

  distribute: async (surveyId: string, data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/surveys/${surveyId}/distribute`),
          data
        )
        .then((res) => res.data)
    );
  },

  getResponses: async (surveyId: string, params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<SurveyResponse>>(
          translateUrl(`/api/v1/strategic-planning/surveys/${surveyId}/responses`),
          { params }
        )
        .then((res) => res.data)
    );
  },
};

// FGD Session API
export const fgdAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<FGDSession>>(
          translateUrl("/api/v1/strategic-planning/fgd-sessions"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<FGDSession>>(
          translateUrl(`/api/v1/strategic-planning/fgd-sessions/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<FGDSession>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<FGDSession>>(
          translateUrl("/api/v1/strategic-planning/fgd-sessions"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<FGDSession>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<FGDSession>>(
          translateUrl(`/api/v1/strategic-planning/fgd-sessions/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/fgd-sessions/${id}`)
        )
        .then((res) => res.data)
    );
  },

  addParticipant: async (sessionId: string, userId: string) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(
            `/api/v1/strategic-planning/fgd-sessions/${sessionId}/participants`
          ),
          { user_id: userId }
        )
        .then((res) => res.data)
    );
  },

  removeParticipant: async (sessionId: string, userId: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(
            `/api/v1/strategic-planning/fgd-sessions/${sessionId}/participants/${userId}`
          )
        )
        .then((res) => res.data)
    );
  },

  uploadMinutes: async (sessionId: string, data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fgd-sessions/${sessionId}/minutes`),
          data
        )
        .then((res) => res.data)
    );
  },
};

// Student Needs API
export const studentNeedsAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<StudentNeedsEnhanced>>(
          translateUrl("/api/v1/strategic-planning/student-needs"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<StudentNeedsEnhanced>>(
          translateUrl(`/api/v1/strategic-planning/student-needs/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<StudentNeedsEnhanced>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<StudentNeedsEnhanced>>(
          translateUrl("/api/v1/strategic-planning/student-needs"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<StudentNeedsEnhanced>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<StudentNeedsEnhanced>>(
          translateUrl(`/api/v1/strategic-planning/student-needs/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/student-needs/${id}`)
        )
        .then((res) => res.data)
    );
  },

  getByStudent: async (studentId: string, params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<StudentNeedsEnhanced>>(
          translateUrl(
            `/api/v1/strategic-planning/student-needs/student/${studentId}`
          ),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getHistory: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/student-needs/${id}/history`)
        )
        .then((res) => res.data)
    );
  },

  scheduleAssessment: async (id: string, data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/student-needs/${id}/next-assessment`),
          data
        )
        .then((res) => res.data)
    );
  },
};

// SWOT API
export const swotAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<SWOTItem>>(
          translateUrl("/api/v1/strategic-planning/swot-items"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<SWOTItem>>(
          translateUrl(`/api/v1/strategic-planning/swot-items/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<SWOTItem>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<SWOTItem>>(
          translateUrl("/api/v1/strategic-planning/swot-items"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<SWOTItem>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<SWOTItem>>(
          translateUrl(`/api/v1/strategic-planning/swot-items/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/swot-items/${id}`)
        )
        .then((res) => res.data)
    );
  },

  createSession: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/swot-sessions"),
          data
        )
        .then((res) => res.data)
    );
  },

  getSession: async (sessionId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/swot-sessions/${sessionId}`)
        )
        .then((res) => res.data)
    );
  },

  updateSession: async (sessionId: string, data: any) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/swot-sessions/${sessionId}`),
          data
        )
        .then((res) => res.data)
    );
  },

  getSessionReport: async (sessionId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/swot-sessions/${sessionId}/report`)
        )
        .then((res) => res.data)
    );
  },

  // FASE 5: Analysis Tool Enhancements

  getAnalyticsAggregation: async (sessionId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/swot/sessions/${sessionId}/analytics`)
        )
        .then((res) => res.data)
    );
  },

  mapDataToItem: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/swot/map-data"),
          data
        )
        .then((res) => res.data)
    );
  },

  getAvailableDataSources: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/swot/school/${schoolId}/data-sources`)
        )
        .then((res) => res.data)
    );
  },

  exportAnalysis: async (sessionId: string, format: "json" | "csv") => {
    return withRetry(() =>
      apiClient
        .get<any>(
          translateUrl(`/api/v1/strategic-planning/swot/sessions/${sessionId}/export`),
          {
            params: { format },
            responseType: "blob",
          }
        )
        .then((res) => res.data)
    );
  },
};

// Root Cause API
export const rootCauseAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<RootCause>>(
          translateUrl("/api/v1/strategic-planning/root-causes"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<RootCause>>(
          translateUrl(`/api/v1/strategic-planning/root-causes/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<RootCause>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<RootCause>>(
          translateUrl("/api/v1/strategic-planning/root-causes"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<RootCause>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<RootCause>>(
          translateUrl(`/api/v1/strategic-planning/root-causes/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/root-causes/${id}`)
        )
        .then((res) => res.data)
    );
  },

  getHistory: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/root-causes/${id}/history`)
        )
        .then((res) => res.data)
    );
  },

  // FASE 5: Analysis Tool Enhancements

  perform5WhysAnalysis: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/root-cause/5-whys"),
          data
        )
        .then((res) => res.data)
    );
  },

  linkRaporMetric: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<void>>(
          translateUrl("/api/v1/strategic-planning/root-cause/link-rapor-metric"),
          data
        )
        .then((res) => res.data)
    );
  },

  getSuggestions: async (rootCauseId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/root-cause/${rootCauseId}/suggestions`)
        )
        .then((res) => res.data)
    );
  },

  exportAnalysis: async (rootCauseId: string, format: "json" | "csv") => {
    return withRetry(() =>
      apiClient
        .get<any>(
          translateUrl(`/api/v1/strategic-planning/root-cause/${rootCauseId}/export`),
          {
            params: { format },
            responseType: "blob",
          }
        )
        .then((res) => res.data)
    );
  },
};

// Fishbone API
export const fishboneAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<FishboneDiagram>>(
          translateUrl("/api/v1/strategic-planning/fishbone-diagrams"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<FishboneDiagram>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-diagrams/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<FishboneDiagram>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<FishboneDiagram>>(
          translateUrl("/api/v1/strategic-planning/fishbone-diagrams"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<FishboneDiagram>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<FishboneDiagram>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-diagrams/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-diagrams/${id}`)
        )
        .then((res) => res.data)
    );
  },

  addNode: async (diagramId: string, data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-diagrams/${diagramId}/nodes`),
          data
        )
        .then((res) => res.data)
    );
  },

  addConnection: async (diagramId: string, data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-diagrams/${diagramId}/connections`),
          data
        )
        .then((res) => res.data)
    );
  },

  // FASE 5: Analysis Tool Enhancements

  getAnalytics: async (diagramId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fishbone/diagrams/${diagramId}/analytics`)
        )
        .then((res) => res.data)
    );
  },

  validateStructure: async (diagramId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fishbone/diagrams/${diagramId}/validate`)
        )
        .then((res) => res.data)
    );
  },

  getCategories: async () => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/fishbone/categories")
        )
        .then((res) => res.data)
    );
  },

  exportDiagram: async (diagramId: string, format: "json" | "csv") => {
    return withRetry(() =>
      apiClient
        .get<any>(
          translateUrl(`/api/v1/strategic-planning/fishbone/diagrams/${diagramId}/export`),
          {
            params: { format },
            responseType: "blob",
          }
        )
        .then((res) => res.data)
    );
  },

  // Fishbone Template Management (T-5.3.14)

  createTemplate: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/fishbone-templates"),
          data
        )
        .then((res) => res.data)
    );
  },

  getTemplateById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-templates/${id}`)
        )
        .then((res) => res.data)
    );
  },

  getPublicTemplates: async (category?: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/fishbone-templates/public"),
          { params: { category } }
        )
        .then((res) => res.data)
    );
  },

  getTemplatesBySchool: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-templates/school/${schoolId}`)
        )
        .then((res) => res.data)
    );
  },

  updateTemplate: async (id: string, data: any) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-templates/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  deleteTemplate: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-templates/${id}`)
        )
        .then((res) => res.data)
    );
  },

  incrementTemplateUsage: async (id: string) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/fishbone-templates/${id}/increment-usage`)
        )
        .then((res) => res.data)
    );
  },

  applyTemplate: async (templateId: string, diagramId: string) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/fishbone/fishbone-templates/${templateId}/apply/${diagramId}`)
        )
        .then((res) => res.data)
    );
  },

  // FASE 6: KSP Enhanced Generation

  // Document Compilation (FR 4.1.1)
  compileDocumentWithAnalysis: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/document-compilation/compile"),
          data
        )
        .then((res) => res.data)
    );
  },

  generateAnalysisSnapshot: async (integrationId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/document-compilation/snapshot/${integrationId}`)
        )
        .then((res) => res.data)
    );
  },

  // KSP Analysis Template Management (FR 4.1.2)
  createKSPTemplate: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/ksp-templates"),
          data
        )
        .then((res) => res.data)
    );
  },

  getKSPTemplateById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-templates/${id}`)
        )
        .then((res) => res.data)
    );
  },

  getPublicKSPTemplates: async (category?: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/ksp-templates/public"),
          { params: { category } }
        )
        .then((res) => res.data)
    );
  },

  getKSPTemplatesBySchool: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-templates/school/${schoolId}`)
        )
        .then((res) => res.data)
    );
  },

  updateKSPTemplate: async (id: string, data: any) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-templates/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  deleteKSPTemplate: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/ksp-templates/${id}`)
        )
        .then((res) => res.data)
    );
  },

  incrementKSPTemplateUsage: async (id: string) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/ksp-templates/${id}/increment-usage`)
        )
        .then((res) => res.data)
    );
  },

  // KSP Analysis Integration (FR 4.1.6)
  createKSPIntegration: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/ksp-integration"),
          data
        )
        .then((res) => res.data)
    );
  },

  getKSPIntegrationById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/${id}`)
        )
        .then((res) => res.data)
    );
  },

  getKSPIntegrationsByDocument: async (documentId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/document/${documentId}`)
        )
        .then((res) => res.data)
    );
  },

  updateKSPIntegration: async (id: string, data: any) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  deleteKSPIntegration: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/${id}`)
        )
        .then((res) => res.data)
    );
  },

  approveKSPIntegration: async (id: string, data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/${id}/approve`),
          data
        )
        .then((res) => res.data)
    );
  },

  // KSP Analysis Recommendations
  createKSPRecommendation: async (data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl("/api/v1/strategic-planning/ksp-integration/:id/recommendations"),
          data
        )
        .then((res) => res.data)
    );
  },

  getKSPRecommendations: async (integrationId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/${integrationId}/recommendations`)
        )
        .then((res) => res.data)
    );
  },

  updateKSPRecommendation: async (id: string, data: any) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/recommendations/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  deleteKSPRecommendation: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integration/recommendations/${id}`)
        )
        .then((res) => res.data)
    );
  },
};

// KSP Integration API
export const kspIntegrationAPI = {
  getAll: async (params?: any) => {
    return withRetry(() =>
      apiClient
        .get<PaginatedResponse<KSPAnalysisIntegration>>(
          translateUrl("/api/v1/strategic-planning/ksp-integrations"),
          { params }
        )
        .then((res) => res.data)
    );
  },

  getById: async (id: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<KSPAnalysisIntegration>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integrations/${id}`)
        )
        .then((res) => res.data)
    );
  },

  create: async (data: Partial<KSPAnalysisIntegration>) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<KSPAnalysisIntegration>>(
          translateUrl("/api/v1/strategic-planning/ksp-integrations"),
          data
        )
        .then((res) => res.data)
    );
  },

  update: async (id: string, data: Partial<KSPAnalysisIntegration>) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<KSPAnalysisIntegration>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integrations/${id}`),
          data
        )
        .then((res) => res.data)
    );
  },

  delete: async (id: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integrations/${id}`)
        )
        .then((res) => res.data)
    );
  },

  generateRecommendations: async (integrationId: string, data: any) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/ksp-integrations/${integrationId}/recommendations`),
          data
        )
        .then((res) => res.data)
    );
  },
};

// FASE 4: Integration APIs
export const localContextAPI = {
  getLocalContextForSWOT: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/local-context/school/${schoolId}/swot`)
        )
        .then((res) => res.data)
    );
  },
  analyzeLearningPotential: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/local-context/school/${schoolId}/learning-potential`)
        )
        .then((res) => res.data)
    );
  },
  getEnhancedLocalCategories: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/local-context/school/${schoolId}/categories-enhanced`)
        )
        .then((res) => res.data)
    );
  },
};

export const analyticsAPI = {
  getSurveyAnalyticsAggregated: async (schoolId: string, surveyId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/analytics/school/${schoolId}/surveys/${surveyId}/aggregated`)
        )
        .then((res) => res.data)
    );
  },
  getStudentProfileAnalysis: async (schoolId: string, profileDimension?: string) => {
    const params = profileDimension ? `?profile_dimension=${profileDimension}` : '';
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/analytics/school/${schoolId}/student-profile${params}`)
        )
        .then((res) => res.data)
    );
  },
  getStatisticalAnalysis: async (schoolId: string, analysisType?: string) => {
    const params = analysisType ? `?analysis_type=${analysisType}` : '';
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/analytics/school/${schoolId}/statistical${params}`)
        )
        .then((res) => res.data)
    );
  },
  generateActionPlanRecommendations: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/analytics/school/${schoolId}/action-plans`)
        )
        .then((res) => res.data)
    );
  },
};

export const schoolDataAPI = {
  getSchoolDataForSWOT: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/school-data/${schoolId}/swot`)
        )
        .then((res) => res.data)
    );
  },
  getDigitalReadinessAssessment: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/school-data/${schoolId}/digital-readiness`)
        )
        .then((res) => res.data)
    );
  },
  getSarprasPrioritization: async (schoolId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/school-data/${schoolId}/sarpras-prioritization`)
        )
        .then((res) => res.data)
    );
  },
};

// FASE 6: Chart Generation API (FR 4.1.3)
export const chartGenerationAPI = {
  generateSWOTChart: async (data: any, chartType?: string) => {
    const params = chartType ? `?type=${chartType}` : '';
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/charts/swot${params}`),
          data
        )
        .then((res) => res.data)
    );
  },
  generateRootCauseChart: async (data: any, chartType?: string) => {
    const params = chartType ? `?type=${chartType}` : '';
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/charts/root-cause${params}`),
          data
        )
        .then((res) => res.data)
    );
  },
  generateFishboneChart: async (data: any, chartType?: string) => {
    const params = chartType ? `?type=${chartType}` : '';
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/charts/fishbone${params}`),
          data
        )
        .then((res) => res.data)
    );
  },
  generateStudentNeedsChart: async (data: any, chartType?: string) => {
    const params = chartType ? `?type=${chartType}` : '';
    return withRetry(() =>
      apiClient
        .post<ApiResponse<any>>(
          translateUrl(`/api/v1/strategic-planning/charts/student-needs${params}`),
          data
        )
        .then((res) => res.data)
    );
  },
};

// FASE 6: AI Platform Integration API (FR 4.1.4)
export interface AIContentGenerationRequest {
  integration_id: string;
  content_type: string; // EXECUTIVE_SUMMARY, ANALYSIS_SECTION, RECOMMENDATION, ACTION_PLAN
  context?: Record<string, any>;
  tone?: string; // FORMAL, SEMI_FORMAL, CASUAL
  language?: string;
  max_length?: number;
}

export interface AIContentGenerationResponse {
  generated_content: string;
  content_id: string;
  confidence: number;
  word_count: number;
  tokens_used: number;
  generated_at: string;
}

export interface AIRecommendationRequest {
  analysis_data: Record<string, any>;
  recommendation_type: string; // SWOT_ACTION, ROOT_CAUSE_SOLUTION, GENERAL
  target_audience?: string;
  priority?: string;
  context?: string;
}

export interface AIRecommendationResponse {
  recommendations: string[];
  confidence: number;
  sources: string[];
  generated_at: string;
}

export interface AIIntegrationConfig {
  api_endpoint: string;
  api_key: string;
  model_version: string;
  max_tokens: number;
  temperature: number;
  timeout: number;
  enabled: boolean;
}

export const aiIntegrationAPI = {
  generateContent: async (req: AIContentGenerationRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<AIContentGenerationResponse>>(
          translateUrl("/api/v1/strategic-planning/ai/generate-content"),
          req
        )
        .then((res) => res.data)
    );
  },
  generateRecommendations: async (req: AIRecommendationRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<AIRecommendationResponse>>(
          translateUrl("/api/v1/strategic-planning/ai/generate-recommendations"),
          req
        )
        .then((res) => res.data)
    );
  },
  getConfig: async () => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<AIIntegrationConfig>>(
          translateUrl("/api/v1/strategic-planning/ai/config")
        )
        .then((res) => res.data)
    );
  },
  updateConfig: async (config: AIIntegrationConfig) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<void>>(
          translateUrl("/api/v1/strategic-planning/ai/config"),
          config
        )
        .then((res) => res.data)
    );
  },
};

// FASE 6: Version History API (FR 4.1.5)
export interface AnalysisVersionHistory {
  id: string;
  analysis_type: string;
  analysis_id: string;
  version: number;
  changes: Record<string, any>;
  change_type: string;
  change_summary: string;
  changed_by: string;
  changed_at: string;
  previous_data?: Record<string, any>;
  new_data?: Record<string, any>;
}

export interface AnalysisVersionHistoryRequest {
  analysis_type: string;
  analysis_id: string;
  changes?: Record<string, any>;
  change_type: string;
  change_summary: string;
  previous_data?: Record<string, any>;
  new_data?: Record<string, any>;
}

export interface AnalysisVersionComparison {
  version_1: AnalysisVersionHistory;
  version_2: AnalysisVersionHistory;
  differences: string[];
  summary: string;
}

export interface VersionRestoreRequest {
  analysis_id: string;
  version: number;
  reason: string;
}

export const versionHistoryAPI = {
  create: async (req: AnalysisVersionHistoryRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<AnalysisVersionHistory>>(
          translateUrl("/api/v1/strategic-planning/version-history"),
          req
        )
        .then((res) => res.data)
    );
  },
  getByAnalysis: async (analysisId: string, analysisType?: string) => {
    const params = analysisType ? `?type=${analysisType}` : '';
    return withRetry(() =>
      apiClient
        .get<ApiResponse<AnalysisVersionHistory[]>>(
          translateUrl(`/api/v1/strategic-planning/version-history/analysis/${analysisId}${params}`)
        )
        .then((res) => res.data)
    );
  },
  getByID: async (versionId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<AnalysisVersionHistory>>(
          translateUrl(`/api/v1/strategic-planning/version-history/${versionId}`)
        )
        .then((res) => res.data)
    );
  },
  compare: async (analysisId: string, version1: number, version2: number) => {
    const params = `?version1=${version1}&version2=${version2}`;
    return withRetry(() =>
      apiClient
        .get<ApiResponse<AnalysisVersionComparison>>(
          translateUrl(`/api/v1/strategic-planning/version-history/compare/${analysisId}${params}`)
        )
        .then((res) => res.data)
    );
  },
  restore: async (req: VersionRestoreRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<void>>(
          translateUrl("/api/v1/strategic-planning/version-history/restore"),
          req
        )
        .then((res) => res.data)
    );
  },
};

// FASE 6: Extended Review and Approval Workflow API (FR 4.1.13)
export interface ApprovalWorkflowStep {
  id: string;
  step_name: string;
  order: number;
  required: boolean;
  approver_role: string;
  description: string;
}

export interface ApprovalWorkflow {
  id: string;
  workflow_name: string;
  workflow_type: string;
  steps: ApprovalWorkflowStep[];
  is_active: boolean;
  school_id?: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface ApprovalWorkflowRequest {
  workflow_name: string;
  workflow_type: string;
  steps: ApprovalWorkflowStep[];
  school_id?: string;
}

export interface ApprovalRequest {
  document_id: string;
  workflow_id: string;
  step_id: string;
  action: string; // APPROVE, REJECT, REQUEST_CHANGES
  comments: string;
  requested_changes?: string;
}

export interface ApprovalResponse {
  id: string;
  document_id: string;
  workflow_id: string;
  step_id: string;
  action: string;
  approver_id: string;
  comments: string;
  requested_changes?: string;
  approved_at: string;
}

export interface DocumentApprovalStatus {
  document_id: string;
  current_step: string;
  current_step_name: string;
  overall_status: string; // PENDING, IN_PROGRESS, APPROVED, REJECTED
  completed_steps: string[];
  pending_steps: string[];
  approval_history: ApprovalResponse[];
  started_at: string;
  completed_at?: string;
}

export interface WorkflowStepAssignment {
  id: string;
  workflow_id: string;
  step_id: string;
  document_id: string;
  assigned_to: string;
  assigned_by: string;
  assigned_at: string;
  status: string; // PENDING, COMPLETED, SKIPPED
  completed_at?: string;
}

export interface ApprovalNotification {
  id: string;
  recipient_id: string;
  document_id: string;
  workflow_id: string;
  step_id: string;
  message: string;
  type: string; // APPROVAL_REQUIRED, APPROVED, REJECTED, CHANGES_REQUESTED
  sent_at: string;
  read_at?: string;
}

export const approvalWorkflowAPI = {
  create: async (req: ApprovalWorkflowRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<ApprovalWorkflow>>(
          translateUrl("/api/v1/strategic-planning/approval-workflows"),
          req
        )
        .then((res) => res.data)
    );
  },
  getByID: async (workflowId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<ApprovalWorkflow>>(
          translateUrl(`/api/v1/strategic-planning/approval-workflows/${workflowId}`)
        )
        .then((res) => res.data)
    );
  },
  getBySchool: async (schoolId: string, workflowType?: string) => {
    const params = workflowType ? `?type=${workflowType}` : '';
    return withRetry(() =>
      apiClient
        .get<ApiResponse<ApprovalWorkflow[]>>(
          translateUrl(`/api/v1/strategic-planning/approval-workflows/school/${schoolId}${params}`)
        )
        .then((res) => res.data)
    );
  },
  update: async (workflowId: string, req: ApprovalWorkflowRequest) => {
    return withRetry(() =>
      apiClient
        .put<ApiResponse<ApprovalWorkflow>>(
          translateUrl(`/api/v1/strategic-planning/approval-workflows/${workflowId}`),
          req
        )
        .then((res) => res.data)
    );
  },
  delete: async (workflowId: string) => {
    return withRetry(() =>
      apiClient
        .delete<ApiResponse<void>>(
          translateUrl(`/api/v1/strategic-planning/approval-workflows/${workflowId}`)
        )
        .then((res) => res.data)
    );
  },
};

export const approvalAPI = {
  submit: async (documentId: string, workflowId: string) => {
    const params = workflowId ? `?workflowId=${workflowId}` : '';
    return withRetry(() =>
      apiClient
        .post<ApiResponse<DocumentApprovalStatus>>(
          translateUrl(`/api/v1/strategic-planning/approvals/submit/${documentId}${params}`)
        )
        .then((res) => res.data)
    );
  },
  process: async (req: ApprovalRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<ApprovalResponse>>(
          translateUrl("/api/v1/strategic-planning/approvals/process"),
          req
        )
        .then((res) => res.data)
    );
  },
  getStatus: async (documentId: string) => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<DocumentApprovalStatus>>(
          translateUrl(`/api/v1/strategic-planning/approvals/status/${documentId}`)
        )
        .then((res) => res.data)
    );
  },
  assignStep: async (req: WorkflowStepAssignment) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<WorkflowStepAssignment>>(
          translateUrl("/api/v1/strategic-planning/approvals/assign"),
          req
        )
        .then((res) => res.data)
    );
  },
  getPending: async () => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<DocumentApprovalStatus[]>>(
          translateUrl("/api/v1/strategic-planning/approvals/pending")
        )
        .then((res) => res.data)
    );
  },
  sendNotification: async (notification: ApprovalNotification) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<void>>(
          translateUrl("/api/v1/strategic-planning/approvals/notifications"),
          notification
        )
        .then((res) => res.data)
    );
  },
  getNotifications: async () => {
    return withRetry(() =>
      apiClient
        .get<ApiResponse<ApprovalNotification[]>>(
          translateUrl("/api/v1/strategic-planning/approvals/notifications")
        )
        .then((res) => res.data)
    );
  },
};

// FASE 6: Curriculum Integration API (FR 4.2.1-4.2.5)
export interface SWOTDataForKSP {
  session_id: string;
  session_name: string;
  strengths: SWOTItem[];
  weaknesses: SWOTItem[];
  opportunities: SWOTItem[];
  threats: SWOTItem[];
  analysis_date: string;
}

export interface SWOTItem {
  id: string;
  description: string;
  quadrant: string;
  priority: string;
}

export interface RootCauseDataForKSP {
  root_cause_id: string;
  problem_statement: string;
  root_causes: RootCauseItem[];
  five_whys_analysis: FiveWhysStep[];
  solutions: SolutionItem[];
  analysis_date: string;
}

export interface RootCauseItem {
  id: string;
  cause: string;
  category: string;
  impact_level: string;
}

export interface FiveWhysStep {
  step_number: number;
  question: string;
  answer: string;
}

export interface SolutionItem {
  id: string;
  description: string;
  status: string;
  deadline: string;
}

export interface FishboneDataForKSP {
  diagram_id: string;
  diagram_name: string;
  problem_statement: string;
  categories: FishboneCategory[];
  analysis_date: string;
}

export interface FishboneCategory {
  category_name: string;
  nodes: FishboneNode[];
}

export interface FishboneNode {
  id: string;
  text: string;
  cause_level: number;
}

export interface StudentNeedsDataForKSP {
  profile_id: string;
  profile_name: string;
  profile_dimension: string;
  needs: StudentNeedItem[];
  priority_distribution: Record<string, number>;
  analysis_date: string;
}

export interface StudentNeedItem {
  id: string;
  need: string;
  category: string;
  priority: string;
  impact_level: string;
}

export interface AnalysisDataIntegrationRequest {
  curriculum_document_id: string;
  include_swot: boolean;
  include_root_cause: boolean;
  include_fishbone: boolean;
  include_student_needs: boolean;
  swot_session_id?: string;
  root_cause_id?: string;
  fishbone_diagram_id?: string;
  student_needs_profile_id?: string;
  customizations?: Record<string, any>;
}

export interface AnalysisDataIntegrationResponse {
  curriculum_document_id: string;
  integration_id: string;
  analysis_data: AnalysisDataSummary;
  generated_content: GeneratedContent;
  status: string;
  message: string;
}

export interface AnalysisDataSummary {
  swot_data?: SWOTDataForKSP;
  root_cause_data?: RootCauseDataForKSP;
  fishbone_data?: FishboneDataForKSP;
  student_needs_data?: StudentNeedsDataForKSP;
}

export interface GeneratedContent {
  executive_summary: string;
  analysis_section: string;
  recommendations: string[];
  action_plan: string;
  charts: Record<string, string>;
}

export interface KSPExportWithAnalysisRequest {
  curriculum_document_id: string;
  format: string; // PDF or WORD
  include_analysis_data: boolean;
  analysis_integration_id?: string;
  customizations?: Record<string, any>;
}

export interface KSPExportWithAnalysisResponse {
  export_id: string;
  document_url: string;
  format: string;
  file_size: number;
  generated_at: string;
  expires_at: string;
}

export const curriculumIntegrationAPI = {
  integrateSWOTData: async (req: AnalysisDataIntegrationRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<AnalysisDataIntegrationResponse>>(
          translateUrl("/api/v1/dokumen-kurikulum/analysis-integration/swot"),
          req
        )
        .then((res) => res.data)
    );
  },
  integrateRootCauseData: async (req: AnalysisDataIntegrationRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<AnalysisDataIntegrationResponse>>(
          translateUrl("/api/v1/dokumen-kurikulum/analysis-integration/root-cause"),
          req
        )
        .then((res) => res.data)
    );
  },
  integrateFishboneData: async (req: AnalysisDataIntegrationRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<AnalysisDataIntegrationResponse>>(
          translateUrl("/api/v1/dokumen-kurikulum/analysis-integration/fishbone"),
          req
        )
        .then((res) => res.data)
    );
  },
  integrateStudentNeedsData: async (req: AnalysisDataIntegrationRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<AnalysisDataIntegrationResponse>>(
          translateUrl("/api/v1/dokumen-kurikulum/analysis-integration/student-needs"),
          req
        )
        .then((res) => res.data)
    );
  },
  generateKSPWithAnalysis: async (req: KSPExportWithAnalysisRequest) => {
    return withRetry(() =>
      apiClient
        .post<ApiResponse<KSPExportWithAnalysisResponse>>(
          translateUrl("/api/v1/dokumen-kurikulum/analysis-integration/generate-ksp"),
          req
        )
        .then((res) => res.data)
    );
  },
};

// Request/Response Interceptors
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem("auth_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      window.location.href = "/auth/sign-in";
    } else if (error.response?.status === 403) {
      // Forbidden - show permission error
      console.error("Permission denied");
    } else if (error.response?.status >= 500) {
      // Server error - show error message
      console.error("Server error:", error.message);
    }
    return Promise.reject(error);
  }
);

// Export all APIs as a single object
export const strategicPlanningAPI = {
  raporPendidikan: raporPendidikanAPI,
  survey: surveyAPI,
  fgd: fgdAPI,
  studentNeeds: studentNeedsAPI,
  swot: swotAPI,
  rootCause: rootCauseAPI,
  fishbone: fishboneAPI,
  kspIntegration: kspIntegrationAPI,
  kspTemplates: kspTemplatesAPI,
  localContext: localContextAPI,
  analytics: analyticsAPI,
  schoolData: schoolDataAPI,
  chartGeneration: chartGenerationAPI,
  aiIntegration: aiIntegrationAPI,
  versionHistory: versionHistoryAPI,
  approvalWorkflow: approvalWorkflowAPI,
  approval: approvalAPI,
  curriculumIntegration: curriculumIntegrationAPI,
};
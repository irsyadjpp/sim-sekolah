import React, { createContext, useContext, useReducer, useCallback, ReactNode } from "react";
import { strategicPlanningAPI } from "@/services/strategic-planning-api";

// Types
import {
  RaporPendidikan,
  Survey,
  FGDSession,
  StudentNeedsEnhanced,
  SWOTItem,
  RootCause,
  FishboneDiagram,
  KSPAnalysisIntegration,
} from "@/services/strategic-planning-api";

// State Types
interface StrategicPlanningState {
  // Data Collection
  raporPendidikan: RaporPendidikan[];
  surveys: Survey[];
  fgdSessions: FGDSession[];

  // Analysis
  swotItems: SWOTItem[];
  rootCauses: RootCause[];
  fishboneDiagrams: FishboneDiagram[];

  // Student Needs
  studentNeeds: StudentNeedsEnhanced[];

  // KSP Integration
  kspIntegrations: KSPAnalysisIntegration[];

  // UI States
  loading: boolean;
  error: string | null;

  // Pagination
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Action Types
type StrategicPlanningAction =
  | { type: "SET_LOADING"; payload: boolean }
  | { type: "SET_ERROR"; payload: string | null }
  | { type: "SET_RAPOR_PENDIDIKAN"; payload: RaporPendidikan[] }
  | { type: "ADD_RAPOR_PENDIDIKAN"; payload: RaporPendidikan }
  | { type: "UPDATE_RAPOR_PENDIDIKAN"; payload: { id: string; data: Partial<RaporPendidikan> } }
  | { type: "DELETE_RAPOR_PENDIDIKAN"; payload: string }
  | { type: "SET_SURVEYS"; payload: Survey[] }
  | { type: "ADD_SURVEY"; payload: Survey }
  | { type: "UPDATE_SURVEY"; payload: { id: string; data: Partial<Survey> } }
  | { type: "DELETE_SURVEY"; payload: string }
  | { type: "SET_FGD_SESSIONS"; payload: FGDSession[] }
  | { type: "ADD_FGD_SESSION"; payload: FGDSession }
  | { type: "UPDATE_FGD_SESSION"; payload: { id: string; data: Partial<FGDSession> } }
  | { type: "DELETE_FGD_SESSION"; payload: string }
  | { type: "SET_SWOT_ITEMS"; payload: SWOTItem[] }
  | { type: "ADD_SWOT_ITEM"; payload: SWOTItem }
  | { type: "UPDATE_SWOT_ITEM"; payload: { id: string; data: Partial<SWOTItem> } }
  | { type: "DELETE_SWOT_ITEM"; payload: string }
  | { type: "SET_ROOT_CAUSES"; payload: RootCause[] }
  | { type: "ADD_ROOT_CAUSE"; payload: RootCause }
  | { type: "UPDATE_ROOT_CAUSE"; payload: { id: string; data: Partial<RootCause> } }
  | { type: "DELETE_ROOT_CAUSE"; payload: string }
  | { type: "SET_FISHBONE_DIAGRAMS"; payload: FishboneDiagram[] }
  | { type: "ADD_FISHBONE_DIAGRAM"; payload: FishboneDiagram }
  | { type: "UPDATE_FISHBONE_DIAGRAM"; payload: { id: string; data: Partial<FishboneDiagram> } }
  | { type: "DELETE_FISHBONE_DIAGRAM"; payload: string }
  | { type: "SET_STUDENT_NEEDS"; payload: StudentNeedsEnhanced[] }
  | { type: "ADD_STUDENT_NEEDS"; payload: StudentNeedsEnhanced }
  | { type: "UPDATE_STUDENT_NEEDS"; payload: { id: string; data: Partial<StudentNeedsEnhanced> } }
  | { type: "DELETE_STUDENT_NEEDS"; payload: string }
  | { type: "SET_KSP_INTEGRATIONS"; payload: KSPAnalysisIntegration[] }
  | { type: "ADD_KSP_INTEGRATION"; payload: KSPAnalysisIntegration }
  | { type: "UPDATE_KSP_INTEGRATION"; payload: { id: string; data: Partial<KSPAnalysisIntegration> } }
  | { type: "DELETE_KSP_INTEGRATION"; payload: string }
  | { type: "SET_PAGINATION"; payload: StrategicPlanningState["pagination"] }
  | { type: "RESET_STATE" };

// Initial State
const initialState: StrategicPlanningState = {
  raporPendidikan: [],
  surveys: [],
  fgdSessions: [],
  swotItems: [],
  rootCauses: [],
  fishboneDiagrams: [],
  studentNeeds: [],
  kspIntegrations: [],
  loading: false,
  error: null,
  pagination: {
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 0,
  },
};

// Reducer
function strategicPlanningReducer(
  state: StrategicPlanningState,
  action: StrategicPlanningAction
): StrategicPlanningState {
  switch (action.type) {
    case "SET_LOADING":
      return { ...state, loading: action.payload };

    case "SET_ERROR":
      return { ...state, error: action.payload, loading: false };

    case "SET_RAPOR_PENDIDIKAN":
      return { ...state, raporPendidikan: action.payload };

    case "ADD_RAPOR_PENDIDIKAN":
      return { ...state, raporPendidikan: [...state.raporPendidikan, action.payload] };

    case "UPDATE_RAPOR_PENDIDIKAN":
      return {
        ...state,
        raporPendidikan: state.raporPendidikan.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_RAPOR_PENDIDIKAN":
      return {
        ...state,
        raporPendidikan: state.raporPendidikan.filter((item) => item.id !== action.payload),
      };

    case "SET_SURVEYS":
      return { ...state, surveys: action.payload };

    case "ADD_SURVEY":
      return { ...state, surveys: [...state.surveys, action.payload] };

    case "UPDATE_SURVEY":
      return {
        ...state,
        surveys: state.surveys.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_SURVEY":
      return {
        ...state,
        surveys: state.surveys.filter((item) => item.id !== action.payload),
      };

    case "SET_FGD_SESSIONS":
      return { ...state, fgdSessions: action.payload };

    case "ADD_FGD_SESSION":
      return { ...state, fgdSessions: [...state.fgdSessions, action.payload] };

    case "UPDATE_FGD_SESSION":
      return {
        ...state,
        fgdSessions: state.fgdSessions.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_FGD_SESSION":
      return {
        ...state,
        fgdSessions: state.fgdSessions.filter((item) => item.id !== action.payload),
      };

    case "SET_SWOT_ITEMS":
      return { ...state, swotItems: action.payload };

    case "ADD_SWOT_ITEM":
      return { ...state, swotItems: [...state.swotItems, action.payload] };

    case "UPDATE_SWOT_ITEM":
      return {
        ...state,
        swotItems: state.swotItems.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_SWOT_ITEM":
      return {
        ...state,
        swotItems: state.swotItems.filter((item) => item.id !== action.payload),
      };

    case "SET_ROOT_CAUSES":
      return { ...state, rootCauses: action.payload };

    case "ADD_ROOT_CAUSE":
      return { ...state, rootCauses: [...state.rootCauses, action.payload] };

    case "UPDATE_ROOT_CAUSE":
      return {
        ...state,
        rootCauses: state.rootCauses.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_ROOT_CAUSE":
      return {
        ...state,
        rootCauses: state.rootCauses.filter((item) => item.id !== action.payload),
      };

    case "SET_FISHBONE_DIAGRAMS":
      return { ...state, fishboneDiagrams: action.payload };

    case "ADD_FISHBONE_DIAGRAM":
      return { ...state, fishboneDiagrams: [...state.fishboneDiagrams, action.payload] };

    case "UPDATE_FISHBONE_DIAGRAM":
      return {
        ...state,
        fishboneDiagrams: state.fishboneDiagrams.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_FISHBONE_DIAGRAM":
      return {
        ...state,
        fishboneDiagrams: state.fishboneDiagrams.filter((item) => item.id !== action.payload),
      };

    case "SET_STUDENT_NEEDS":
      return { ...state, studentNeeds: action.payload };

    case "ADD_STUDENT_NEEDS":
      return { ...state, studentNeeds: [...state.studentNeeds, action.payload] };

    case "UPDATE_STUDENT_NEEDS":
      return {
        ...state,
        studentNeeds: state.studentNeeds.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_STUDENT_NEEDS":
      return {
        ...state,
        studentNeeds: state.studentNeeds.filter((item) => item.id !== action.payload),
      };

    case "SET_KSP_INTEGRATIONS":
      return { ...state, kspIntegrations: action.payload };

    case "ADD_KSP_INTEGRATION":
      return { ...state, kspIntegrations: [...state.kspIntegrations, action.payload] };

    case "UPDATE_KSP_INTEGRATION":
      return {
        ...state,
        kspIntegrations: state.kspIntegrations.map((item) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };

    case "DELETE_KSP_INTEGRATION":
      return {
        ...state,
        kspIntegrations: state.kspIntegrations.filter((item) => item.id !== action.payload),
      };

    case "SET_PAGINATION":
      return { ...state, pagination: action.payload };

    case "RESET_STATE":
      return initialState;

    default:
      return state;
  }
}

// Context Type
interface StrategicPlanningContextType {
  state: StrategicPlanningState;
  dispatch: React.Dispatch<StrategicPlanningAction>;

  // Rapor Pendidikan Actions
  fetchRaporPendidikan: (params?: any) => Promise<void>;
  createRaporPendidikan: (data: Partial<RaporPendidikan>) => Promise<void>;
  updateRaporPendidikan: (id: string, data: Partial<RaporPendidikan>) => Promise<void>;
  deleteRaporPendidikan: (id: string) => Promise<void>;

  // Survey Actions
  fetchSurveys: (params?: any) => Promise<void>;
  createSurvey: (data: Partial<Survey>) => Promise<void>;
  updateSurvey: (id: string, data: Partial<Survey>) => Promise<void>;
  deleteSurvey: (id: string) => Promise<void>;

  // FGD Actions
  fetchFGDSessions: (params?: any) => Promise<void>;
  createFGDSession: (data: Partial<FGDSession>) => Promise<void>;
  updateFGDSession: (id: string, data: Partial<FGDSession>) => Promise<void>;
  deleteFGDSession: (id: string) => Promise<void>;

  // SWOT Actions
  fetchSWOTItems: (params?: any) => Promise<void>;
  createSWOTItem: (data: Partial<SWOTItem>) => Promise<void>;
  updateSWOTItem: (id: string, data: Partial<SWOTItem>) => Promise<void>;
  deleteSWOTItem: (id: string) => Promise<void>;

  // Root Cause Actions
  fetchRootCauses: (params?: any) => Promise<void>;
  createRootCause: (data: Partial<RootCause>) => Promise<void>;
  updateRootCause: (id: string, data: Partial<RootCause>) => Promise<void>;
  deleteRootCause: (id: string) => Promise<void>;

  // Fishbone Actions
  fetchFishboneDiagrams: (params?: any) => Promise<void>;
  createFishboneDiagram: (data: Partial<FishboneDiagram>) => Promise<void>;
  updateFishboneDiagram: (id: string, data: Partial<FishboneDiagram>) => Promise<void>;
  deleteFishboneDiagram: (id: string) => Promise<void>;

  // Student Needs Actions
  fetchStudentNeeds: (params?: any) => Promise<void>;
  createStudentNeeds: (data: Partial<StudentNeedsEnhanced>) => Promise<void>;
  updateStudentNeeds: (id: string, data: Partial<StudentNeedsEnhanced>) => Promise<void>;
  deleteStudentNeeds: (id: string) => Promise<void>;

  // KSP Integration Actions
  fetchKSPIntegrations: (params?: any) => Promise<void>;
  createKSPIntegration: (data: Partial<KSPAnalysisIntegration>) => Promise<void>;
  updateKSPIntegration: (id: string, data: Partial<KSPAnalysisIntegration>) => Promise<void>;
  deleteKSPIntegration: (id: string) => Promise<void>;

  // FASE 4: Integration Actions
  // Local Context Integration
  getLocalContextForSWOT: (schoolId: string) => Promise<any>;
  analyzeLearningPotential: (schoolId: string) => Promise<any>;
  getEnhancedLocalCategories: (schoolId: string) => Promise<any>;

  // Student Context Analytics
  getSurveyAnalyticsAggregated: (schoolId: string, surveyId: string) => Promise<any>;
  getStudentProfileAnalysis: (schoolId: string, profileDimension?: string) => Promise<any>;
  getStatisticalAnalysis: (schoolId: string, analysisType?: string) => Promise<any>;
  generateActionPlanRecommendations: (schoolId: string) => Promise<any>;

  // School Data Integration
  getSchoolDataForSWOT: (schoolId: string) => Promise<any>;
  getDigitalReadinessAssessment: (schoolId: string) => Promise<any>;
  getSarprasPrioritization: (schoolId: string) => Promise<any>;

  // Utility Actions
  clearError: () => void;
  resetState: () => void;
}

// Create Context
const StrategicPlanningContext = createContext<StrategicPlanningContextType | undefined>(
  undefined
);

// Provider Component
interface StrategicPlanningProviderProps {
  children: ReactNode;
}

export const StrategicPlanningProvider: React.FC<StrategicPlanningProviderProps> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(strategicPlanningReducer, initialState);

  // Rapor Pendidikan Actions
  const fetchRaporPendidikan = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.raporPendidikan.getAll(params);
      dispatch({ type: "SET_RAPOR_PENDIDIKAN", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch rapor data" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createRaporPendidikan = useCallback(async (data: Partial<RaporPendidikan>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.raporPendidikan.create(data);
      dispatch({ type: "ADD_RAPOR_PENDIDIKAN", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create rapor data" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateRaporPendidikan = useCallback(async (id: string, data: Partial<RaporPendidikan>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.raporPendidikan.update(id, data);
      dispatch({ type: "UPDATE_RAPOR_PENDIDIKAN", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update rapor data" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteRaporPendidikan = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.raporPendidikan.delete(id);
      dispatch({ type: "DELETE_RAPOR_PENDIDIKAN", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete rapor data" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // Survey Actions
  const fetchSurveys = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.survey.getAll(params);
      dispatch({ type: "SET_SURVEYS", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch surveys" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createSurvey = useCallback(async (data: Partial<Survey>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.survey.create(data);
      dispatch({ type: "ADD_SURVEY", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create survey" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateSurvey = useCallback(async (id: string, data: Partial<Survey>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.survey.update(id, data);
      dispatch({ type: "UPDATE_SURVEY", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update survey" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteSurvey = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.survey.delete(id);
      dispatch({ type: "DELETE_SURVEY", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete survey" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // FGD Actions
  const fetchFGDSessions = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.fgd.getAll(params);
      dispatch({ type: "SET_FGD_SESSIONS", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch FGD sessions" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createFGDSession = useCallback(async (data: Partial<FGDSession>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.fgd.create(data);
      dispatch({ type: "ADD_FGD_SESSION", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create FGD session" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateFGDSession = useCallback(async (id: string, data: Partial<FGDSession>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.fgd.update(id, data);
      dispatch({ type: "UPDATE_FGD_SESSION", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update FGD session" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteFGDSession = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.fgd.delete(id);
      dispatch({ type: "DELETE_FGD_SESSION", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete FGD session" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // SWOT Actions
  const fetchSWOTItems = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.swot.getAll(params);
      dispatch({ type: "SET_SWOT_ITEMS", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch SWOT items" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createSWOTItem = useCallback(async (data: Partial<SWOTItem>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.swot.create(data);
      dispatch({ type: "ADD_SWOT_ITEM", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create SWOT item" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateSWOTItem = useCallback(async (id: string, data: Partial<SWOTItem>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.swot.update(id, data);
      dispatch({ type: "UPDATE_SWOT_ITEM", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update SWOT item" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteSWOTItem = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.swot.delete(id);
      dispatch({ type: "DELETE_SWOT_ITEM", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete SWOT item" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // Root Cause Actions
  const fetchRootCauses = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.rootCause.getAll(params);
      dispatch({ type: "SET_ROOT_CAUSES", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch root causes" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createRootCause = useCallback(async (data: Partial<RootCause>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.rootCause.create(data);
      dispatch({ type: "ADD_ROOT_CAUSE", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create root cause" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateRootCause = useCallback(async (id: string, data: Partial<RootCause>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.rootCause.update(id, data);
      dispatch({ type: "UPDATE_ROOT_CAUSE", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update root cause" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteRootCause = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.rootCause.delete(id);
      dispatch({ type: "DELETE_ROOT_CAUSE", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete root cause" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // Fishbone Actions
  const fetchFishboneDiagrams = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.fishbone.getAll(params);
      dispatch({ type: "SET_FISHBONE_DIAGRAMS", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch fishbone diagrams" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createFishboneDiagram = useCallback(async (data: Partial<FishboneDiagram>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.fishbone.create(data);
      dispatch({ type: "ADD_FISHBONE_DIAGRAM", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create fishbone diagram" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateFishboneDiagram = useCallback(async (id: string, data: Partial<FishboneDiagram>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.fishbone.update(id, data);
      dispatch({ type: "UPDATE_FISHBONE_DIAGRAM", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update fishbone diagram" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteFishboneDiagram = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.fishbone.delete(id);
      dispatch({ type: "DELETE_FISHBONE_DIAGRAM", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete fishbone diagram" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // Student Needs Actions
  const fetchStudentNeeds = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.studentNeeds.getAll(params);
      dispatch({ type: "SET_STUDENT_NEEDS", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch student needs" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createStudentNeeds = useCallback(async (data: Partial<StudentNeedsEnhanced>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.studentNeeds.create(data);
      dispatch({ type: "ADD_STUDENT_NEEDS", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create student needs" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateStudentNeeds = useCallback(async (id: string, data: Partial<StudentNeedsEnhanced>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.studentNeeds.update(id, data);
      dispatch({ type: "UPDATE_STUDENT_NEEDS", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update student needs" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteStudentNeeds = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.studentNeeds.delete(id);
      dispatch({ type: "DELETE_STUDENT_NEEDS", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete student needs" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // KSP Integration Actions
  const fetchKSPIntegrations = useCallback(async (params?: any) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.kspIntegration.getAll(params);
      dispatch({ type: "SET_KSP_INTEGRATIONS", payload: response.data });
      if (response.pagination) {
        dispatch({ type: "SET_PAGINATION", payload: response.pagination });
      }
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to fetch KSP integrations" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const createKSPIntegration = useCallback(async (data: Partial<KSPAnalysisIntegration>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.kspIntegration.create(data);
      dispatch({ type: "ADD_KSP_INTEGRATION", payload: response.data });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to create KSP integration" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const updateKSPIntegration = useCallback(async (id: string, data: Partial<KSPAnalysisIntegration>) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.kspIntegration.update(id, data);
      dispatch({ type: "UPDATE_KSP_INTEGRATION", payload: { id, data } });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to update KSP integration" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const deleteKSPIntegration = useCallback(async (id: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      await strategicPlanningAPI.kspIntegration.delete(id);
      dispatch({ type: "DELETE_KSP_INTEGRATION", payload: id });
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to delete KSP integration" });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // FASE 4: Integration Actions
  // Local Context Integration
  const getLocalContextForSWOT = useCallback(async (schoolId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.localContext.getLocalContextForSWOT(schoolId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get local context for SWOT" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const analyzeLearningPotential = useCallback(async (schoolId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.localContext.analyzeLearningPotential(schoolId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to analyze learning potential" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const getEnhancedLocalCategories = useCallback(async (schoolId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.localContext.getEnhancedLocalCategories(schoolId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get enhanced local categories" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // Student Context Analytics
  const getSurveyAnalyticsAggregated = useCallback(async (schoolId: string, surveyId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.analytics.getSurveyAnalyticsAggregated(schoolId, surveyId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get survey analytics aggregated" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const getStudentProfileAnalysis = useCallback(async (schoolId: string, profileDimension?: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.analytics.getStudentProfileAnalysis(schoolId, profileDimension);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get student profile analysis" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const getStatisticalAnalysis = useCallback(async (schoolId: string, analysisType?: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.analytics.getStatisticalAnalysis(schoolId, analysisType);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get statistical analysis" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const generateActionPlanRecommendations = useCallback(async (schoolId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.analytics.generateActionPlanRecommendations(schoolId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to generate action plan recommendations" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // School Data Integration
  const getSchoolDataForSWOT = useCallback(async (schoolId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.schoolData.getSchoolDataForSWOT(schoolId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get school data for SWOT" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const getDigitalReadinessAssessment = useCallback(async (schoolId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.schoolData.getDigitalReadinessAssessment(schoolId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get digital readiness assessment" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  const getSarprasPrioritization = useCallback(async (schoolId: string) => {
    try {
      dispatch({ type: "SET_LOADING", payload: true });
      const response = await strategicPlanningAPI.schoolData.getSarprasPrioritization(schoolId);
      return response.data;
    } catch (error: any) {
      dispatch({ type: "SET_ERROR", payload: error.message || "Failed to get sarpras prioritization" });
      throw error;
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // Utility Actions
  const clearError = useCallback(() => {
    dispatch({ type: "SET_ERROR", payload: null });
  }, []);

  const resetState = useCallback(() => {
    dispatch({ type: "RESET_STATE" });
  }, []);

  const value: StrategicPlanningContextType = {
    state,
    dispatch,

    // Rapor Pendidikan
    fetchRaporPendidikan,
    createRaporPendidikan,
    updateRaporPendidikan,
    deleteRaporPendidikan,

    // Survey
    fetchSurveys,
    createSurvey,
    updateSurvey,
    deleteSurvey,

    // FGD
    fetchFGDSessions,
    createFGDSession,
    updateFGDSession,
    deleteFGDSession,

    // SWOT
    fetchSWOTItems,
    createSWOTItem,
    updateSWOTItem,
    deleteSWOTItem,

    // Root Cause
    fetchRootCauses,
    createRootCause,
    updateRootCause,
    deleteRootCause,

    // Fishbone
    fetchFishboneDiagrams,
    createFishboneDiagram,
    updateFishboneDiagram,
    deleteFishboneDiagram,

    // Student Needs
    fetchStudentNeeds,
    createStudentNeeds,
    updateStudentNeeds,
    deleteStudentNeeds,

    // KSP Integration
    fetchKSPIntegrations,
    createKSPIntegration,
    updateKSPIntegration,
    deleteKSPIntegration,

    // FASE 4: Integration
    getLocalContextForSWOT,
    analyzeLearningPotential,
    getEnhancedLocalCategories,
    getSurveyAnalyticsAggregated,
    getStudentProfileAnalysis,
    getStatisticalAnalysis,
    generateActionPlanRecommendations,
    getSchoolDataForSWOT,
    getDigitalReadinessAssessment,
    getSarprasPrioritization,

    // Utilities
    clearError,
    resetState,
  };

  return (
    <StrategicPlanningContext.Provider value={value}>
      {children}
    </StrategicPlanningContext.Provider>
  );
};

// Custom Hook
export const useStrategicPlanning = () => {
  const context = useContext(StrategicPlanningContext);
  if (context === undefined) {
    throw new Error("useStrategicPlanning must be used within a StrategicPlanningProvider");
  }
  return context;
};
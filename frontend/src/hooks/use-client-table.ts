/* eslint-disable react-hooks/set-state-in-effect */
import { useEffect, useMemo, useState } from "react";

interface TableState {
  page: number;
  limit: number;
  sortBy: string;
  sortDir: "asc" | "desc";
}

interface UseClientTableProps<T> {
  key: string;
  data: T[];
  defaultLimit?: number;
}

// Helper to access nested object properties via string path (e.g. "subject.subject_name")
const getNestedValue = (obj: any, path: string) => {
  return path.split(".").reduce((acc, part) => acc && acc[part], obj);
};

export function useClientTable<T>({ key, data, defaultLimit = 10 }: UseClientTableProps<T>) {
  // 1. Initialize state from Session Storage or Defaults
  const [state, setState] = useState<TableState>(() => {
    try {
      const stored = sessionStorage.getItem(`table_state_${key}`);
      if (stored) {
        return JSON.parse(stored) as TableState;
      }
    } catch (e) {
      console.warn("Failed to parse table state from session storage");
    }
    return {
      page: 1, // 1-based page index for logic
      limit: defaultLimit,
      sortBy: "",
      sortDir: "asc",
    };
  });

  // 2. Sync state changes back to Session Storage
  useEffect(() => {
    sessionStorage.setItem(`table_state_${key}`, JSON.stringify(state));
  }, [key, state]);

  // 3. Sorting Logic
  const sortedData = useMemo(() => {
    if (!state.sortBy) return data;

    return [...data].sort((a: any, b: any) => {
      const valA = getNestedValue(a, state.sortBy);
      const valB = getNestedValue(b, state.sortBy);

      if (valA == null) return state.sortDir === "asc" ? -1 : 1;
      if (valB == null) return state.sortDir === "asc" ? 1 : -1;

      if (valA < valB) return state.sortDir === "asc" ? -1 : 1;
      if (valA > valB) return state.sortDir === "asc" ? 1 : -1;
      return 0;
    });
  }, [data, state.sortBy, state.sortDir]);

  // 4. Pagination Logic
  const paginatedData = useMemo(() => {
    const start = (state.page - 1) * state.limit;
    return sortedData.slice(start, start + state.limit);
  }, [sortedData, state.page, state.limit]);

  // Ensure page is not out of bounds if data shrinks (e.g., after a search filter)

  useEffect(() => {
    const totalPages = Math.ceil(sortedData.length / state.limit);
    if (state.page > totalPages && totalPages > 0) {
      setState((prev) => ({ ...prev, page: totalPages }));
    } else if (state.page < 1 && sortedData.length > 0) {
      setState((prev) => ({ ...prev, page: 1 }));
    }
  }, [sortedData.length, state.limit, state.page]);

  // 5. Handlers
  const handlePageChange = (newPage: number) => {
    setState((prev) => ({ ...prev, page: newPage }));
  };

  const handleLimitChange = (newLimit: number) => {
    setState((prev) => ({ ...prev, limit: newLimit, page: 1 })); // Reset to page 1 when limit changes
  };

  const handleSort = (field: string) => {
    setState((prev) => {
      if (prev.sortBy === field) {
        return {
          ...prev,
          sortDir: prev.sortDir === "asc" ? "desc" : "asc",
        };
      }
      return {
        ...prev,
        sortBy: field,
        sortDir: "asc",
      };
    });
  };

  return {
    // Data
    paginatedData,
    total: sortedData.length,
    // State
    page: state.page,
    limit: state.limit,
    sortBy: state.sortBy,
    sortDir: state.sortDir,
    // Handlers
    handlePageChange,
    handleLimitChange,
    handleSort,
  };
}

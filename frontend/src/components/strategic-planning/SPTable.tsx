import React, { useMemo } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Paper,
  Typography,
  Box,
  CircularProgress,
} from "@mui/material";
import { useClientTable } from "@/hooks/use-client-table";
import { cn } from "@/lib/utils";

interface Column {
  id: string;
  label: string;
  width?: number | string;
  align?: "left" | "center" | "right";
}

interface SPTableProps<T> {
  columns: Column[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  onRowClick?: (row: T) => void;
  renderCell?: (columnId: string, row: T) => React.ReactNode;
  tableKey?: string;
}

function SPTable<T extends Record<string, any>>({
  columns,
  data,
  loading = false,
  emptyMessage = "Tidak ada data tersedia",
  onRowClick,
  renderCell,
  tableKey = "default-table",
}: SPTableProps<T>) {
  const {
    paginatedData,
    page,
    limit,
    total,
    sortBy,
    sortDir,
    handlePageChange,
    handleLimitChange,
    handleSort,
  } = useClientTable({ key: tableKey, data, defaultLimit: 10 });

  const getCellValue = (columnId: string, row: T): React.ReactNode => {
    if (renderCell) {
      return renderCell(columnId, row);
    }
    const value = row[columnId];
    if (value === undefined || value === null) {
      return "-";
    }
    return String(value);
  };

  return (
    <Box>
      <TableContainer component={Paper} className="rounded-2xl">
        <Table>
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  width={column.width}
                  align={column.align || "left"}
                  className="font-bold"
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={columns.length} align="center" className="py-4">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length === 0 ? (
              <TableRow>
                <TableCell colSpan={columns.length} align="center" className="py-4">
                  <Typography variant="body2" className="text-text-secondary">
                    {emptyMessage}
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              paginatedData.map((row, index) => (
                <TableRow
                  key={index}
                  hover
                  onClick={() => onRowClick && onRowClick(row)}
                  className={cn("cursor-pointer", onRowClick && "hover:bg-grey-50")}
                >
                  {columns.map((column) => (
                    <TableCell
                      key={column.id}
                      width={column.width}
                      align={column.align || "left"}
                    >
                      {getCellValue(column.id, row)}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
      {!loading && paginatedData.length > 0 && (
        <TablePagination
          rowsPerPageOptions={[5, 10, 25, 50]}
          component="div"
          count={total}
          rowsPerPage={limit}
          page={page}
          onPageChange={handlePageChange}
          onRowsPerPageChange={handleLimitChange}
          labelRowsPerPage="Baris per halaman:"
          labelDisplayedRows={({ from, to, count }) => `${from}-${to} dari ${count !== -1 ? count : `lebih dari ${to}`}`}
        />
      )}
    </Box>
  );
}

export default SPTable;
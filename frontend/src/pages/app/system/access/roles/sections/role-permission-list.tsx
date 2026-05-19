import { useCallback, useState } from "react";

import {
  Box,
  Button,
  FilledInput,
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  Select,
  SelectProps,
} from "@mui/material";
import { Grid } from "@mui/material";
import type { GridColDef } from "@mui/x-data-grid";
import {
  GridActionsCellItem,
  GridRenderCellParams,
  GridRowSelectionModel,
  GridRowSpacingParams,
  QuickFilter,
  QuickFilterClear,
  QuickFilterControl,
  Toolbar,
} from "@mui/x-data-grid";
import { DataGrid } from "@mui/x-data-grid";

import NiArrowDown from "@/icons/nexture/ni-arrow-down";
import NiArrowUp from "@/icons/nexture/ni-arrow-up";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiCheckSquare from "@/icons/nexture/ni-check-square";
import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiChevronLeftRightSmall from "@/icons/nexture/ni-chevron-left-right-small";
import NiCols from "@/icons/nexture/ni-cols";
import NiCross from "@/icons/nexture/ni-cross";
import NiCrossSquare from "@/icons/nexture/ni-cross-square";
import NiDuplicate from "@/icons/nexture/ni-duplicate";
import NiEllipsisVertical from "@/icons/nexture/ni-ellipsis-vertical";
import NiEyeInactive from "@/icons/nexture/ni-eye-inactive";
import NiFilter from "@/icons/nexture/ni-filter";
import NiFilterPlus from "@/icons/nexture/ni-filter-plus";
import NiPenSquare from "@/icons/nexture/ni-pen-square";
import NiSearch from "@/icons/nexture/ni-search";
import { cn } from "@/lib/utils";

interface Permission {
  id: string;
  permission_name: string;
  description: string;
}

interface RolePermissionListProps {
  selectedRoleId: string | null;
  selectedRoleName: string | undefined;
  allPermissions: Permission[];
  localPermissions: Record<string, Set<string>>;
  saving: boolean;
  loading: boolean;
  handleTogglePermission: (moduleKey: string, action: "view" | "create" | "edit" | "delete") => void;
}

const MODULE_KEYS = [
  "system",
  "school",
  "staff",
  "student",
  "ppdb",
  "curriculum",
  "classroom",
  "presence",
  "modules",
  "assessment",
  "counseling",
  "report",
];

const getPermissionName = (moduleKey: string, action: "view" | "create" | "edit" | "delete"): string | null => {
  if (moduleKey === "system") {
    if (action === "view") return "system:view";
    if (action === "create") return "system:access";
    if (action === "edit") return "system:update";
    return null;
  }
  if (moduleKey === "school") {
    if (action === "view") return "school:view";
    if (action === "edit") return "school:update";
    return null;
  }
  if (moduleKey === "staff") {
    if (action === "view") return "staff:view";
    if (action === "create") return "staff:create";
    if (action === "edit") return "staff:update";
    if (action === "delete") return "staff:delete";
  }
  if (moduleKey === "student") {
    if (action === "view") return "student:view";
    if (action === "create") return "student:create";
    if (action === "edit") return "student:update";
    if (action === "delete") return "student:delete";
  }
  if (moduleKey === "ppdb") {
    if (action === "view") return "ppdb:view";
    if (action === "edit") return "ppdb:update";
    return null;
  }
  if (moduleKey === "curriculum") {
    if (action === "view") return "curriculum:view";
    if (action === "edit") return "curriculum:update";
    return null;
  }
  if (moduleKey === "classroom") {
    if (action === "view") return "classroom:view";
    if (action === "create") return "classroom:create";
    if (action === "edit") return "classroom:update";
    if (action === "delete") return "classroom:delete";
  }
  if (moduleKey === "presence") {
    if (action === "view") return "presence:view";
    if (action === "edit") return "presence:update";
    return null;
  }
  if (moduleKey === "modules") {
    if (action === "view") return "modules:view";
    if (action === "edit") return "modules:update";
    return null;
  }
  if (moduleKey === "assessment") {
    if (action === "view") return "assessment:view";
    if (action === "edit") return "assessment:update";
    return null;
  }
  if (moduleKey === "counseling") {
    if (action === "view") return "counseling:view";
    if (action === "create") return "counseling:create";
    if (action === "edit") return "counseling:update";
    return null;
  }
  if (moduleKey === "report") {
    if (action === "view") return "report:view";
    if (action === "edit") return "report:finalize";
    return null;
  }
  return null;
};

const getModuleLabel = (key: string): string => {
  switch (key) {
    case "system":
      return "Sistem & Analitik";
    case "school":
      return "Profil Sekolah";
    case "staff":
      return "Kepegawaian (Guru/Staf)";
    case "student":
      return "Kesiswaan (Data Murid)";
    case "ppdb":
      return "Penerimaan Siswa Baru (PPDB)";
    case "curriculum":
      return "Kurikulum & KSP";
    case "classroom":
      return "Rombel & Jadwal Kelas";
    case "presence":
      return "Presensi & Kehadiran";
    case "modules":
      return "Bahan & Modul Ajar";
    case "assessment":
      return "Asesmen & Nilai Raport";
    case "counseling":
      return "Bimbingan Konseling (EWS)";
    case "report":
      return "Cetak Rapor Digital";
    default:
      return key;
  }
};

export default function RolePermissionList({
  selectedRoleId,
  selectedRoleName,
  allPermissions,
  localPermissions,
  saving,
  loading,
  handleTogglePermission,
}: RolePermissionListProps) {
  const [rowSelectionModel, setRowSelectionModel] = useState<GridRowSelectionModel>({
    type: "include",
    ids: new Set(),
  });

  const getRowSpacing = useCallback((params: GridRowSpacingParams) => {
    return {
      top: params.isFirstVisible ? 0 : 5,
      bottom: 5,
    };
  }, []);

  const gridRows = selectedRoleId
    ? MODULE_KEYS.map((key) => {
        const viewName = getPermissionName(key, "view");
        const createName = getPermissionName(key, "create");
        const editName = getPermissionName(key, "edit");
        const deleteName = getPermissionName(key, "delete");

        const viewObj = allPermissions.find((p) => p.permission_name === viewName);
        const createObj = allPermissions.find((p) => p.permission_name === createName);
        const editObj = allPermissions.find((p) => p.permission_name === editName);
        const deleteObj = allPermissions.find((p) => p.permission_name === deleteName);

        const activeSet = localPermissions[selectedRoleId] || new Set();

        return {
          id: key,
          type: getModuleLabel(key),
          configuration: "Semua Item Saat Ini & Masa Depan",
          view: viewObj ? activeSet.has(viewObj.id) : null,
          create: createObj ? activeSet.has(createObj.id) : null,
          edit: editObj ? activeSet.has(editObj.id) : null,
          delete: deleteObj ? activeSet.has(deleteObj.id) : null,
        };
      })
    : [];

  const columns: GridColDef<(typeof gridRows)[number]>[] = [
    {
      field: "id",
      headerName: "ID",
      width: 240,
      type: "string",
    },
    {
      field: "type",
      headerName: "Modul / Sumber Daya",
      align: "left",
      headerAlign: "left",
      width: 250,
    },
    {
      field: "configuration",
      headerName: "Ruang Lingkup",
      align: "left",
      headerAlign: "left",
      width: 240,
    },
    {
      field: "view",
      headerName: "Melihat (View)",
      align: "left",
      headerAlign: "left",
      type: "boolean",
      width: 120,
      renderCell: (params: GridRenderCellParams<any, boolean | null>) => {
        const value = params.value;
        if (value === null) {
          return (
            <Box className="flex h-full w-full items-center pl-4">
              <span className="text-sm font-bold text-slate-300">—</span>
            </Box>
          );
        }
        const isDisabled = selectedRoleName === "ADMIN" || saving;
        return (
          <Box className="flex h-full w-full items-center">
            <IconButton
              disabled={isDisabled}
              onClick={() => handleTogglePermission(params.row.id, "view")}
              size="small"
              disableRipple
              sx={{ p: 0.5 }}
            >
              {value ? <NiCheckSquare className="text-success" /> : <NiCrossSquare className="text-error" />}
            </IconButton>
          </Box>
        );
      },
    },
    {
      field: "create",
      headerName: "Membuat (Create)",
      align: "left",
      headerAlign: "left",
      type: "boolean",
      width: 130,
      renderCell: (params: GridRenderCellParams<any, boolean | null>) => {
        const value = params.value;
        if (value === null) {
          return (
            <Box className="flex h-full w-full items-center pl-4">
              <span className="text-sm font-bold text-slate-300">—</span>
            </Box>
          );
        }
        const isDisabled = selectedRoleName === "ADMIN" || saving;
        return (
          <Box className="flex h-full w-full items-center">
            <IconButton
              disabled={isDisabled}
              onClick={() => handleTogglePermission(params.row.id, "create")}
              size="small"
              disableRipple
              sx={{ p: 0.5 }}
            >
              {value ? <NiCheckSquare className="text-success" /> : <NiCrossSquare className="text-error" />}
            </IconButton>
          </Box>
        );
      },
    },
    {
      field: "edit",
      headerName: "Mengubah (Edit)",
      align: "left",
      headerAlign: "left",
      type: "boolean",
      width: 130,
      renderCell: (params: GridRenderCellParams<any, boolean | null>) => {
        const value = params.value;
        if (value === null) {
          return (
            <Box className="flex h-full w-full items-center pl-4">
              <span className="text-sm font-bold text-slate-300">—</span>
            </Box>
          );
        }
        const isDisabled = selectedRoleName === "ADMIN" || saving;
        return (
          <Box className="flex h-full w-full items-center">
            <IconButton
              disabled={isDisabled}
              onClick={() => handleTogglePermission(params.row.id, "edit")}
              size="small"
              disableRipple
              sx={{ p: 0.5 }}
            >
              {value ? <NiCheckSquare className="text-success" /> : <NiCrossSquare className="text-error" />}
            </IconButton>
          </Box>
        );
      },
    },
    {
      field: "delete",
      headerName: "Menghapus (Delete)",
      align: "left",
      headerAlign: "left",
      type: "boolean",
      width: 140,
      renderCell: (params: GridRenderCellParams<any, boolean | null>) => {
        const value = params.value;
        if (value === null) {
          return (
            <Box className="flex h-full w-full items-center pl-4">
              <span className="text-sm font-bold text-slate-300">—</span>
            </Box>
          );
        }
        const isDisabled = selectedRoleName === "ADMIN" || saving;
        return (
          <Box className="flex h-full w-full items-center">
            <IconButton
              disabled={isDisabled}
              onClick={() => handleTogglePermission(params.row.id, "delete")}
              size="small"
              disableRipple
              sx={{ p: 0.5 }}
            >
              {value ? <NiCheckSquare className="text-success" /> : <NiCrossSquare className="text-error" />}
            </IconButton>
          </Box>
        );
      },
    },
    {
      field: "actions",
      headerName: "Tindakan",
      type: "actions",
      minWidth: 80,
      flex: 1,
      align: "right",
      headerAlign: "right",
      getActions: () => [
        <GridActionsCellItem key={1} icon={<NiPenSquare size="medium" />} label="Edit" showInMenu />,
        <GridActionsCellItem key={2} icon={<NiDuplicate size="medium" />} label="Duplicate" showInMenu />,
        <GridActionsCellItem key={0} icon={<NiCrossSquare size="medium" />} label="Delete" showInMenu />,
      ],
    },
  ];

  function CustomToolbar() {
    return (
      <Toolbar className="min-h-auto border-none p-0">
        <Grid container spacing={5} className="m-0 mb-4 w-full">
          <FormControl variant="filled" size="medium" className="surface mb-0 flex-1 pt-0.25">
            <InputLabel>Search</InputLabel>
            <QuickFilter
              render={() => (
                <QuickFilterControl
                  render={({ ref, ...controlProps }, state) => (
                    <FilledInput
                      {...controlProps}
                      inputRef={ref}
                      endAdornment={
                        <>
                          <InputAdornment position="end" className={cn(state.value === "" && "hidden")}>
                            <QuickFilterClear edge="end">
                              <NiCross size="medium" className="text-text-disabled" />
                            </QuickFilterClear>
                          </InputAdornment>
                          <InputAdornment position="end" className={cn(state.value !== "" && "hidden")}>
                            <IconButton edge="end">
                              {<NiSearch size="medium" className="text-text-disabled" />}
                            </IconButton>
                          </InputAdornment>
                        </>
                      }
                    />
                  )}
                />
              )}
            />
          </FormControl>
        </Grid>
      </Toolbar>
    );
  }

  return (
    <Box sx={{ width: "100%", p: 3 }}>
      <DataGrid
        rows={gridRows}
        columns={columns}
        loading={loading}
        initialState={{
          columns: { columnVisibilityModel: { id: false } },
        }}
        pagination={false}
        hideFooter
        getRowSpacing={getRowSpacing}
        rowHeight={68}
        columnHeaderHeight={32}
        disableRowSelectionOnClick
        className="full-page border-none"
        slotProps={{
          panel: {
            className: "mt-1!",
          },
          main: {
            className: "min-h-[815px]! overflow-visible",
          },
        }}
        slots={{
          columnSortedDescendingIcon: () => {
            return <NiArrowDown size={"small"}></NiArrowDown>;
          },
          columnSortedAscendingIcon: () => {
            return <NiArrowUp size={"small"}></NiArrowUp>;
          },
          columnFilteredIcon: () => {
            return <NiFilterPlus size={"small"}></NiFilterPlus>;
          },
          columnReorderIcon: () => {
            return <NiChevronLeftRightSmall size={"small"}></NiChevronLeftRightSmall>;
          },
          columnMenuIcon: () => {
            return <NiEllipsisVertical size={"small"}></NiEllipsisVertical>;
          },
          columnMenuSortAscendingIcon: NiArrowUp,
          columnMenuSortDescendingIcon: NiArrowDown,
          columnMenuFilterIcon: NiFilter,
          columnMenuHideIcon: NiEyeInactive,
          columnMenuClearIcon: NiCross,
          columnMenuManageColumnsIcon: NiCols,
          filterPanelDeleteIcon: NiCross,
          filterPanelRemoveAllIcon: NiBinEmpty,
          baseSelect: (props: any) => {
            const propsCasted = props as SelectProps;
            return (
              <FormControl size="small" variant="outlined">
                <InputLabel>{props.label}</InputLabel>
                <Select {...propsCasted} IconComponent={NiChevronDownSmall} MenuProps={{ className: "outlined" }} />
              </FormControl>
            );
          },
          quickFilterIcon: () => {
            return <NiSearch size={"medium"} />;
          },
          quickFilterClearIcon: () => {
            return <NiCross size={"medium"} />;
          },
          baseButton: (props) => {
            return <Button {...props} variant="pastel" color="grey"></Button>;
          },
          moreActionsIcon: () => {
            return <NiEllipsisVertical size={"medium"} />;
          },
          toolbar: CustomToolbar,
        }}
        rowSelectionModel={rowSelectionModel}
        onRowSelectionModelChange={(newModel: GridRowSelectionModel) => {
          setRowSelectionModel(newModel);
        }}
        hideFooterSelectedRowCount
        showToolbar
      />
    </Box>
  );
}

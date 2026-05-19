import { MenuItem } from "@/types/types";

export const leftMenuItems: MenuItem[] = [
  {
    id: "home",
    icon: "NiHome",
    label: "menu-home",
    href: "/home",
    color: "text-primary",
    children: [
      {
        id: "dashboard",
        label: "menu-summary",
        icon: "NiDashboard",
        href: "/home/board/summary",
      },
    ],
  },
  {
    id: "data-induk",
    icon: "NiBuilding",
    label: "menu-institution",
    href: "/profile",
    color: "text-primary",
    children: [
      { id: "school-profile", label: "menu-school", icon: "NiBuilding", href: "/profile/school" },
      { id: "staff-data", label: "menu-character-building", icon: "NiBadge", href: "/academic/subjects/staff" },
      { id: "student-data", label: "menu-data-students", icon: "NiUsers", href: "/students" },
      { id: "spmb-data", label: "menu-spmb-online", icon: "NiBadge", href: "/spmb/admin" },
      { id: "class-data", label: "menu-data-classes", icon: "NiLayout", href: "/academic/subjects/classroom" },
    ],
  },
  {
    id: "kurikulum",
    icon: "NiBook",
    label: "menu-curriculum",
    href: "/academic/curriculum",
    color: "text-primary",
    children: [
      {
        id: "standar-belajar",
        label: "menu-data-master",
        icon: "NiArchive",
        href: "/academic/curriculum",
        children: [
          { id: "phases", label: "menu-phases", href: "/academic/phases" },
          { id: "subjects", label: "menu-subjects", href: "/academic/subjects" },
          { id: "standards", label: "menu-standards", href: "/academic/curriculum" },
          { id: "objectives", label: "menu-objectives", href: "/academic/curriculum/objectives" },
          { id: "flow", label: "menu-flow", href: "/academic/curriculum/flow" },
          { id: "dimensions", label: "menu-dimensions", href: "/academic/dimensions" },
        ],
      },
      { id: "characteristics", label: "menu-data-local", icon: "NiMap", href: "/local-context" },
      { id: "ksp-doc", label: "menu-ksp-builder", icon: "NiPen", href: "/academic/ksp" },
    ],
  },
  {
    id: "pembelajaran",
    icon: "NiGraduation",
    label: "menu-learning",
    href: "/learning",
    color: "text-primary",
    children: [
      { id: "class-schedule", label: "menu-class-schedule", icon: "NiCalendar", href: "/academic/subjects/schedule" },
      { id: "presence", label: "menu-daily-presence", icon: "NiCheckFull", href: "/students/presence/daily" },
      {
        id: "teaching-modules",
        label: "menu-modules",
        icon: "NiArchive",
        href: "/learning/modules",
        children: [
          { id: "drafts", label: "menu-drafts", href: "/learning/modules/drafts" },
          { id: "library", label: "menu-library", href: "/learning/modules/library" },
        ],
      },
      { id: "p5-projects", label: "menu-projects", icon: "NiBriefcase", href: "/learning/projects/plans" },
    ],
  },
  {
    id: "asesmen",
    icon: "NiPen",
    label: "menu-assessment",
    href: "/academic/evaluation",
    color: "text-primary",
    children: [
      { id: "question-bank", label: "menu-question-bank", icon: "NiArchive", href: "/academic/evaluation/bank" },
      { id: "formative", label: "menu-formative-value", icon: "NiActivity", href: "/academic/evaluation/formative" },
      { id: "summative", label: "menu-summative-value", icon: "NiStar", href: "/academic/evaluation/summative" },
    ],
  },
  {
    id: "laporan",
    icon: "NiDocumentChart",
    label: "menu-reports",
    href: "/reports",
    color: "text-primary",
    children: [
      { id: "p5-achievement", label: "menu-project-scores", icon: "NiHeart", href: "/learning/projects/results" },
      { id: "gradebook-recap", label: "menu-gradebook", icon: "NiBook", href: "/reports/gradebook/scores" },
      { id: "print-rapport", label: "menu-print", icon: "NiPrinter", href: "/reports/gradebook/print" },
    ],
  },
];

export const leftMenuBottomItems: MenuItem[] = [
  {
    id: "sistem",
    icon: "NiCpu",
    label: "menu-system",
    href: "/system",
    color: "text-primary",
    children: [
      { id: "access-rights", label: "menu-access-rights", icon: "NiLock", href: "/system/access" },
      { id: "academic-year", label: "menu-academic-year-cycle", icon: "NiCalendar", href: "/system/academic-years" },
      { id: "grade-level", label: "menu-grade-master", icon: "NiLayout", href: "/system/grades" },
      { id: "system-status", label: "menu-data-index", icon: "NiActivity", href: "/system/engine" },
    ],
  },
  { id: "guide", label: "menu-guide", href: "/docs", icon: "NiBook", color: "text-primary" },
  { id: "settings", label: "menu-settings", href: "/settings", icon: "NiSettings" },
];

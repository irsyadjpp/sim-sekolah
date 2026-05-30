import { useParams } from "react-router-dom";
import { Navigate } from "react-router-dom";

export default function SurveyEditPage() {
  const { id } = useParams();
  return <Navigate to={`/strategic-planning/data-collection/surveys/create?id=${id}`} replace />;
}
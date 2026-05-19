import React from "react";

export function withChartElementStyle<P extends object>(Component: React.ComponentType<P>) {
  const DisplayName = Component.displayName || Component.name || "Component";

  const StyledComponent = (props: P) => {
    return <Component {...props} />;
  };

  StyledComponent.displayName = `withChartElementStyle(${DisplayName})`;
  return StyledComponent;
}

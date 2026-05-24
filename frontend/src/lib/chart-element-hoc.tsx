import React from "react";

export function withChartElementStyle<P extends object>(Component: React.ComponentType<P>, defaultProps?: any) {
  const DisplayName = Component.displayName || Component.name || "Component";

  const StyledComponent = (props: P) => {
    return <Component {...props} {...defaultProps} />;
  };

  StyledComponent.displayName = `withChartElementStyle(${DisplayName})`;
  return StyledComponent;
}

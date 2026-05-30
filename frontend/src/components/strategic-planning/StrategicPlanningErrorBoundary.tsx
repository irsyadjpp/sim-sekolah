import React, { Component, ErrorInfo, ReactNode } from "react";
import { Box, Typography, Button, Container, Paper } from "@mui/material";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class StrategicPlanningErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log the error to an error reporting service
    console.error("Strategic Planning Error Boundary caught an error:", error, errorInfo);
    
    this.setState({
      error,
      errorInfo,
    });
  }

  handleReset = (): void => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <Container maxWidth="md">
          <Box sx={{ mt: 8, mb: 4 }}>
            <Paper elevation={3} sx={{ p: 4, textAlign: "center" }}>
              <Typography variant="h4" component="h1" gutterBottom color="error">
                Terjadi Kesalahan
              </Typography>
              <Typography variant="body1" paragraph>
                Maaf, terjadi kesalahan yang tidak terduga pada modul Perencanaan Strategis.
                Silakan coba lagi atau hubungi administrator jika masalah berlanjut.
              </Typography>
              
              {this.state.error && (
                <Box sx={{ mt: 2, p: 2, bgcolor: "error.light", borderRadius: 1 }}>
                  <Typography variant="body2" component="pre" sx={{ fontSize: "0.8rem", textAlign: "left" }}>
                    {this.state.error.toString()}
                  </Typography>
                </Box>
              )}
              
              {process.env.NODE_ENV === "development" && this.state.errorInfo && (
                <Box sx={{ mt: 2, p: 2, bgcolor: "grey.100", borderRadius: 1 }}>
                  <Typography variant="body2" component="pre" sx={{ fontSize: "0.7rem", textAlign: "left" }}>
                    {this.state.errorInfo.componentStack}
                  </Typography>
                </Box>
              )}
              
              <Box sx={{ mt: 4 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={this.handleReset}
                  size="large"
                >
                  Coba Lagi
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => window.location.href = "/strategic-planning"}
                  sx={{ ml: 2 }}
                  size="large"
                >
                  Kembali ke Dashboard
                </Button>
              </Box>
            </Paper>
          </Box>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default StrategicPlanningErrorBoundary;
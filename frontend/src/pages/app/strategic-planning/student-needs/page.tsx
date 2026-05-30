import React from "react";
import { Box, Typography, Container } from "@mui/material";

const StudentNeedsPage: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Profiling Kebutuhan Murid
        </Typography>
        <Typography variant="body1">
          Profil kebutuhan murid yang ditingkatkan dengan berbagai dimensi asesmen.
        </Typography>
      </Box>
    </Container>
  );
};

export default StudentNeedsPage;
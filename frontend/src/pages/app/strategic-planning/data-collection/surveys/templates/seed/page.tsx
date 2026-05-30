import { useState } from "react";
import { Alert, Box, Button, Card, CardContent, CircularProgress, Typography, Stack } from "@mui/material";
import { seedSurveyTemplates, TEMPLATES_LIST } from "@/utils/survey-templates";
import NiCheckCircle from "@/icons/nexture/ni-check-circle";
import NiXCircle from "@/icons/nexture/ni-x-circle";

export default function SeedTemplatesPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ success: string[]; failed: string[] } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSeed = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const results = await seedSurveyTemplates();
      setResult(results);
    } catch (err: any) {
      setError(err.message || "Failed to seed templates");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box className="max-w-2xl mx-auto py-8">
      <Card>
        <CardContent className="p-6">
          <Typography variant="h5" className="mb-4 font-bold">
            Seed Survey Templates
          </Typography>

          <Typography variant="body2" className="mb-4">
            Halaman ini akan membuat 3 template survey sistem default di database:
          </Typography>

          <Stack spacing={2} className="mb-6">
            {TEMPLATES_LIST.map((template) => (
              <Box key={template.key} className="flex items-center gap-2 p-3 border rounded">
                <Typography variant="body2" className="font-medium flex-1">
                  {template.name}
                </Typography>
                <Typography variant="caption" className="text-text-secondary">
                  {template.questions.length} pertanyaan
                </Typography>
              </Box>
            ))}
          </Stack>

          {error && (
            <Alert severity="error" className="mb-4">
              {error}
            </Alert>
          )}

          {result && (
            <>
              {result.success.length > 0 && (
                <Alert severity="success" className="mb-4">
                  <Typography variant="body2" className="font-bold mb-2">
                    Berhasil dibuat ({result.success.length}):
                  </Typography>
                  {result.success.map((name) => (
                    <Box key={name} className="flex items-center gap-2 mt-1">
                      <NiCheckCircle size={16} color="success" />
                      <Typography variant="caption">{name}</Typography>
                    </Box>
                  ))}
                </Alert>
              )}

              {result.failed.length > 0 && (
                <Alert severity="error" className="mb-4">
                  <Typography variant="body2" className="font-bold mb-2">
                    Gagal dibuat ({result.failed.length}):
                  </Typography>
                  {result.failed.map((name) => (
                    <Box key={name} className="flex items-center gap-2 mt-1">
                      <NiXCircle size={16} color="error" />
                      <Typography variant="caption">{name}</Typography>
                    </Box>
                  ))}
                </Alert>
              )}
            </>
          )}

          <Button
            variant="contained"
            fullWidth
            onClick={handleSeed}
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : undefined}
          >
            {loading ? "Creating Templates..." : "Seed Templates"}
          </Button>

          <Typography variant="caption" className="text-text-secondary mt-4 block">
            Note: Template yang sudah ada akan dilewati (tidak akan duplikat).
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
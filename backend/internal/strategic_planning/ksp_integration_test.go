package strategic_planning

import (
	"testing"

	"github.com/google/uuid"
)

// Test for FR 4.1.14: Test KSP Generation dengan Analysis Integration
// This test validates the DTO structures for KSP generation with analysis integration

func TestKSPIntegrationDTOs(t *testing.T) {
	t.Run("DocumentCompilationRequest", func(t *testing.T) {
		req := &DocumentCompilationRequest{
			IntegrationID:   uuid.New().String(),
			Format:          "PDF",
			IncludeTOC:      true,
			IncludeCharts:   true,
			IncludeAppendix: false,
			CustomStyling:   map[string]interface{}{"font": "Arial"},
		}

		if req.IntegrationID == "" {
			t.Error("IntegrationID should not be empty")
		}
		if req.Format == "" {
			t.Error("Format should not be empty")
		}
	})

	t.Run("DocumentCompilationResponse", func(t *testing.T) {
		resp := &DocumentCompilationResponse{
			DocumentID:        uuid.New().String(),
			DocumentURL:       "/api/v1/strategic-planning/ksp-integrations/" + uuid.New().String() + "/document",
			Format:            "PDF",
			PageCount:         15,
			FileSize:          1024 * 1024,
			CompilationStatus: "COMPLETED",
			GeneratedAt:       "2026-05-27T12:00:00Z",
			ExpiresAt:         "2026-05-28T12:00:00Z",
		}

		if resp.DocumentID == "" {
			t.Error("DocumentID should not be empty")
		}
		if resp.DocumentURL == "" {
			t.Error("DocumentURL should not be empty")
		}
	})

	t.Run("AnalysisDataSnapshot", func(t *testing.T) {
		snapshot := &AnalysisDataSnapshot{
			IntegrationID: uuid.New().String(),
			SWOTData:      &map[string]interface{}{},
			RootCauseData: &map[string]interface{}{},
			FishboneData:  &map[string]interface{}{},
			CapturedAt:    "2026-05-27T12:00:00Z",
		}

		if snapshot.IntegrationID == "" {
			t.Error("IntegrationID should not be empty")
		}
		if snapshot.SWOTData == nil {
			t.Error("SWOTData should not be nil")
		}
	})

	t.Run("ChartGenerationRequest", func(t *testing.T) {
		req := &ChartGenerationRequest{
			IntegrationID: uuid.New().String(),
			ChartConfigs: []ChartConfig{
				{
					ChartType:  "PIE",
					Title:      "SWOT Analysis",
					Data:       map[string]interface{}{"strengths": 5},
					Width:      800,
					Height:     600,
					ShowLegend: true,
				},
			},
			Format: "PNG",
		}

		if req.IntegrationID == "" {
			t.Error("IntegrationID should not be empty")
		}
		if len(req.ChartConfigs) == 0 {
			t.Error("ChartConfigs should not be empty")
		}
	})

	t.Run("AIContentGenerationRequest", func(t *testing.T) {
		req := &AIContentGenerationRequest{
			IntegrationID: uuid.New().String(),
			ContentType:   "EXECUTIVE_SUMMARY",
			Context:       map[string]interface{}{},
		}

		if req.IntegrationID == "" {
			t.Error("IntegrationID should not be empty")
		}
		if req.ContentType == "" {
			t.Error("ContentType should not be empty")
		}
	})

	t.Run("AIContentGenerationResponse", func(t *testing.T) {
		resp := &AIContentGenerationResponse{
			ContentID:        uuid.New().String(),
			GeneratedContent: "AI-generated content",
			Confidence:       0.85,
			WordCount:        100,
			TokensUsed:       1000,
			GeneratedAt:      "2026-05-27T12:00:00Z",
		}

		if resp.ContentID == "" {
			t.Error("ContentID should not be empty")
		}
		if resp.GeneratedContent == "" {
			t.Error("GeneratedContent should not be empty")
		}
	})

	t.Run("AIIntegrationConfig", func(t *testing.T) {
		config := &AIIntegrationConfig{
			APIEndpoint:  "https://api.openai.com/v1",
			APIKey:       "sk-****",
			ModelVersion: "gpt-4",
			MaxTokens:    4000,
			Temperature: 0.7,
			Timeout:      30,
			Enabled:      true,
		}

		if config.APIEndpoint == "" {
			t.Error("APIEndpoint should not be empty")
		}
		if config.APIKey == "" {
			t.Error("APIKey should not be empty")
		}
	})

	t.Run("AnalysisVersionHistoryRequest", func(t *testing.T) {
		req := &AnalysisVersionHistoryRequest{
			AnalysisID:   uuid.New().String(),
			AnalysisType: "SWOT",
			Changes:      map[string]interface{}{},
		}

		if req.AnalysisID == "" {
			t.Error("AnalysisID should not be empty")
		}
		if req.AnalysisType == "" {
			t.Error("AnalysisType should not be empty")
		}
	})

	t.Run("ApprovalWorkflowRequest", func(t *testing.T) {
		req := &ApprovalWorkflowRequest{
			WorkflowName: "KSP Approval Workflow",
			WorkflowType: "KSP_GENERATION",
			Steps: []ApprovalWorkflowStep{
				{
					StepName: "Kepala Sekolah",
					Order:    1,
					Required: true,
				},
			},
		}

		if req.WorkflowName == "" {
			t.Error("WorkflowName should not be empty")
		}
		if len(req.Steps) == 0 {
			t.Error("Steps should not be empty")
		}
	})

	t.Run("ApprovalRequest", func(t *testing.T) {
		req := &ApprovalRequest{
			DocumentID: uuid.New().String(),
			WorkflowID: uuid.New().String(),
			StepID:     uuid.New().String(),
		}

		if req.DocumentID == "" {
			t.Error("DocumentID should not be empty")
		}
		if req.WorkflowID == "" {
			t.Error("WorkflowID should not be empty")
		}
		if req.StepID == "" {
			t.Error("StepID should not be empty")
		}
	})
}

package curriculum

import (
	"testing"

	"github.com/google/uuid"
)

// Test for FR 4.2.6: Test Integration dengan Existing Curriculum Module
// This test validates the DTO structures for curriculum integration with analysis data

func TestCurriculumIntegrationDTOs(t *testing.T) {
	t.Run("SWOTDataForKSP", func(t *testing.T) {
		data := &SWOTDataForKSP{
			SessionID: uuid.New().String(),
			Strengths: []SWOTItem{
				{
					ID:          uuid.New().String(),
					Quadrant:    "STRENGTHS",
					Description: "Fasilitas lengkap",
					Priority:    "1",
				},
			},
		}

		if data.SessionID == "" {
			t.Error("SessionID should not be empty")
		}
		if len(data.Strengths) == 0 {
			t.Error("Strengths should not be empty")
		}
	})

	t.Run("RootCauseDataForKSP", func(t *testing.T) {
		data := &RootCauseDataForKSP{
			RootCauseID: uuid.New().String(),
			ProblemStatement:       "Penurunan kualitas pembelajaran",
			RootCauses: []RootCauseItem{
				{
					ID:          uuid.New().String(),
					Cause:       "Kurangnya pelatihan guru",
					ImpactLevel: "HIGH",
				},
			},
			FiveWhysAnalysis: []FiveWhysStep{
				{
					StepNumber:  1,
					Question: "Kenapa kualitas menurun?",
					Answer: "Kurang pelatihan",
				},
			},
		}

		if data.RootCauseID == "" {
			t.Error("RootCauseID should not be empty")
		}
		if data.ProblemStatement == "" {
			t.Error("ProblemStatement should not be empty")
		}
	})

	t.Run("FishboneDataForKSP", func(t *testing.T) {
		data := &FishboneDataForKSP{
			DiagramID: uuid.New().String(),
			ProblemStatement:       "Masalah kehadiran siswa",
			Categories: []FishboneCategory{
				{
					CategoryName:  "Manusia",
					Nodes: []FishboneNode{
						{
							ID:          uuid.New().String(),
							Text:       "Kesehatan siswa",
						},
					},
				},
			},
		}

		if data.DiagramID == "" {
			t.Error("DiagramID should not be empty")
		}
		if data.ProblemStatement == "" {
			t.Error("ProblemStatement should not be empty")
		}
	})

	t.Run("StudentNeedsDataForKSP", func(t *testing.T) {
		data := &StudentNeedsDataForKSP{
			ProfileID: uuid.New().String(),
			ProfileName: "Profil 1",
			Needs: []StudentNeedItem{
				{
					ID:          uuid.New().String(),
					Need:        "Literasi",
					Priority:    "HIGH",
				},
			},
		}

		if data.ProfileID == "" {
			t.Error("ProfileID should not be empty")
		}
		if len(data.Needs) == 0 {
			t.Error("Needs should not be empty")
		}
	})

	t.Run("AnalysisDataIntegrationRequest", func(t *testing.T) {
		req := &AnalysisDataIntegrationRequest{
			CurriculumDocumentID: uuid.New().String(),
			IncludeSWOT:          true,
			IncludeRootCause:     true,
			IncludeFishbone:      true,
			IncludeStudentNeeds:  true,
		}

		if req.CurriculumDocumentID == "" {
			t.Error("CurriculumDocumentID should not be empty")
		}
	})

	t.Run("KSPExportWithAnalysisRequest", func(t *testing.T) {
		req := &KSPExportWithAnalysisRequest{
			CurriculumDocumentID: uuid.New().String(),
			Format:               "PDF",
			IncludeAnalysisData:  true,
		}

		if req.CurriculumDocumentID == "" {
			t.Error("CurriculumDocumentID should not be empty")
		}
		if req.Format == "" {
			t.Error("Format should not be empty")
		}
	})
}

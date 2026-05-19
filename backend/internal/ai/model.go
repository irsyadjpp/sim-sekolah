package ai

type GenerateNarrativeRequest struct {
	StudentName    string `json:"student_name" validate:"required"`
	ContextData    string `json:"context_data" validate:"required"` // Contoh: "Nilai IPAS 90, aktif berdiskusi"
	GenerationType string `json:"generation_type" validate:"required,oneof=competency_achieved competency_needs_improvement p5_description deep_learning_observation homeroom_notes"`
}

type GenerateNarrativeResponse struct {
	Narrative string `json:"narrative"`
}

// Struct untuk memparsing request/response ke Google Gemini API (REST)
type GeminiRequest struct {
	Contents []GeminiContent `json:"contents"`
}

type GeminiContent struct {
	Parts []GeminiPart `json:"parts"`
}

type GeminiPart struct {
	Text string `json:"text"`
}

type GeminiResponse struct {
	Candidates []GeminiCandidate `json:"candidates"`
}

type GeminiCandidate struct {
	Content GeminiContent `json:"content"`
}

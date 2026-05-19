package ai

import (
	"context"
	"errors"

	"sim-sekolah/config"
)

type AIService interface {
	GenerateNarrative(ctx context.Context, req GenerateNarrativeRequest) (string, error)
}

type aiService struct {
	repo AIRepository
}

func NewAIService(repo AIRepository) AIService {
	return &aiService{repo: repo}
}

func (s *aiService) GenerateNarrative(ctx context.Context, req GenerateNarrativeRequest) (string, error) {
	apiKey := config.GetEnv("GEMINI_API_KEY", "") // Still use Env for now if not in yaml
	if apiKey == "" {
		return "", errors.New("GEMINI_API_KEY tidak dikonfigurasi")
	}

	prompt := GetPromptTemplate(req.GenerationType, req.StudentName, req.ContextData)

	return s.repo.GenerateContent(ctx, apiKey, prompt)
}

package school

import (
	"fmt"
	"sim-sekolah/pkg/logger"
)

// TriggerContextEmbedding triggers the RAG ingestion process in the background.
// This is typically called after a school profile update.
func TriggerContextEmbedding(profil *MasterSchool) {
	// In a real implementation, this would:
	// 1. Construct the school context text
	// 2. Perform semantic chunking
	// 3. Generate embeddings via AI API (Gemini/OpenAI)
	// 4. Upsert to Vector DB (pgvector/Pinecone)

	go func() {
		contextText := fmt.Sprintf(
			"Profil Sekolah: %s (NPSN: %s). Status: %s. Jam Operasional: %s. Status BOS: %s.",
			profil.SchoolName,
			profil.NPSN,
			profil.Status,
			profil.OperatingHours,
			profil.BOSStatus,
		)

		// TODO: Call Embedding Service / RAG Pipeline
		logger.Info(fmt.Sprintf("[RAG-WORKER] Triggering embedding for school profile: %s. Content length: %d", profil.SchoolName, len(contextText)))
	}()
}

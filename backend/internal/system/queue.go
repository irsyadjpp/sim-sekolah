package system

import (
	"context"
	"encoding/json"
	"log/slog"
	"sync"
	"time"

	"sim-sekolah/pkg/logger"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

const redisQueueKey = "system:jobs"

// JobPayload is the schema for a task enqueued via Redis List
type JobPayload struct {
	JobID       uuid.UUID `json:"job_id"`
	TaskType    string    `json:"task_type"`    // 'PERUMUSAN_KSP', 'PERUMUSAN_MODUL', 'NARASI_RAPOR'
	ReferenceID uuid.UUID `json:"reference_id"` // ID of the target document/module
	UserID      uuid.UUID `json:"user_id"`
	EnqueuedAt  time.Time `json:"enqueued_at"`
}

// QueueService provides methods for enqueueing and consuming async jobs
type QueueService struct {
	rdb *redis.Client
	db  *gorm.DB
}

// NewQueueService creates a new QueueService with Redis and DB dependencies
func NewQueueService(rdb *redis.Client, db *gorm.DB) *QueueService {
	return &QueueService{rdb: rdb, db: db}
}

// Enqueue pushes a task payload onto the Redis List (LPUSH = newest first, BRPOP from right)
func (q *QueueService) Enqueue(ctx context.Context, taskType string, referenceID, userID uuid.UUID) (uuid.UUID, error) {
	payload := JobPayload{
		JobID:       uuid.New(),
		TaskType:    taskType,
		ReferenceID: referenceID,
		UserID:      userID,
		EnqueuedAt:  time.Now(),
	}

	raw, err := json.Marshal(payload)
	if err != nil {
		return uuid.Nil, err
	}

	// LPUSH onto the Redis List
	if err := q.rdb.LPush(ctx, redisQueueKey, raw).Err(); err != nil {
		return uuid.Nil, err
	}

	// Write the initial ANTREAN record into the audit DB log
	record := &AutomationQueue{
		ID:          payload.JobID,
		TaskType:    taskType,
		ReferenceID: referenceID,
		UserID:      userID,
		Status:      "ANTREAN",
		CreatedAt:   payload.EnqueuedAt,
		UpdatedAt:   payload.EnqueuedAt,
	}
	if err := q.db.WithContext(ctx).Create(record).Error; err != nil {
		logger.Error("Failed to write automation queue audit log", err, slog.String("job_id", payload.JobID.String()))
	}

	logger.Info("Job enqueued",
		slog.String("task_type", taskType),
		slog.String("job_id", payload.JobID.String()),
	)
	return payload.JobID, nil
}

// StartWorker blocks and processes jobs in parallel via a thread-safe Worker Pool
func (q *QueueService) StartWorker(ctx context.Context) {
	numWorkers := 3 // Jumlah pekerja konkruen optimal untuk server sekolah lokal
	logger.Info("System queue worker pool started",
		slog.Int("num_workers", numWorkers),
		slog.String("queue_key", redisQueueKey),
	)

	var wg sync.WaitGroup
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			q.runWorkerLoop(ctx, workerID)
		}(i)
	}

	// Wait for all workers to shut down gracefully on context cancel
	wg.Wait()
	logger.Info("All system queue workers shut down successfully")
}

func (q *QueueService) runWorkerLoop(ctx context.Context, workerID int) {
	logger.Info("Worker started", slog.Int("worker_id", workerID))
	for {
		select {
		case <-ctx.Done():
			logger.Info("Worker shutting down", slog.Int("worker_id", workerID))
			return
		default:
			// BRPOP is completely thread-safe and safe to call concurrently from multiple goroutines
			results, err := q.rdb.BRPop(ctx, 5*time.Second, redisQueueKey).Result()
			if err != nil {
				// Timeout is normal — redis.Nil is returned; check for real errors
				if err != redis.Nil && ctx.Err() == nil {
					logger.Error("Queue BRPOP error", err, slog.Int("worker_id", workerID))
				}
				continue
			}

			if len(results) < 2 {
				continue
			}

			var payload JobPayload
			if err := json.Unmarshal([]byte(results[1]), &payload); err != nil {
				logger.Error("Failed to unmarshal job payload", err, slog.Int("worker_id", workerID))
				continue
			}

			q.processJob(ctx, payload, workerID)
		}
	}
}

// processJob marks a job PROSES, simulates work, then marks SELESAI or GAGAL
func (q *QueueService) processJob(ctx context.Context, payload JobPayload, workerID int) {
	logger.Info("Processing job",
		slog.Int("worker_id", workerID),
		slog.String("task_type", payload.TaskType),
		slog.String("job_id", payload.JobID.String()),
	)

	// Detached context: Pastikan pencatatan status selesai/gagal database tetap berjalan
	// bahkan jika konteks aplikasi utama dibatalkan (graceful shutdown)
	detachedCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Mark PROSES
	if err := q.db.WithContext(detachedCtx).Model(&AutomationQueue{}).
		Where("id = ?", payload.JobID).
		Updates(map[string]interface{}{"status": "PROSES", "updated_at": time.Now()}).Error; err != nil {
		logger.Error("Failed to update status to PROSES", err, slog.String("job_id", payload.JobID.String()))
	}

	// --- TODO: wire real AI/local LLM logic here ---
	// For now, simulate processing delay
	time.Sleep(500 * time.Millisecond)

	// Mark SELESAI
	if err := q.db.WithContext(detachedCtx).Model(&AutomationQueue{}).
		Where("id = ?", payload.JobID).
		Updates(map[string]interface{}{"status": "SELESAI", "updated_at": time.Now()}).Error; err != nil {
		logger.Error("Failed to update status to SELESAI", err, slog.String("job_id", payload.JobID.String()))
	}

	logger.Info("Job completed",
		slog.Int("worker_id", workerID),
		slog.String("task_type", payload.TaskType),
		slog.String("job_id", payload.JobID.String()),
	)
}

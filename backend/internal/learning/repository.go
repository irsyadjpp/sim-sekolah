package learning

import (
	"context"
	"gorm.io/gorm"
)

type LearningRepository interface {
	CreateATP(ctx context.Context, atp *ATP) error
	GetATPByID(ctx context.Context, id string) (*ATP, error)
	CreateTeachingModule(ctx context.Context, module *TeachingModule) error
	CreateProjectModule(ctx context.Context, project *ProjectModule) error
}

type learningRepository struct {
	db *gorm.DB
}

func NewLearningRepository(db *gorm.DB) LearningRepository {
	return &learningRepository{db: db}
}

func (r *learningRepository) CreateATP(ctx context.Context, atp *ATP) error {
	return r.db.Create(atp).Error
}

func (r *learningRepository) GetATPByID(ctx context.Context, id string) (*ATP, error) {
	var atp ATP
	err := r.db.Preload("Details.Objective").First(&atp, "id = ?", id).Error
	return &atp, err
}

func (r *learningRepository) CreateTeachingModule(ctx context.Context, module *TeachingModule) error {
	return r.db.Create(module).Error
}

func (r *learningRepository) CreateProjectModule(ctx context.Context, project *ProjectModule) error {
	return r.db.Create(project).Error
}

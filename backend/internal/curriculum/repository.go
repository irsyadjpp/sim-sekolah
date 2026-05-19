package curriculum

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type CurriculumRepository interface {
	CreateDocument(ctx context.Context, doc *CurriculumDocument) error
	GetDocuments(ctx context.Context) ([]CurriculumDocument, error)
	GetDocumentByID(ctx context.Context, id uuid.UUID) (*CurriculumDocument, error)
	GetDocumentBySchoolAndYear(ctx context.Context, schoolID, academicYearID uuid.UUID) (*CurriculumDocument, error)
	UpdateDocumentStatus(ctx context.Context, id uuid.UUID, status string) error

	GetReadinessData(ctx context.Context, schoolID uuid.UUID) (*ReadinessData, error)

	GetChapter(ctx context.Context, docID uuid.UUID, chapterNumber int) (*CurriculumChapter, error)
	UpdateChapterContent(ctx context.Context, chapterID uuid.UUID, content string) error
	CountChapters(ctx context.Context, docID uuid.UUID) (int64, error)
}

type curriculumRepository struct {
	db *gorm.DB
}

func NewCurriculumRepository(db *gorm.DB) CurriculumRepository {
	return &curriculumRepository{db: db}
}

func (r *curriculumRepository) CreateDocument(ctx context.Context, doc *CurriculumDocument) error {
	return r.db.WithContext(ctx).Create(doc).Error
}

func (r *curriculumRepository) GetDocuments(ctx context.Context) ([]CurriculumDocument, error) {
	var docs []CurriculumDocument
	if err := r.db.WithContext(ctx).Preload("AcademicYear").Order("created_at desc").Find(&docs).Error; err != nil {
		return nil, err
	}
	return docs, nil
}

func (r *curriculumRepository) GetDocumentByID(ctx context.Context, id uuid.UUID) (*CurriculumDocument, error) {
	var doc CurriculumDocument
	if err := r.db.WithContext(ctx).Preload("AcademicYear").Preload("Chapters").First(&doc, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &doc, nil
}

func (r *curriculumRepository) GetDocumentBySchoolAndYear(ctx context.Context, schoolID, academicYearID uuid.UUID) (*CurriculumDocument, error) {
	var doc CurriculumDocument
	if err := r.db.WithContext(ctx).Where("school_id = ? AND academic_year_id = ?", schoolID, academicYearID).First(&doc).Error; err != nil {
		return nil, err
	}
	return &doc, nil
}

func (r *curriculumRepository) UpdateDocumentStatus(ctx context.Context, id uuid.UUID, status string) error {
	return r.db.WithContext(ctx).Model(&CurriculumDocument{}).Where("id = ?", id).Update("status", status).Error
}

func (r *curriculumRepository) GetReadinessData(ctx context.Context, schoolID uuid.UUID) (*ReadinessData, error) {
	var data ReadinessData
	if err := r.db.WithContext(ctx).Where("school_id = ?", schoolID).First(&data).Error; err != nil {
		return nil, err
	}
	return &data, nil
}

func (r *curriculumRepository) GetChapter(ctx context.Context, docID uuid.UUID, chapterNumber int) (*CurriculumChapter, error) {
	var chapter CurriculumChapter
	if err := r.db.WithContext(ctx).Where("curriculum_document_id = ? AND chapter_number = ?", docID, chapterNumber).First(&chapter).Error; err != nil {
		return nil, err
	}
	return &chapter, nil
}

func (r *curriculumRepository) UpdateChapterContent(ctx context.Context, chapterID uuid.UUID, content string) error {
	return r.db.WithContext(ctx).Model(&CurriculumChapter{}).Where("id = ?", chapterID).Update("content", content).Error
}

func (r *curriculumRepository) CountChapters(ctx context.Context, docID uuid.UUID) (int64, error) {
	var count int64
	err := r.db.WithContext(ctx).Model(&CurriculumChapter{}).Where("curriculum_document_id = ? AND content != '' AND content IS NOT NULL", docID).Count(&count).Error
	return count, err
}

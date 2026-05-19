package cp

import (
	"context"
	"errors"
	"fmt"
	"strings"

	"sim-sekolah/internal/common"
	"sim-sekolah/internal/phase"
	"sim-sekolah/internal/subject"

	"github.com/google/uuid"
)

// CPService defines the business logic for LearningOutcome and its Details.
type CPService interface {
	GetAll(pagination common.Pagination, search string) ([]LearningOutcome, int64, error)
	GetByID(id string) (*LearningOutcome, error)
	Create(ctx context.Context, req CreateCPRequest) (*LearningOutcome, error)
	Update(ctx context.Context, id string, req UpdateCPRequest) (*LearningOutcome, error)
	Delete(ctx context.Context, id string) error

	// Details
	GetAllDetails(cpID string) ([]CPDetail, error)
	CreateDetail(ctx context.Context, cpID string, req CreateCPDetailRequest) (*CPDetail, error)
	UpdateDetail(ctx context.Context, cpID, detailID string, req UpdateCPDetailRequest) (*CPDetail, error)
	DeleteDetail(ctx context.Context, cpID, detailID string) error

	// TP (Tujuan Pembelajaran)
	GetAllObjectives(cpID string) ([]LearningObjective, error)
	CreateObjective(ctx context.Context, cpID string, req CreateTPRequest) (*LearningObjective, error)
	DeleteObjective(ctx context.Context, cpID, objectiveID string) error
}

type cpService struct {
	cpRepo     CPRepository
	detailRepo CPDetailRepository
	tpRepo     LearningObjectiveRepository
	subRepo    subject.SubjectRepository
	phaseRepo  phase.PhaseRepository
	elemRepo   subject.SubjectElementRepository
}

// NewCPService creates a new CPService with injected repositories.
func NewCPService(
	cpRepo CPRepository,
	detailRepo CPDetailRepository,
	tpRepo LearningObjectiveRepository,
	subRepo subject.SubjectRepository,
	phaseRepo phase.PhaseRepository,
	elemRepo subject.SubjectElementRepository,
) CPService {
	return &cpService{
		cpRepo:     cpRepo,
		detailRepo: detailRepo,
		tpRepo:     tpRepo,
		subRepo:    subRepo,
		phaseRepo:  phaseRepo,
		elemRepo:   elemRepo,
	}
}

func (s *cpService) GetAll(pagination common.Pagination, search string) ([]LearningOutcome, int64, error) {
	return s.cpRepo.GetAll(pagination.Limit, pagination.Offset, search)
}

func (s *cpService) GetByID(id string) (*LearningOutcome, error) {
	return s.cpRepo.GetByID(id)
}

func (s *cpService) Create(ctx context.Context, req CreateCPRequest) (*LearningOutcome, error) {
	// Check for duplicate ElementIDs in request payload
	elementSeen := make(map[string]bool)
	for _, d := range req.Details {
		if d.ElementID == "" {
			continue
		}
		if elementSeen[d.ElementID] {
			return nil, errors.New("terdapat duplikasi elemen pada detail capaian pembelajaran")
		}
		elementSeen[d.ElementID] = true
	}

	phaseUUID, _ := uuid.Parse(req.PhaseID)
	subjectUUID, _ := uuid.Parse(req.SubjectID)

	// Fetch related data for code generation
	sub, err := s.subRepo.GetByID(req.SubjectID)
	if err != nil || sub == nil {
		return nil, errors.New("mata pelajaran tidak valid atau tidak ditemukan")
	}
	ph, err := s.phaseRepo.GetByID(req.PhaseID)
	if err != nil || ph == nil {
		return nil, errors.New("fase pembelajaran tidak valid atau tidak ditemukan")
	}

	// Generate CP Code: CP-[TahunSK]-[Mapel]-[Fase]
	// Example: CP-26-MTK-A
	phaseCode := strings.TrimPrefix(strings.ToUpper(ph.Code), "FAS-")
	cpCode := strings.ToUpper(fmt.Sprintf("CP-%s-%s-%s", req.YearSK, sub.Abbreviation, phaseCode))

	// Compact CP Code for Elements: CP26MTKA
	compactCPCode := strings.ReplaceAll(cpCode, "-", "")

	cp := &LearningOutcome{
		PhaseID:     phaseUUID,
		SubjectID:   subjectUUID,
		CPCode:      cpCode,
		YearSK:      req.YearSK,
		OutcomeText: req.OutcomeText,
	}

	for _, d := range req.Details {
		elementUUID, _ := uuid.Parse(d.ElementID)
		// Fetch element abbreviation
		elem, err := s.elemRepo.GetByID(d.ElementID)
		elemAbbr := ""
		if err == nil {
			elemAbbr = elem.Abbreviation
		}

		// Generate Element Code: ELM-[KodeCP]-[SingkatanElemen]
		subCode := strings.ToUpper(fmt.Sprintf("ELM-%s-%s", compactCPCode, elemAbbr))

		cp.Details = append(cp.Details, CPDetail{
			ElementID:  elementUUID,
			SubCode:    subCode,
			DetailText: d.DetailText,
			SequenceNo: d.SequenceNo,
		})
	}

	if err := s.cpRepo.Create(ctx, cp); err != nil {
		return nil, err
	}

	return cp, nil
}

func (s *cpService) Update(ctx context.Context, id string, req UpdateCPRequest) (*LearningOutcome, error) {
	cp, err := s.cpRepo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, cp.CreatedBy); err != nil {
		return nil, err
	}

	if req.PhaseID != "" {
		phaseUUID, _ := uuid.Parse(req.PhaseID)
		cp.PhaseID = phaseUUID
	}
	if req.SubjectID != "" {
		subjectUUID, _ := uuid.Parse(req.SubjectID)
		cp.SubjectID = subjectUUID
	}
	if req.CPCode != "" {
		cp.CPCode = req.CPCode
	}
	if req.OutcomeText != "" {
		cp.OutcomeText = req.OutcomeText
	}

	if len(req.Details) > 0 {
		elementSeen := make(map[string]bool)
		var details []CPDetail
		for _, d := range req.Details {
			if d.ElementID == "" {
				continue
			}
			if elementSeen[d.ElementID] {
				return nil, errors.New("terdapat duplikasi elemen pada detail capaian pembelajaran")
			}
			elementSeen[d.ElementID] = true

			elementUUID, _ := uuid.Parse(d.ElementID)
			details = append(details, CPDetail{
				ElementID:  elementUUID,
				SubCode:    d.SubCode,
				DetailText: d.DetailText,
				SequenceNo: d.SequenceNo,
			})
		}
		cp.Details = details
	}

	if err := s.cpRepo.Update(ctx, cp); err != nil {
		return nil, err
	}

	return cp, nil
}

func (s *cpService) Delete(ctx context.Context, id string) error {
	cp, err := s.cpRepo.GetByID(id)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, cp.CreatedBy); err != nil {
		return err
	}

	return s.cpRepo.Delete(ctx, id)
}

// ========================
// Detail Methods
// ========================

func (s *cpService) GetAllDetails(cpID string) ([]CPDetail, error) {
	if _, err := s.cpRepo.GetByID(cpID); err != nil {
		return nil, err
	}
	return s.detailRepo.GetAllByCP(cpID)
}

func (s *cpService) CreateDetail(ctx context.Context, cpID string, req CreateCPDetailRequest) (*CPDetail, error) {
	cp, err := s.cpRepo.GetByID(cpID)
	if err != nil {
		return nil, err
	}

	elementUUID, _ := uuid.Parse(req.ElementID)
	detail := &CPDetail{
		LearningOutcomeID: cp.ID,
		ElementID:         elementUUID,
		SubCode:           req.SubCode,
		DetailText:        req.DetailText,
		SequenceNo:        req.SequenceNo,
	}

	if err := s.detailRepo.Create(ctx, detail); err != nil {
		return nil, err
	}

	return detail, nil
}

func (s *cpService) UpdateDetail(ctx context.Context, cpID, detailID string, req UpdateCPDetailRequest) (*CPDetail, error) {
	detail, err := s.detailRepo.GetByID(detailID)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, detail.CreatedBy); err != nil {
		return nil, err
	}

	cpUUID, _ := uuid.Parse(cpID)
	if detail.LearningOutcomeID != cpUUID {
		return nil, errors.New("detail not belongs to this learning outcome")
	}

	if req.ElementID != "" {
		elementUUID, _ := uuid.Parse(req.ElementID)
		detail.ElementID = elementUUID
	}
	if req.SubCode != "" {
		detail.SubCode = req.SubCode
	}
	if req.DetailText != "" {
		detail.DetailText = req.DetailText
	}
	if req.SequenceNo > 0 {
		detail.SequenceNo = req.SequenceNo
	}

	if err := s.detailRepo.Update(ctx, detail); err != nil {
		return nil, err
	}

	return detail, nil
}

func (s *cpService) DeleteDetail(ctx context.Context, cpID, detailID string) error {
	detail, err := s.detailRepo.GetByID(detailID)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, detail.CreatedBy); err != nil {
		return err
	}

	cpUUID, _ := uuid.Parse(cpID)
	if detail.LearningOutcomeID != cpUUID {
		return errors.New("detail not belongs to this learning outcome")
	}

	return s.detailRepo.Delete(ctx, detailID)
}

// TP Methods
func (s *cpService) GetAllObjectives(cpID string) ([]LearningObjective, error) {
	return s.tpRepo.GetAllByCP(cpID)
}

func (s *cpService) CreateObjective(ctx context.Context, cpID string, req CreateTPRequest) (*LearningObjective, error) {
	cpUUID, _ := uuid.Parse(cpID)
	tp := &LearningObjective{
		LearningOutcomeID: cpUUID,
		Description:       req.Description,
	}
	if err := s.tpRepo.Create(ctx, tp); err != nil {
		return nil, err
	}
	return tp, nil
}

func (s *cpService) DeleteObjective(ctx context.Context, cpID, objectiveID string) error {
	return s.tpRepo.Delete(ctx, objectiveID)
}

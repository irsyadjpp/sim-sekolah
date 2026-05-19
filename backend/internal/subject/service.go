package subject

import (
	"context"
	"errors"
	"regexp"
	"strings"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// SubjectService mendefinisikan business logic untuk Subject dan SubjectElement
type SubjectService interface {
	GetAll(pagination common.Pagination, search string, isActive *bool) ([]Subject, int64, error)
	GetByID(id string) (*Subject, error)
	Create(ctx context.Context, req CreateSubjectRequest) (*Subject, error)
	Update(ctx context.Context, id string, req UpdateSubjectRequest) (*Subject, error)
	Delete(ctx context.Context, id string) error

	// Elements
	GetAllElements(subjectID string) ([]SubjectElement, error)
	CreateElement(ctx context.Context, subjectID string, req CreateSubjectElementRequest) (*SubjectElement, error)
	UpdateElement(ctx context.Context, subjectID, elementID string, req UpdateSubjectElementRequest) (*SubjectElement, error)
	DeleteElement(ctx context.Context, subjectID, elementID string) error
}

type subjectService struct {
	subRepo  SubjectRepository
	elemRepo SubjectElementRepository
}

// NewSubjectService creates a new SubjectService with injected repositories.
func NewSubjectService(subRepo SubjectRepository, elemRepo SubjectElementRepository) SubjectService {
	return &subjectService{
		subRepo:  subRepo,
		elemRepo: elemRepo,
	}
}

// ========================
// Subject Methods
// ========================

func (s *subjectService) GetAll(pagination common.Pagination, search string, isActive *bool) ([]Subject, int64, error) {
	return s.subRepo.GetAll(pagination.Limit, pagination.Offset, search, isActive)
}

func (s *subjectService) GetByID(id string) (*Subject, error) {
	return s.subRepo.GetByID(id)
}

func (s *subjectService) Create(ctx context.Context, req CreateSubjectRequest) (*Subject, error) {
	level := req.Level
	if level == "" {
		level = "SD"
	}

	abbr := req.Abbreviation
	if abbr == "" {
		abbr = generateAbbreviation(req.SubjectName)
	}

	sub := &Subject{
		SubjectCode:     req.SubjectCode,
		SubjectName:     req.SubjectName,
		Rational:        req.Rational,
		Goals:           req.Goals,
		Characteristics: req.Characteristics,
		Level:           level,
		Abbreviation:    abbr,
	}

	if req.IsActive != nil {
		sub.IsActive = *req.IsActive
	} else {
		sub.IsActive = true
	}

	for _, p := range req.CharacteristicPoints {
		cp := CharacteristicPoint{
			Description: p.Description,
		}
		for _, e := range p.Elements {
			eAbbr := e.Abbreviation
			if eAbbr == "" {
				eAbbr = generateAbbreviation(e.ElementName)
			}
			cp.Elements = append(cp.Elements, SubjectElement{
				SubjectID:    sub.ID,
				ElementName:  e.ElementName,
				Abbreviation: eAbbr,
				Description:  e.Description,
			})
		}
		sub.CharacteristicPoints = append(sub.CharacteristicPoints, cp)
	}

	if err := s.subRepo.Create(ctx, sub); err != nil {
		return nil, err
	}

	return sub, nil
}

func (s *subjectService) Update(ctx context.Context, id string, req UpdateSubjectRequest) (*Subject, error) {
	sub, err := s.subRepo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, sub.CreatedBy); err != nil {
		return nil, err
	}

	if req.SubjectCode != "" {
		sub.SubjectCode = req.SubjectCode
	}
	if req.SubjectName != "" {
		sub.SubjectName = req.SubjectName
	}
	if req.Level != "" {
		sub.Level = req.Level
	}
	if req.Abbreviation != "" {
		sub.Abbreviation = req.Abbreviation
	}
	if req.IsActive != nil {
		sub.IsActive = *req.IsActive
	}
	if req.Rational != "" {
		sub.Rational = req.Rational
	}
	if req.Goals != "" {
		sub.Goals = req.Goals
	}
	if req.Characteristics != "" {
		sub.Characteristics = req.Characteristics
	}

	// Handle nested CharacteristicPoints if provided
	if req.CharacteristicPoints != nil {
		var points []CharacteristicPoint
		for _, p := range req.CharacteristicPoints {
			cp := CharacteristicPoint{
				SubjectID:   sub.ID,
				Description: p.Description,
			}
			if p.ID != "" {
				if uid, err := uuid.Parse(p.ID); err == nil {
					cp.ID = uid
				}
			}
			for _, e := range p.Elements {
				eAbbr := e.Abbreviation
				if eAbbr == "" {
					eAbbr = generateAbbreviation(e.ElementName)
				}
				se := SubjectElement{
					SubjectID:    sub.ID,
					ElementName:  e.ElementName,
					Abbreviation: eAbbr,
					Description:  e.Description,
				}
				if e.ID != "" {
					if uid, err := uuid.Parse(e.ID); err == nil {
						se.ID = uid
					}
				}
				cp.Elements = append(cp.Elements, se)
			}
			points = append(points, cp)
		}
		sub.CharacteristicPoints = points
	}

	if err := s.subRepo.Update(ctx, sub); err != nil {
		return nil, err
	}

	return sub, nil
}

func (s *subjectService) Delete(ctx context.Context, id string) error {
	sub, err := s.subRepo.GetByID(id)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, sub.CreatedBy); err != nil {
		return err
	}

	return s.subRepo.Delete(ctx, id)
}

// ========================
// SubjectElement Methods
// ========================

func (s *subjectService) GetAllElements(subjectID string) ([]SubjectElement, error) {
	// Verifikasi subject ada
	if _, err := s.subRepo.GetByID(subjectID); err != nil {
		return nil, err
	}
	return s.elemRepo.GetAllBySubject(subjectID)
}

func (s *subjectService) CreateElement(ctx context.Context, subjectID string, req CreateSubjectElementRequest) (*SubjectElement, error) {
	// Verifikasi subject ada
	sub, err := s.subRepo.GetByID(subjectID)
	if err != nil {
		return nil, err
	}

	elem := &SubjectElement{
		SubjectID:   sub.ID,
		ElementName: req.ElementName,
		Description: req.Description,
	}

	if err := s.elemRepo.Create(ctx, elem); err != nil {
		return nil, err
	}

	return elem, nil
}

func (s *subjectService) UpdateElement(ctx context.Context, subjectID, elementID string, req UpdateSubjectElementRequest) (*SubjectElement, error) {
	// Verifikasi element ada
	elem, err := s.elemRepo.GetByID(elementID)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, elem.CreatedBy); err != nil {
		return nil, err
	}

	// Verifikasi element milik subject tersebut
	subUUID, _ := uuid.Parse(subjectID)
	if elem.SubjectID != subUUID {
		return nil, errors.New("element not belongs to this subject")
	}

	if req.ElementName != "" {
		elem.ElementName = req.ElementName
	}

	if req.Abbreviation != "" {
		elem.Abbreviation = req.Abbreviation
	} else if req.ElementName != "" {
		elem.Abbreviation = generateAbbreviation(req.ElementName)
	}

	elem.Description = req.Description

	if err := s.elemRepo.Update(ctx, elem); err != nil {
		return nil, err
	}

	return elem, nil
}

func (s *subjectService) DeleteElement(ctx context.Context, subjectID, elementID string) error {
	elem, err := s.elemRepo.GetByID(elementID)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, elem.CreatedBy); err != nil {
		return err
	}

	subUUID, _ := uuid.Parse(subjectID)
	if elem.SubjectID != subUUID {
		return errors.New("element not belongs to this subject")
	}

	return s.elemRepo.Delete(ctx, elementID)
}
func generateAbbreviation(name string) string {
	// Predefined common abbreviations
	commonAbbrs := map[string]string{
		"MATEMATIKA":              "MTK",
		"BAHASA INDONESIA":        "BIN",
		"BAHASA INGGRIS":          "BIG",
		"PENDIDIKAN AGAMA":        "PAI",
		"ILMU PENGETAHUAN ALAM":   "IPA",
		"ILMU PENGETAHUAN SOSIAL": "IPS",
		"PENDIDIKAN PANCASILA":    "PPN",
	}

	upperName := strings.ToUpper(strings.TrimSpace(name))
	if abbr, ok := commonAbbrs[upperName]; ok {
		return abbr
	}

	// Clean name from non-alphanumeric
	reg, _ := regexp.Compile("[^a-zA-Z0-9 ]+")
	cleanName := reg.ReplaceAllString(upperName, "")
	words := strings.Fields(cleanName)

	if len(words) >= 2 {
		// Take first char of each word
		abbr := ""
		for _, w := range words {
			if len(w) > 0 {
				abbr += string(w[0])
			}
		}
		if len(abbr) < 3 && len(words) == 2 {
			// If only 2 words and resulting abbr is too short, take more chars
			abbr = string(words[0][0]) + string(words[1][:2])
		}
		return strings.ToUpper(abbr)
	}

	// Single word: take first 3 chars
	if len(cleanName) > 3 {
		return cleanName[:3]
	}
	return cleanName
}

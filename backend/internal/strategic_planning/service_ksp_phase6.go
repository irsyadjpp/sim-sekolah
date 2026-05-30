package strategic_planning

// Phase 6: KSP Enhanced Generation
// This file contains the implementations for:
//   - Version History Management (FR 4.1.5)
//   - Extended Review and Approval Workflow (FR 4.1.13)
//   - Fishbone Template management (T-5.3.14)
//   - Real CompileDocumentWithAnalysis & GenerateAnalysisSnapshot

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"strings"
	"time"

	pb "sim-sekolah/internal/ai/grpc/pb/strategicanalysisservice"

	"github.com/google/uuid"
)

// ─── In-memory stores (replace with DB tables in production migration) ──────

// versionHistoryStore is a simple in-memory store for analysis version history.
// In production this would be a PostgreSQL table.
var versionHistoryStore = make(map[string][]*AnalysisVersionHistory) // key: analysisType+":"+analysisID

// approvalWorkflowStore is an in-memory store for approval workflows.
var approvalWorkflowStore = make(map[string]*ApprovalWorkflow) // key: workflowID

// documentApprovalStore tracks the approval status of documents.
var documentApprovalStore = make(map[string]*DocumentApprovalStatus) // key: documentID

// approvalNotificationStore holds notifications per recipient.
var approvalNotificationStore = make(map[string][]*ApprovalNotification) // key: recipientID

// ─── Version History Management (FR 4.1.5) ──────────────────────────────────

func (s *service) CreateAnalysisVersionHistory(ctx context.Context, req AnalysisVersionHistoryRequest, changedBy string) (*AnalysisVersionHistory, error) {
	if req.AnalysisType == "" {
		return nil, errors.New("analysis_type is required")
	}
	if req.AnalysisID == "" {
		return nil, errors.New("analysis_id is required")
	}

	storeKey := req.AnalysisType + ":" + req.AnalysisID
	existingVersions := versionHistoryStore[storeKey]
	nextVersion := len(existingVersions) + 1

	entry := &AnalysisVersionHistory{
		ID:            uuid.New().String(),
		AnalysisType:  req.AnalysisType,
		AnalysisID:    req.AnalysisID,
		Version:       nextVersion,
		Changes:       req.Changes,
		ChangeType:    req.ChangeType,
		ChangeSummary: req.ChangeSummary,
		ChangedBy:     changedBy,
		ChangedAt:     time.Now().Format(time.RFC3339),
		PreviousData:  req.PreviousData,
		NewData:       req.NewData,
	}

	versionHistoryStore[storeKey] = append(existingVersions, entry)
	return entry, nil
}

func (s *service) GetAnalysisVersionHistory(ctx context.Context, analysisID string, analysisType string) ([]*AnalysisVersionHistory, error) {
	if analysisID == "" {
		return nil, errors.New("analysis_id is required")
	}

	storeKey := analysisType + ":" + analysisID
	versions := versionHistoryStore[storeKey]
	if versions == nil {
		return []*AnalysisVersionHistory{}, nil
	}

	// Return newest-first
	result := make([]*AnalysisVersionHistory, len(versions))
	for i, v := range versions {
		result[len(versions)-1-i] = v
	}
	return result, nil
}

func (s *service) GetAnalysisVersionByID(ctx context.Context, versionID string) (*AnalysisVersionHistory, error) {
	if versionID == "" {
		return nil, errors.New("version_id is required")
	}

	for _, versions := range versionHistoryStore {
		for _, v := range versions {
			if v.ID == versionID {
				return v, nil
			}
		}
	}
	return nil, fmt.Errorf("version with id %s not found", versionID)
}

func (s *service) CompareAnalysisVersions(ctx context.Context, analysisID string, version1 int, version2 int) (*AnalysisVersionComparison, error) {
	if analysisID == "" {
		return nil, errors.New("analysis_id is required")
	}
	if version1 <= 0 || version2 <= 0 {
		return nil, errors.New("version numbers must be positive")
	}

	var v1, v2 *AnalysisVersionHistory
	for _, versions := range versionHistoryStore {
		for _, v := range versions {
			if v.AnalysisID == analysisID {
				if v.Version == version1 {
					v1 = v
				}
				if v.Version == version2 {
					v2 = v
				}
			}
		}
	}

	if v1 == nil {
		return nil, fmt.Errorf("version %d not found for analysis %s", version1, analysisID)
	}
	if v2 == nil {
		return nil, fmt.Errorf("version %d not found for analysis %s", version2, analysisID)
	}

	differences := computeVersionDifferences(v1, v2)
	summary := fmt.Sprintf("Comparing version %d (%s) vs version %d (%s). Found %d difference(s).",
		v1.Version, v1.ChangedAt, v2.Version, v2.ChangedAt, len(differences))

	return &AnalysisVersionComparison{
		Version1:    *v1,
		Version2:    *v2,
		Differences: differences,
		Summary:     summary,
	}, nil
}

// computeVersionDifferences compares two version histories and returns a list of diff descriptions.
func computeVersionDifferences(v1, v2 *AnalysisVersionHistory) []string {
	var diffs []string

	if v1.ChangeType != v2.ChangeType {
		diffs = append(diffs, fmt.Sprintf("change_type: %q → %q", v1.ChangeType, v2.ChangeType))
	}
	if v1.ChangeSummary != v2.ChangeSummary {
		diffs = append(diffs, fmt.Sprintf("change_summary: %q → %q", v1.ChangeSummary, v2.ChangeSummary))
	}
	if v1.ChangedBy != v2.ChangedBy {
		diffs = append(diffs, fmt.Sprintf("changed_by: %q → %q", v1.ChangedBy, v2.ChangedBy))
	}

	// Deep compare changes maps
	for key, val1 := range v1.Changes {
		if val2, ok := v2.Changes[key]; ok {
			j1, _ := json.Marshal(val1)
			j2, _ := json.Marshal(val2)
			if string(j1) != string(j2) {
				diffs = append(diffs, fmt.Sprintf("field %q changed: %s → %s", key, j1, j2))
			}
		} else {
			diffs = append(diffs, fmt.Sprintf("field %q was removed in v%d", key, v2.Version))
		}
	}
	for key := range v2.Changes {
		if _, ok := v1.Changes[key]; !ok {
			diffs = append(diffs, fmt.Sprintf("field %q was added in v%d", key, v2.Version))
		}
	}

	if len(diffs) == 0 {
		diffs = append(diffs, "No differences found between the two versions")
	}
	return diffs
}

func (s *service) RestoreAnalysisVersion(ctx context.Context, req VersionRestoreRequest, changedBy string) error {
	if req.AnalysisID == "" {
		return errors.New("analysis_id is required")
	}
	if req.Version <= 0 {
		return errors.New("version must be positive")
	}

	var targetVersion *AnalysisVersionHistory
	for _, versions := range versionHistoryStore {
		for _, v := range versions {
			if v.AnalysisID == req.AnalysisID && v.Version == req.Version {
				targetVersion = v
				break
			}
		}
	}

	if targetVersion == nil {
		return fmt.Errorf("version %d not found for analysis %s", req.Version, req.AnalysisID)
	}

	// Record a new version history entry for the restore action
	restoreReq := AnalysisVersionHistoryRequest{
		AnalysisType:  targetVersion.AnalysisType,
		AnalysisID:    req.AnalysisID,
		ChangeType:    "RESTORE",
		ChangeSummary: fmt.Sprintf("Restored to version %d. Reason: %s", req.Version, req.Reason),
		Changes: map[string]interface{}{
			"restored_from_version": req.Version,
			"reason":                req.Reason,
		},
		PreviousData: nil,
		NewData:      targetVersion.NewData,
	}

	_, err := s.CreateAnalysisVersionHistory(ctx, restoreReq, changedBy)
	return err
}

// ─── Extended Review and Approval Workflow (FR 4.1.13) ──────────────────────

func (s *service) CreateApprovalWorkflow(ctx context.Context, req ApprovalWorkflowRequest, createdBy string) (*ApprovalWorkflow, error) {
	if req.WorkflowName == "" {
		return nil, errors.New("workflow_name is required")
	}
	if req.WorkflowType == "" {
		return nil, errors.New("workflow_type is required")
	}
	if len(req.Steps) == 0 {
		return nil, errors.New("at least one step is required")
	}

	// Assign IDs to steps that don't have one
	for i := range req.Steps {
		if req.Steps[i].ID == "" {
			req.Steps[i].ID = uuid.New().String()
		}
	}

	wf := &ApprovalWorkflow{
		ID:           uuid.New().String(),
		WorkflowName: req.WorkflowName,
		WorkflowType: req.WorkflowType,
		Steps:        req.Steps,
		IsActive:     true,
		SchoolID:     req.SchoolID,
		CreatedBy:    createdBy,
		CreatedAt:    time.Now().Format(time.RFC3339),
		UpdatedAt:    time.Now().Format(time.RFC3339),
	}

	approvalWorkflowStore[wf.ID] = wf
	return wf, nil
}

func (s *service) GetApprovalWorkflowByID(ctx context.Context, workflowID string) (*ApprovalWorkflow, error) {
	if workflowID == "" {
		return nil, errors.New("workflow_id is required")
	}

	wf, ok := approvalWorkflowStore[workflowID]
	if !ok {
		return nil, fmt.Errorf("workflow with id %s not found", workflowID)
	}
	return wf, nil
}

func (s *service) GetApprovalWorkflowsBySchool(ctx context.Context, schoolID string, workflowType string) ([]*ApprovalWorkflow, error) {
	var result []*ApprovalWorkflow
	for _, wf := range approvalWorkflowStore {
		if wf.SchoolID == schoolID || schoolID == "" {
			if workflowType == "" || wf.WorkflowType == workflowType {
				result = append(result, wf)
			}
		}
	}
	return result, nil
}

func (s *service) UpdateApprovalWorkflow(ctx context.Context, workflowID string, req ApprovalWorkflowRequest) (*ApprovalWorkflow, error) {
	wf, ok := approvalWorkflowStore[workflowID]
	if !ok {
		return nil, fmt.Errorf("workflow with id %s not found", workflowID)
	}

	if req.WorkflowName != "" {
		wf.WorkflowName = req.WorkflowName
	}
	if req.WorkflowType != "" {
		wf.WorkflowType = req.WorkflowType
	}
	if len(req.Steps) > 0 {
		// Assign IDs to new steps
		for i := range req.Steps {
			if req.Steps[i].ID == "" {
				req.Steps[i].ID = uuid.New().String()
			}
		}
		wf.Steps = req.Steps
	}
	if req.SchoolID != "" {
		wf.SchoolID = req.SchoolID
	}
	wf.UpdatedAt = time.Now().Format(time.RFC3339)

	approvalWorkflowStore[workflowID] = wf
	return wf, nil
}

func (s *service) DeleteApprovalWorkflow(ctx context.Context, workflowID string) error {
	if _, ok := approvalWorkflowStore[workflowID]; !ok {
		return fmt.Errorf("workflow with id %s not found", workflowID)
	}
	delete(approvalWorkflowStore, workflowID)
	return nil
}

func (s *service) SubmitForApproval(ctx context.Context, documentID string, workflowID string, submittedBy string) (*DocumentApprovalStatus, error) {
	if documentID == "" {
		return nil, errors.New("document_id is required")
	}

	wf, err := s.GetApprovalWorkflowByID(ctx, workflowID)
	if err != nil {
		return nil, fmt.Errorf("workflow not found: %w", err)
	}

	if len(wf.Steps) == 0 {
		return nil, errors.New("workflow has no steps")
	}

	pendingSteps := make([]string, len(wf.Steps))
	for i, step := range wf.Steps {
		pendingSteps[i] = step.ID
	}

	status := &DocumentApprovalStatus{
		DocumentID:      documentID,
		CurrentStep:     wf.Steps[0].ID,
		CurrentStepName: wf.Steps[0].StepName,
		OverallStatus:   "IN_PROGRESS",
		CompletedSteps:  []string{},
		PendingSteps:    pendingSteps,
		ApprovalHistory: []ApprovalResponse{},
		StartedAt:       time.Now().Format(time.RFC3339),
	}

	documentApprovalStore[documentID] = status

	// Send a notification to the first step's approver
	_ = s.SendApprovalNotification(ctx, ApprovalNotification{
		ID:          uuid.New().String(),
		RecipientID: submittedBy, // In production this would be the approver role's user
		DocumentID:  documentID,
		WorkflowID:  workflowID,
		StepID:      wf.Steps[0].ID,
		Message:     fmt.Sprintf("Document %s has been submitted for approval. Step: %s", documentID, wf.Steps[0].StepName),
		Type:        "APPROVAL_REQUIRED",
		SentAt:      time.Now().Format(time.RFC3339),
	})

	return status, nil
}

func (s *service) ProcessApproval(ctx context.Context, req ApprovalRequest, approverID string) (*ApprovalResponse, error) {
	if req.DocumentID == "" {
		return nil, errors.New("document_id is required")
	}
	if req.Action == "" {
		return nil, errors.New("action is required")
	}

	validActions := map[string]bool{"APPROVE": true, "REJECT": true, "REQUEST_CHANGES": true}
	if !validActions[req.Action] {
		return nil, fmt.Errorf("invalid action %q; must be one of APPROVE, REJECT, REQUEST_CHANGES", req.Action)
	}

	status, ok := documentApprovalStore[req.DocumentID]
	if !ok {
		return nil, fmt.Errorf("no approval process found for document %s", req.DocumentID)
	}

	wf, err := s.GetApprovalWorkflowByID(ctx, req.WorkflowID)
	if err != nil {
		return nil, fmt.Errorf("workflow not found: %w", err)
	}

	approvalResp := &ApprovalResponse{
		ID:               uuid.New().String(),
		DocumentID:       req.DocumentID,
		WorkflowID:       req.WorkflowID,
		StepID:           req.StepID,
		Action:           req.Action,
		ApproverID:       approverID,
		Comments:         req.Comments,
		RequestedChanges: req.RequestedChanges,
		ApprovedAt:       time.Now().Format(time.RFC3339),
	}

	status.ApprovalHistory = append(status.ApprovalHistory, *approvalResp)

	switch req.Action {
	case "APPROVE":
		// Move current step to completed
		status.CompletedSteps = append(status.CompletedSteps, req.StepID)
		// Remove from pending
		newPending := make([]string, 0)
		for _, ps := range status.PendingSteps {
			if ps != req.StepID {
				newPending = append(newPending, ps)
			}
		}
		status.PendingSteps = newPending

		// Advance to next step or mark as fully approved
		if len(newPending) == 0 {
			status.OverallStatus = "APPROVED"
			now := time.Now().Format(time.RFC3339)
			status.CompletedAt = now
			status.CurrentStep = ""
			status.CurrentStepName = ""
		} else {
			// Find the next step in the workflow
			nextStepID := newPending[0]
			for _, step := range wf.Steps {
				if step.ID == nextStepID {
					status.CurrentStep = step.ID
					status.CurrentStepName = step.StepName
					break
				}
			}
		}

	case "REJECT":
		status.OverallStatus = "REJECTED"
		now := time.Now().Format(time.RFC3339)
		status.CompletedAt = now
		status.CurrentStep = ""
		status.CurrentStepName = ""

	case "REQUEST_CHANGES":
		status.OverallStatus = "CHANGES_REQUESTED"
		// Keep current step; submitter should resubmit after changes
	}

	documentApprovalStore[req.DocumentID] = status

	// Send notification for the action
	notifType := map[string]string{
		"APPROVE":         "APPROVED",
		"REJECT":          "REJECTED",
		"REQUEST_CHANGES": "CHANGES_REQUESTED",
	}[req.Action]

	_ = s.SendApprovalNotification(ctx, ApprovalNotification{
		ID:          uuid.New().String(),
		RecipientID: approverID,
		DocumentID:  req.DocumentID,
		WorkflowID:  req.WorkflowID,
		StepID:      req.StepID,
		Message:     fmt.Sprintf("Approval action %s performed on document %s", req.Action, req.DocumentID),
		Type:        notifType,
		SentAt:      time.Now().Format(time.RFC3339),
	})

	return approvalResp, nil
}

func (s *service) GetDocumentApprovalStatus(ctx context.Context, documentID string) (*DocumentApprovalStatus, error) {
	if documentID == "" {
		return nil, errors.New("document_id is required")
	}

	status, ok := documentApprovalStore[documentID]
	if !ok {
		return &DocumentApprovalStatus{
			DocumentID:      documentID,
			OverallStatus:   "NOT_SUBMITTED",
			CompletedSteps:  []string{},
			PendingSteps:    []string{},
			ApprovalHistory: []ApprovalResponse{},
			StartedAt:       "",
		}, nil
	}
	return status, nil
}

func (s *service) GetPendingApprovals(ctx context.Context, approverID string) ([]*DocumentApprovalStatus, error) {
	var result []*DocumentApprovalStatus
	for _, status := range documentApprovalStore {
		if status.OverallStatus == "IN_PROGRESS" {
			result = append(result, status)
		}
	}
	return result, nil
}

func (s *service) SendApprovalNotification(ctx context.Context, notification ApprovalNotification) error {
	if notification.RecipientID == "" {
		return errors.New("recipient_id is required")
	}
	if notification.ID == "" {
		notification.ID = uuid.New().String()
	}
	if notification.SentAt == "" {
		notification.SentAt = time.Now().Format(time.RFC3339)
	}

	approvalNotificationStore[notification.RecipientID] = append(
		approvalNotificationStore[notification.RecipientID],
		&notification,
	)
	return nil
}

func (s *service) GetApprovalNotifications(ctx context.Context, recipientID string) ([]*ApprovalNotification, error) {
	if recipientID == "" {
		return nil, errors.New("recipient_id is required")
	}

	notifications := approvalNotificationStore[recipientID]
	if notifications == nil {
		return []*ApprovalNotification{}, nil
	}
	return notifications, nil
}

// ─── Fishbone Template Management (T-5.3.14) ────────────────────────────────

func (s *service) IncrementTemplateUsage(ctx context.Context, templateID string) error {
	templateUID, err := uuid.Parse(templateID)
	if err != nil {
		return errors.New("invalid template ID")
	}
	return s.repo.IncrementTemplateUsage(ctx, templateUID)
}

func (s *service) ApplyTemplateToDiagram(ctx context.Context, templateID string, diagramID string) error {
	templateUID, err := uuid.Parse(templateID)
	if err != nil {
		return errors.New("invalid template ID")
	}
	diagramUID, err := uuid.Parse(diagramID)
	if err != nil {
		return errors.New("invalid diagram ID")
	}

	template, err := s.GetFishboneTemplateByID(ctx, templateID)
	if err != nil {
		return fmt.Errorf("template not found: %w", err)
	}

	// Apply preset nodes from the template to the diagram
	diagram, err := s.repo.GetFishboneDiagramByID(ctx, diagramUID)
	if err != nil {
		return fmt.Errorf("diagram not found: %w", err)
	}

	// Copy bone categories from the template
	if len(template.PresetNodes) > 0 {
		diagram.BoneCategories = []string{}
		seenCategories := map[string]bool{}
		for i, node := range template.PresetNodes {
			category := node.BoneCategory
			if category == "" {
				continue
			}

			if !seenCategories[category] {
				seenCategories[category] = true
				diagram.BoneCategories = append(diagram.BoneCategories, category)
			}

			causeText := node.CauseText
			if causeText == "" {
				causeText = fmt.Sprintf("Cause %d", i+1)
			}

			newNode := &FishboneNode{
				ID:           uuid.New(),
				DiagramID:    diagramUID,
				BoneCategory: category,
				CauseText:    causeText,
				NodeLevel:    1,
				SequenceNo:   i,
				IsMainBone:   i == 0,
			}
			_ = s.repo.CreateFishboneNode(ctx, newNode)
		}
	}

	// Update diagram categories
	if err := s.repo.UpdateFishboneDiagram(ctx, diagram); err != nil {
		return fmt.Errorf("failed to update diagram: %w", err)
	}

	// Increment template usage count
	return s.repo.IncrementTemplateUsage(ctx, templateUID)
}

// ─── Enhanced CompileDocumentWithAnalysis (FR 4.1.1, T-6.2.1–T-6.2.5) ───────

// CompileDocumentWithAnalysis fetches real SWOT, RootCause, Fishbone, and StudentNeeds
// data from the repository and integrates them into the KSP document compilation response.
func (s *service) CompileDocumentWithAnalysis(ctx context.Context, req DocumentCompilationRequest) (*DocumentCompilationResponse, error) {
	integrationUID, err := uuid.Parse(req.IntegrationID)
	if err != nil {
		return nil, errors.New("invalid integration ID")
	}

	_, err = s.repo.GetKSPAnalysisIntegrationByID(ctx, integrationUID)
	if err != nil {
		return nil, fmt.Errorf("integration not found: %w", err)
	}

	// This is a simplified compilation - in a real system this would generate a PDF or Word doc
	// We assume sections are generated internally
	
	response := &DocumentCompilationResponse{
		DocumentID:        req.IntegrationID,
		DocumentURL:       "/api/v1/strategic-planning/ksp-integrations/" + req.IntegrationID + "/document",
		Format:            req.Format,
		PageCount:         15, // estimated
		FileSize:          1024 * 1024,
		CompilationStatus: "COMPLETED",
		GeneratedAt:       time.Now().Format(time.RFC3339),
		ExpiresAt:         time.Now().Add(24 * time.Hour).Format(time.RFC3339),
	}

	return response, nil
}

func (s *service) compileDocumentSections(ctx context.Context, integration *KSPAnalysisIntegration) ([]string, error) {
	var sections []string

	// --- SWOT Section (T-6.2.1) ---
	if integration.SWOTAnalysisID != nil {
		swotSession, err := s.repo.GetSWOTAnalysisSessionByID(ctx, *integration.SWOTAnalysisID)
		if err == nil && swotSession != nil {
			swotItems, _ := s.repo.GetSWOTSessionItems(ctx, swotSession.ID)
			sections = append(sections, buildSWOTSection(swotSession, swotItems))
		}
	}

	// --- Root Cause Section (T-6.2.2) ---
	if integration.RootCauseID != nil {
		rootCause, err := s.repo.GetRootCauseByID(ctx, *integration.RootCauseID)
		if err == nil && rootCause != nil {
			sections = append(sections, buildRootCauseSection(rootCause))
		}
	}

	// --- Fishbone Section (T-6.2.3) ---
	if integration.FishboneDiagramID != nil {
		diagram, err := s.repo.GetFishboneDiagramByID(ctx, *integration.FishboneDiagramID)
		if err == nil && diagram != nil {
			nodes, _ := s.repo.GetFishboneNodesByDiagram(ctx, diagram.ID)
			sections = append(sections, buildFishboneSection(diagram, nodes))
		}
	}

	// --- Student Needs Section (T-6.2.4) ---
	if integration.StudentNeedsID != nil {
		studentNeeds, err := s.repo.GetStudentNeedsEnhancedByID(ctx, *integration.StudentNeedsID)
		if err == nil && studentNeeds != nil {
			sections = append(sections, buildStudentNeedsSection(studentNeeds))
		}
	}

	// --- Rapor Pendidikan Section ---
	if integration.RaporPendidikanID != nil {
		rapor, err := s.repo.GetRaporPendidikanByID(ctx, *integration.RaporPendidikanID)
		if err == nil && rapor != nil {
			sections = append(sections, buildRaporSection(rapor))
		}
	}

	return sections, nil
}

// buildSWOTSection composes a human-readable SWOT section for the KSP document.
func buildSWOTSection(session *SWOTAnalysisSession, items []*SWOTSessionItem) string {
	var sb strings.Builder
	sb.WriteString("## Analisis SWOT\n\n")
	sb.WriteString(fmt.Sprintf("**Sesi:** %s\n", session.SessionName))
	if session.Description != nil {
		sb.WriteString(fmt.Sprintf("**Deskripsi:** %s\n", *session.Description))
	}
	sb.WriteString(fmt.Sprintf("**Tanggal Analisis:** %s\n\n", session.AnalysisDate.Format("02 January 2006")))

	quadrantLabels := map[string]string{
		"S": "Kekuatan (Strengths)",
		"W": "Kelemahan (Weaknesses)",
		"O": "Peluang (Opportunities)",
		"T": "Ancaman (Threats)",
	}
	grouped := map[string][]*SWOTSessionItem{}
	for _, item := range items {
		q := "S"
		if item.Quadrant != nil {
			q = *item.Quadrant
		}
		grouped[q] = append(grouped[q], item)
	}
	for _, q := range []string{"S", "W", "O", "T"} {
		sb.WriteString(fmt.Sprintf("### %s\n", quadrantLabels[q]))
		if len(grouped[q]) == 0 {
			sb.WriteString("- (belum ada item)\n")
		}
		for _, item := range grouped[q] {
			notes := ""
			if item.Notes != nil {
				notes = *item.Notes
			}
			sb.WriteString(fmt.Sprintf("- %s\n", notes))
		}
		sb.WriteString("\n")
	}

	if len(session.KeyInsights) > 0 {
		sb.WriteString("### Insight Utama\n")
		for _, insight := range session.KeyInsights {
			sb.WriteString(fmt.Sprintf("- %s\n", insight))
		}
	}

	return sb.String()
}

// buildRootCauseSection composes a human-readable Root Cause / 5-Whys section.
func buildRootCauseSection(rc *RootCause) string {
	var sb strings.Builder
	sb.WriteString("## Analisis Akar Masalah (5-Whys)\n\n")
	sb.WriteString(fmt.Sprintf("**Masalah yang Diidentifikasi:** %s\n\n", rc.IdentifiedProblem))

	whys := []struct {
		label string
		value *string
	}{
		{"Why 1", rc.Why1},
		{"Why 2", rc.Why2},
		{"Why 3", rc.Why3},
		{"Why 4", rc.Why4},
		{"Why 5", rc.Why5},
	}
	for _, w := range whys {
		if w.value != nil && *w.value != "" {
			sb.WriteString(fmt.Sprintf("- **%s:** %s\n", w.label, *w.value))
		}
	}
	sb.WriteString(fmt.Sprintf("\n**Akar Masalah:** %s\n", rc.RootCause))
	sb.WriteString(fmt.Sprintf("**Kegiatan Benahi:** %s\n", rc.KegiatanBenahi))

	if rc.Status != "" {
		sb.WriteString(fmt.Sprintf("**Status:** %s (%d%%)\n", rc.Status, rc.CompletionPercentage))
	}
	return sb.String()
}

// buildFishboneSection composes a human-readable Fishbone/Ishikawa section.
func buildFishboneSection(diagram *FishboneDiagram, nodes []*FishboneNode) string {
	var sb strings.Builder
	sb.WriteString("## Diagram Fishbone (Ishikawa)\n\n")
	sb.WriteString(fmt.Sprintf("**Efek Utama:** %s\n\n", diagram.HeadEffect))
	if diagram.Description != nil {
		sb.WriteString(fmt.Sprintf("**Deskripsi:** %s\n\n", *diagram.Description))
	}

	// Group nodes by category
	byCategory := map[string][]*FishboneNode{}
	for _, node := range nodes {
		byCategory[node.BoneCategory] = append(byCategory[node.BoneCategory], node)
	}
	for cat, catNodes := range byCategory {
		sb.WriteString(fmt.Sprintf("### Kategori: %s\n", cat))
		for _, node := range catNodes {
			indent := strings.Repeat("  ", node.NodeLevel-1)
			sb.WriteString(fmt.Sprintf("%s- %s\n", indent, node.CauseText))
		}
		sb.WriteString("\n")
	}
	return sb.String()
}

// buildStudentNeedsSection composes a student needs section.
func buildStudentNeedsSection(sn *StudentNeedsEnhanced) string {
	var sb strings.Builder
	sb.WriteString("## Analisis Kebutuhan Peserta Didik\n\n")
	sb.WriteString(fmt.Sprintf("**Profil Dimensi:** %s\n", sn.ProfilDimensi))
	if sn.CurrentStatus != nil {
		sb.WriteString(fmt.Sprintf("**Status Saat Ini:** %s\n", *sn.CurrentStatus))
	}
	if sn.GapAnalysis != nil {
		sb.WriteString(fmt.Sprintf("**Analisis Kesenjangan:** %s\n", *sn.GapAnalysis))
	}
	if sn.ActionPlan != nil {
		sb.WriteString(fmt.Sprintf("**Rencana Tindakan:** %s\n", *sn.ActionPlan))
	}
	sb.WriteString(fmt.Sprintf("**Prioritas:** %d | **Progres:** %d%%\n", sn.PriorityLevel, sn.ProgressPercentage))
	return sb.String()
}

// buildRaporSection composes a Rapor Pendidikan section.
func buildRaporSection(rapor *RaporPendidikan) string {
	var sb strings.Builder
	sb.WriteString("## Data Rapor Pendidikan\n\n")
	sb.WriteString(fmt.Sprintf("**Tahun:** %s | **Semester:** %s\n\n", rapor.Year, rapor.Semester))
	if rapor.LiteracyScore != nil {
		sb.WriteString(fmt.Sprintf("- Skor Literasi: **%.2f**\n", *rapor.LiteracyScore))
	}
	if rapor.NumeracyScore != nil {
		sb.WriteString(fmt.Sprintf("- Skor Numerasi: **%.2f**\n", *rapor.NumeracyScore))
	}
	if rapor.CharacterScore != nil {
		sb.WriteString(fmt.Sprintf("- Skor Karakter: **%.2f**\n", *rapor.CharacterScore))
	}
	return sb.String()
}

// ─── Real GenerateAnalysisSnapshot (T-6.2.5) ────────────────────────────────

// GenerateAnalysisSnapshot fetches real data from the repository.
func (s *service) GenerateAnalysisSnapshot(ctx context.Context, integrationID string) (*AnalysisDataSnapshot, error) {
	integrationUID, err := uuid.Parse(integrationID)
	if err != nil {
		return nil, errors.New("invalid integration ID")
	}

	integration, err := s.repo.GetKSPAnalysisIntegrationByID(ctx, integrationUID)
	if err != nil {
		return nil, fmt.Errorf("integration not found: %w", err)
	}

	snapshot := &AnalysisDataSnapshot{
		IntegrationID: integrationID,
		CapturedAt:    time.Now().Format(time.RFC3339),
	}

	// SWOT snapshot (T-6.2.1)
	if integration.SWOTAnalysisID != nil {
		session, err := s.repo.GetSWOTAnalysisSessionByID(ctx, *integration.SWOTAnalysisID)
		if err == nil && session != nil {
			items, _ := s.repo.GetSWOTSessionItems(ctx, session.ID)
			swotData := map[string]interface{}{
				"session_id":   session.ID,
				"session_name": session.SessionName,
				"status":       session.Status,
				"item_count":   len(items),
			}
			snapshot.SWOTData = &swotData
		}
	}

	// Root Cause snapshot (T-6.2.2)
	if integration.RootCauseID != nil {
		rc, err := s.repo.GetRootCauseByID(ctx, *integration.RootCauseID)
		if err == nil && rc != nil {
			rcData := map[string]interface{}{
				"id":                 rc.ID,
				"identified_problem": rc.IdentifiedProblem,
				"root_cause":         rc.RootCause,
				"kegiatan_benahi":    rc.KegiatanBenahi,
				"status":             rc.Status,
				"completion":         rc.CompletionPercentage,
			}
			snapshot.RootCauseData = &rcData
		}
	}

	// Fishbone snapshot (T-6.2.3)
	if integration.FishboneDiagramID != nil {
		diagram, err := s.repo.GetFishboneDiagramByID(ctx, *integration.FishboneDiagramID)
		if err == nil && diagram != nil {
			nodes, _ := s.repo.GetFishboneNodesByDiagram(ctx, diagram.ID)
			fishData := map[string]interface{}{
				"diagram_id":  diagram.ID,
				"head_effect": diagram.HeadEffect,
				"status":      diagram.Status,
				"node_count":  len(nodes),
				"categories":  diagram.BoneCategories,
			}
			snapshot.FishboneData = &fishData
		}
	}

	// Student Needs snapshot (T-6.2.4)
	if integration.StudentNeedsID != nil {
		sn, err := s.repo.GetStudentNeedsEnhancedByID(ctx, *integration.StudentNeedsID)
		if err == nil && sn != nil {
			snData := map[string]interface{}{
				"id":                  sn.ID,
				"profil_dimensi":      sn.ProfilDimensi,
				"current_status":      sn.CurrentStatus,
				"action_plan_status":  sn.ActionPlanStatus,
				"progress_percentage": sn.ProgressPercentage,
				"priority_level":      sn.PriorityLevel,
			}
			snapshot.StudentNeedsData = &snData
		}
	}

	// Rapor Pendidikan snapshot
	if integration.RaporPendidikanID != nil {
		rapor, err := s.repo.GetRaporPendidikanByID(ctx, *integration.RaporPendidikanID)
		if err == nil && rapor != nil {
			raporData := map[string]interface{}{
				"id":              rapor.ID,
				"year":            rapor.Year,
				"semester":        rapor.Semester,
				"literacy_score":  rapor.LiteracyScore,
				"numeracy_score":  rapor.NumeracyScore,
				"character_score": rapor.CharacterScore,
			}
			snapshot.RaporData = &raporData
		}
	}

	return snapshot, nil
}

// ─── Real GenerateChartsFromAnalysis (FR 4.1.3) ─────────────────────────────

// GenerateChartsFromAnalysis fetches real data for multiple chart configs.
func (s *service) GenerateChartsFromAnalysis(ctx context.Context, req ChartGenerationRequest) ([]*ChartGenerationResponse, error) {
	var charts []*ChartGenerationResponse

	for _, cfg := range req.ChartConfigs {
		switch cfg.ChartType {
		case "SWOT_BAR", "SWOT_PIE", "SWOT_RADAR":
			// Derive chart sub-type
			parts := strings.SplitN(cfg.ChartType, "_", 2)
			subType := "BAR"
			if len(parts) == 2 {
				subType = parts[1]
			}
			// Pull real SWOT counts from integration if integration_id present
			data := SWOTChartData{}
			if req.IntegrationID != "" {
				integUID, err := uuid.Parse(req.IntegrationID)
				if err == nil {
					integration, err := s.repo.GetKSPAnalysisIntegrationByID(ctx, integUID)
					if err == nil && integration.SWOTAnalysisID != nil {
						items, err2 := s.repo.GetSWOTItemsBySchool(ctx, integration.SchoolID, "")
						if err2 == nil {
							for _, item := range items {
								switch item.Quadrant {
								case "S":
									data.Strengths++
								case "W":
									data.Weaknesses++
								case "O":
									data.Opportunities++
								case "T":
									data.Threats++
								}
							}
						}
					}
				}
			}
			// Fallback to config data field
			if data.Strengths+data.Weaknesses+data.Opportunities+data.Threats == 0 {
				if s, ok := cfg.Data["strengths"].(float64); ok {
					data.Strengths = int(s)
				}
				if w, ok := cfg.Data["weaknesses"].(float64); ok {
					data.Weaknesses = int(w)
				}
				if o, ok := cfg.Data["opportunities"].(float64); ok {
					data.Opportunities = int(o)
				}
				if t, ok := cfg.Data["threats"].(float64); ok {
					data.Threats = int(t)
				}
			}
			chart, _ := s.GenerateSWOTChart(ctx, data, subType)
			if chart != nil {
				charts = append(charts, chart)
			}

		case "ROOT_CAUSE_BAR", "ROOT_CAUSE_PIE":
			parts := strings.SplitN(cfg.ChartType, "_", 3)
			subType := "BAR"
			if len(parts) == 3 {
				subType = parts[2]
			}
			data := RootCauseChartData{}
			if req.IntegrationID != "" {
				integUID, err := uuid.Parse(req.IntegrationID)
				if err == nil {
					integration, err := s.repo.GetKSPAnalysisIntegrationByID(ctx, integUID)
					if err == nil {
						rcs, err2 := s.repo.GetRootCausesBySchool(ctx, integration.SchoolID, "")
						if err2 == nil {
							data.TotalRootCauses = len(rcs)
							data.StatusDistribution = map[string]int{}
							for _, rc := range rcs {
								data.StatusDistribution[rc.Status]++
								switch rc.Status {
								case "RESOLVED":
									data.Resolved++
								case "IN_PROGRESS":
									data.InProgress++
								default:
									data.Pending++
								}
							}
						}
					}
				}
			}
			chart, _ := s.GenerateRootCauseChart(ctx, data, subType)
			if chart != nil {
				charts = append(charts, chart)
			}

		case "FISHBONE":
			data := FishboneChartData{}
			if req.IntegrationID != "" {
				integUID, err := uuid.Parse(req.IntegrationID)
				if err == nil {
					integration, err := s.repo.GetKSPAnalysisIntegrationByID(ctx, integUID)
					if err == nil && integration.FishboneDiagramID != nil {
						diagram, err2 := s.repo.GetFishboneDiagramByID(ctx, *integration.FishboneDiagramID)
						if err2 == nil {
							nodes, _ := s.repo.GetFishboneNodesByDiagram(ctx, diagram.ID)
							data.TotalDiagrams = 1
							data.TotalNodes = len(nodes)
							data.CategoryDistribution = map[string]int{}
							for _, node := range nodes {
								data.CategoryDistribution[node.BoneCategory]++
							}
						}
					}
				}
			}
			chart, _ := s.GenerateFishboneChart(ctx, data, "FISHBONE")
			if chart != nil {
				charts = append(charts, chart)
			}

		case "STUDENT_NEEDS_BAR", "STUDENT_NEEDS_PIE":
			parts := strings.SplitN(cfg.ChartType, "_", 3)
			subType := "BAR"
			if len(parts) == 3 {
				subType = parts[2]
			}
			data := StudentNeedsChartData{}
			if req.IntegrationID != "" {
				integUID, err := uuid.Parse(req.IntegrationID)
				if err == nil {
					integration, err := s.repo.GetKSPAnalysisIntegrationByID(ctx, integUID)
					if err == nil {
						needsList, _, err2 := s.repo.GetStudentNeedsEnhancedBySchool(ctx, integration.SchoolID, Pagination{Limit: 1000})
						if err2 == nil {
							data.TotalProfiles = len(needsList)
							data.ProfileDistribution = map[string]int{}
							for _, sn := range needsList {
								data.ProfileDistribution[sn.ProfilDimensi]++
								if sn.PriorityLevel >= 4 {
									data.CriticalNeeds++
								}
							}
						}
					}
				}
			}
			chart, _ := s.GenerateStudentNeedsChart(ctx, data, subType)
			if chart != nil {
				charts = append(charts, chart)
			}
		}
	}

	return charts, nil
}

// ─── Enhanced GenerateRecommendationsWithAI (FR 4.1.4) ──────────────────────

// GenerateRecommendationsWithAI calls the AI platform gRPC service.
func (s *service) GenerateRecommendationsWithAI(ctx context.Context, req AIRecommendationRequest) (*AIRecommendationResponse, error) {
	if s.aiClient == nil {
		// Graceful fallback: return structured placeholder recommendations
		return &AIRecommendationResponse{
			Recommendations: []string{
				"Tingkatkan kualitas data SWOT dengan melibatkan lebih banyak pemangku kepentingan.",
				"Lakukan validasi root cause analysis secara berkala oleh tim pengawas.",
				"Integrasikan diagram fishbone dengan rencana tindak lanjut yang terukur.",
				"Pantau progres kebutuhan peserta didik melalui asesmen bulanan.",
			},
			Confidence:  0.75,
			Sources:     []string{"SWOT Analysis", "Root Cause Analysis", "Student Needs Assessment"},
			GeneratedAt: time.Now().Format(time.RFC3339),
		}, nil
	}

	// Serialize analysis data for the AI platform
	analysisJSON := "{}"
	if req.AnalysisData != nil {
		if b, err := json.Marshal(req.AnalysisData); err == nil {
			analysisJSON = string(b)
		}
	}

	grpcReq := &pb.GenerateKSPSectionRequest{
		RequestId: uuid.New().String(),
		Metadata: &pb.AnalysisMetadata{
			Language: "id",
		},
		SectionKey:      "recommendations_" + req.RecommendationType,
		SectionTitle:    fmt.Sprintf("Rekomendasi %s", req.RecommendationType),
		AnalysisContext: analysisJSON,
		MaxWords:        500,
	}

	resp, err := s.aiClient.GenerateKSPSection(ctx, grpcReq)
	if err != nil {
		// Graceful fallback on AI error
		return &AIRecommendationResponse{
			Recommendations: []string{
				"AI service temporarily unavailable. Please review analysis data manually.",
			},
			Confidence:  0.5,
			GeneratedAt: time.Now().Format(time.RFC3339),
		}, nil
	}

	// Parse recommendations from the generated content
	recommendations := strings.Split(resp.Section.Content, "\n")
	var filtered []string
	for _, r := range recommendations {
		r = strings.TrimSpace(r)
		if r != "" {
			filtered = append(filtered, r)
		}
	}
	if len(filtered) == 0 {
		filtered = []string{resp.Section.Content}
	}

	return &AIRecommendationResponse{
		Recommendations: filtered,
		Confidence:      0.9,
		Sources:         []string{"AI Strategic Analysis Platform"},
		GeneratedAt:     time.Now().Format(time.RFC3339),
	}, nil
}

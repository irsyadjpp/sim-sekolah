# File Organization Analysis - Misplaced Files Report

**Date**: 2026-05-30  
**Status**: In Progress - Analyzing misplaced files in monolith

---

## Issues Identified in Intelligence Directory

### Files Outside Folders
- ❌ ai_agents_service.py (outside) vs ai_agents_service/ (folder exists)
- ❌ adaptive_learning_service.py (outside) vs adaptive_learning_engine/ (folder exists)
- ❌ assessment_service.py (outside) vs assessment_engine/ (folder exists)
- ❌ curriculum_service.py (outside) vs curriculum_engine/ (folder exists)
- ❌ educational_intelligence_service.py (outside) vs educational_intelligence_service/ (folder exists)
- ❌ educational_ontology_service.py (outside) vs educational_ontology_service/ (folder exists)
- ❌ learning_graph_service.py (outside) vs learning_graph_engine/ (folder exists)
- ❌ learning_progression_service.py (outside) vs learning_progression_engine/ (folder exists)
- ❌ pedagogy_service.py (outside) vs pedagogy_engine/ (folder exists)
- ❌ recommendation_service.py (outside) vs recommendation_engine/ (folder exists)
- ✅ strategic_analysis_service.py (outside) - no matching folder (OK)

---

## Initial Analysis Results

### File Size Comparison
- ai_agents_service.py: 106 lines vs ai_agents_service/main.py: 2206 lines
- adaptive_learning_service.py: 547 lines vs adaptive_learning_engine/main.py: 668 lines
- assessment_service.py: 433 lines vs assessment_engine/main.py: 544 lines

### Pattern Analysis
- Files outside folders are **wrapper services** that import from microservice code
- Folders contain **complete microservice implementations** with FastAPI servers
- Outside files appear to be monolith adapters/wrappers

---

## Recommended Actions

### Option 1: Move Outside Files to Matching Folders
- Pros: Keeps everything together
- Cons: May cause naming conflicts (_service vs _engine)

### Option 2: Rename Folders to Match Files
- pros: More consistent naming
- Cons: May break imports and require renaming

### Option 3: Delete Outside Files (They are Wrappers)
- pros: Cleaner structure
- Cons: May break existing imports

### Option 4: Keep Current Structure (It's Intentional)
- The outside files might be monolith wrappers
- The folders contain microservice implementations
- This could be intentional for monolith architecture

---

## Next Steps
1. Analyze which approach is correct based on import dependencies
2. Check if other directories have similar issues
3. Implement the proper solution
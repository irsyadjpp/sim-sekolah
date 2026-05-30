from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnalysisMetadata(_message.Message):
    __slots__ = ("school_id", "academic_year", "language", "provider", "model", "extra")
    class ExtraEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SCHOOL_ID_FIELD_NUMBER: _ClassVar[int]
    ACADEMIC_YEAR_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    school_id: str
    academic_year: str
    language: str
    provider: str
    model: str
    extra: _containers.ScalarMap[str, str]
    def __init__(self, school_id: _Optional[str] = ..., academic_year: _Optional[str] = ..., language: _Optional[str] = ..., provider: _Optional[str] = ..., model: _Optional[str] = ..., extra: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SWOTItem(_message.Message):
    __slots__ = ("id", "quadrant", "content", "category", "priority", "data_source")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUADRANT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    quadrant: str
    content: str
    category: str
    priority: float
    data_source: str
    def __init__(self, id: _Optional[str] = ..., quadrant: _Optional[str] = ..., content: _Optional[str] = ..., category: _Optional[str] = ..., priority: _Optional[float] = ..., data_source: _Optional[str] = ...) -> None: ...

class AnalyzeSWOTRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "existing_items", "data_sources", "school_context", "include_recommendations")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    EXISTING_ITEMS_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    SCHOOL_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_RECOMMENDATIONS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    existing_items: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    data_sources: _containers.RepeatedScalarFieldContainer[str]
    school_context: str
    include_recommendations: bool
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., existing_items: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., data_sources: _Optional[_Iterable[str]] = ..., school_context: _Optional[str] = ..., include_recommendations: _Optional[bool] = ...) -> None: ...

class SWOTAnalysisResult(_message.Message):
    __slots__ = ("strengths", "weaknesses", "opportunities", "threats", "so_strategies", "wo_strategies", "st_strategies", "wt_strategies", "summary", "analysis_confidence")
    STRENGTHS_FIELD_NUMBER: _ClassVar[int]
    WEAKNESSES_FIELD_NUMBER: _ClassVar[int]
    OPPORTUNITIES_FIELD_NUMBER: _ClassVar[int]
    THREATS_FIELD_NUMBER: _ClassVar[int]
    SO_STRATEGIES_FIELD_NUMBER: _ClassVar[int]
    WO_STRATEGIES_FIELD_NUMBER: _ClassVar[int]
    ST_STRATEGIES_FIELD_NUMBER: _ClassVar[int]
    WT_STRATEGIES_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    strengths: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    weaknesses: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    opportunities: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    threats: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    so_strategies: _containers.RepeatedScalarFieldContainer[str]
    wo_strategies: _containers.RepeatedScalarFieldContainer[str]
    st_strategies: _containers.RepeatedScalarFieldContainer[str]
    wt_strategies: _containers.RepeatedScalarFieldContainer[str]
    summary: str
    analysis_confidence: float
    def __init__(self, strengths: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., weaknesses: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., opportunities: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., threats: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., so_strategies: _Optional[_Iterable[str]] = ..., wo_strategies: _Optional[_Iterable[str]] = ..., st_strategies: _Optional[_Iterable[str]] = ..., wt_strategies: _Optional[_Iterable[str]] = ..., summary: _Optional[str] = ..., analysis_confidence: _Optional[float] = ...) -> None: ...

class AnalyzeSWOTResponse(_message.Message):
    __slots__ = ("success", "message", "result", "tokens_used", "latency_ms")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_USED_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    result: SWOTAnalysisResult
    tokens_used: int
    latency_ms: float
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., result: _Optional[_Union[SWOTAnalysisResult, _Mapping]] = ..., tokens_used: _Optional[int] = ..., latency_ms: _Optional[float] = ...) -> None: ...

class SuggestSWOTItemsRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "quadrant", "context", "max_suggestions")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    QUADRANT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    MAX_SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    quadrant: str
    context: str
    max_suggestions: int
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., quadrant: _Optional[str] = ..., context: _Optional[str] = ..., max_suggestions: _Optional[int] = ...) -> None: ...

class SuggestSWOTItemsResponse(_message.Message):
    __slots__ = ("success", "message", "suggestions")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    suggestions: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., suggestions: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ...) -> None: ...

class RootCauseData(_message.Message):
    __slots__ = ("id", "problem", "description", "category", "priority", "existing_causes")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    EXISTING_CAUSES_FIELD_NUMBER: _ClassVar[int]
    id: str
    problem: str
    description: str
    category: str
    priority: str
    existing_causes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., problem: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[str] = ..., priority: _Optional[str] = ..., existing_causes: _Optional[_Iterable[str]] = ...) -> None: ...

class AnalyzeRootCauseRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "root_cause", "school_context", "include_solutions")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ROOT_CAUSE_FIELD_NUMBER: _ClassVar[int]
    SCHOOL_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SOLUTIONS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    root_cause: RootCauseData
    school_context: str
    include_solutions: bool
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., root_cause: _Optional[_Union[RootCauseData, _Mapping]] = ..., school_context: _Optional[str] = ..., include_solutions: _Optional[bool] = ...) -> None: ...

class RootCauseFinding(_message.Message):
    __slots__ = ("layer", "cause", "explanation", "confidence", "evidence")
    LAYER_FIELD_NUMBER: _ClassVar[int]
    CAUSE_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    EVIDENCE_FIELD_NUMBER: _ClassVar[int]
    layer: str
    cause: str
    explanation: str
    confidence: float
    evidence: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, layer: _Optional[str] = ..., cause: _Optional[str] = ..., explanation: _Optional[str] = ..., confidence: _Optional[float] = ..., evidence: _Optional[_Iterable[str]] = ...) -> None: ...

class RootCauseAnalysisResult(_message.Message):
    __slots__ = ("findings", "recommendations", "intervention_steps", "summary", "analysis_confidence")
    FINDINGS_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDATIONS_FIELD_NUMBER: _ClassVar[int]
    INTERVENTION_STEPS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    findings: _containers.RepeatedCompositeFieldContainer[RootCauseFinding]
    recommendations: _containers.RepeatedScalarFieldContainer[str]
    intervention_steps: _containers.RepeatedScalarFieldContainer[str]
    summary: str
    analysis_confidence: float
    def __init__(self, findings: _Optional[_Iterable[_Union[RootCauseFinding, _Mapping]]] = ..., recommendations: _Optional[_Iterable[str]] = ..., intervention_steps: _Optional[_Iterable[str]] = ..., summary: _Optional[str] = ..., analysis_confidence: _Optional[float] = ...) -> None: ...

class AnalyzeRootCauseResponse(_message.Message):
    __slots__ = ("success", "message", "result", "tokens_used", "latency_ms")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_USED_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    result: RootCauseAnalysisResult
    tokens_used: int
    latency_ms: float
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., result: _Optional[_Union[RootCauseAnalysisResult, _Mapping]] = ..., tokens_used: _Optional[int] = ..., latency_ms: _Optional[float] = ...) -> None: ...

class GenerateFiveWhysRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "problem_statement", "context", "num_whys")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_STATEMENT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    NUM_WHYS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    problem_statement: str
    context: str
    num_whys: int
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., problem_statement: _Optional[str] = ..., context: _Optional[str] = ..., num_whys: _Optional[int] = ...) -> None: ...

class WhyLevel(_message.Message):
    __slots__ = ("level", "question", "answer", "rationale")
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    RATIONALE_FIELD_NUMBER: _ClassVar[int]
    level: int
    question: str
    answer: str
    rationale: str
    def __init__(self, level: _Optional[int] = ..., question: _Optional[str] = ..., answer: _Optional[str] = ..., rationale: _Optional[str] = ...) -> None: ...

class GenerateFiveWhysResponse(_message.Message):
    __slots__ = ("success", "message", "why_chain", "root_cause_conclusion", "corrective_actions")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WHY_CHAIN_FIELD_NUMBER: _ClassVar[int]
    ROOT_CAUSE_CONCLUSION_FIELD_NUMBER: _ClassVar[int]
    CORRECTIVE_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    why_chain: _containers.RepeatedCompositeFieldContainer[WhyLevel]
    root_cause_conclusion: str
    corrective_actions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., why_chain: _Optional[_Iterable[_Union[WhyLevel, _Mapping]]] = ..., root_cause_conclusion: _Optional[str] = ..., corrective_actions: _Optional[_Iterable[str]] = ...) -> None: ...

class FishboneNode(_message.Message):
    __slots__ = ("id", "label", "category", "parent_id", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    label: str
    category: str
    parent_id: str
    description: str
    def __init__(self, id: _Optional[str] = ..., label: _Optional[str] = ..., category: _Optional[str] = ..., parent_id: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class AnalyzeFishboneRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "problem_statement", "existing_nodes", "context")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_STATEMENT_FIELD_NUMBER: _ClassVar[int]
    EXISTING_NODES_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    problem_statement: str
    existing_nodes: _containers.RepeatedCompositeFieldContainer[FishboneNode]
    context: str
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., problem_statement: _Optional[str] = ..., existing_nodes: _Optional[_Iterable[_Union[FishboneNode, _Mapping]]] = ..., context: _Optional[str] = ...) -> None: ...

class FishboneSuggestion(_message.Message):
    __slots__ = ("category", "cause", "explanation", "relevance")
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CAUSE_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_FIELD_NUMBER: _ClassVar[int]
    RELEVANCE_FIELD_NUMBER: _ClassVar[int]
    category: str
    cause: str
    explanation: str
    relevance: float
    def __init__(self, category: _Optional[str] = ..., cause: _Optional[str] = ..., explanation: _Optional[str] = ..., relevance: _Optional[float] = ...) -> None: ...

class AnalyzeFishboneResult(_message.Message):
    __slots__ = ("suggestions", "priority_causes", "structured_summary", "completeness_score")
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_CAUSES_FIELD_NUMBER: _ClassVar[int]
    STRUCTURED_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    COMPLETENESS_SCORE_FIELD_NUMBER: _ClassVar[int]
    suggestions: _containers.RepeatedCompositeFieldContainer[FishboneSuggestion]
    priority_causes: _containers.RepeatedScalarFieldContainer[str]
    structured_summary: str
    completeness_score: float
    def __init__(self, suggestions: _Optional[_Iterable[_Union[FishboneSuggestion, _Mapping]]] = ..., priority_causes: _Optional[_Iterable[str]] = ..., structured_summary: _Optional[str] = ..., completeness_score: _Optional[float] = ...) -> None: ...

class AnalyzeFishboneResponse(_message.Message):
    __slots__ = ("success", "message", "result", "tokens_used", "latency_ms")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_USED_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    result: AnalyzeFishboneResult
    tokens_used: int
    latency_ms: float
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., result: _Optional[_Union[AnalyzeFishboneResult, _Mapping]] = ..., tokens_used: _Optional[int] = ..., latency_ms: _Optional[float] = ...) -> None: ...

class SuggestFishboneCategoriesRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "problem_statement", "max_per_category")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_STATEMENT_FIELD_NUMBER: _ClassVar[int]
    MAX_PER_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    problem_statement: str
    max_per_category: int
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., problem_statement: _Optional[str] = ..., max_per_category: _Optional[int] = ...) -> None: ...

class CategorySuggestions(_message.Message):
    __slots__ = ("category", "suggestions")
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    category: str
    suggestions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, category: _Optional[str] = ..., suggestions: _Optional[_Iterable[str]] = ...) -> None: ...

class SuggestFishboneCategoriesResponse(_message.Message):
    __slots__ = ("success", "message", "categories")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    categories: _containers.RepeatedCompositeFieldContainer[CategorySuggestions]
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., categories: _Optional[_Iterable[_Union[CategorySuggestions, _Mapping]]] = ...) -> None: ...

class SWOTDataInput(_message.Message):
    __slots__ = ("strengths", "weaknesses", "opportunities", "threats", "summary")
    STRENGTHS_FIELD_NUMBER: _ClassVar[int]
    WEAKNESSES_FIELD_NUMBER: _ClassVar[int]
    OPPORTUNITIES_FIELD_NUMBER: _ClassVar[int]
    THREATS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    strengths: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    weaknesses: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    opportunities: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    threats: _containers.RepeatedCompositeFieldContainer[SWOTItem]
    summary: str
    def __init__(self, strengths: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., weaknesses: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., opportunities: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., threats: _Optional[_Iterable[_Union[SWOTItem, _Mapping]]] = ..., summary: _Optional[str] = ...) -> None: ...

class RootCauseDataInput(_message.Message):
    __slots__ = ("problem", "findings", "recommendations")
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    FINDINGS_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDATIONS_FIELD_NUMBER: _ClassVar[int]
    problem: str
    findings: _containers.RepeatedCompositeFieldContainer[RootCauseFinding]
    recommendations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, problem: _Optional[str] = ..., findings: _Optional[_Iterable[_Union[RootCauseFinding, _Mapping]]] = ..., recommendations: _Optional[_Iterable[str]] = ...) -> None: ...

class FishboneDataInput(_message.Message):
    __slots__ = ("problem", "causes", "structured_summary")
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    CAUSES_FIELD_NUMBER: _ClassVar[int]
    STRUCTURED_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    problem: str
    causes: _containers.RepeatedCompositeFieldContainer[FishboneSuggestion]
    structured_summary: str
    def __init__(self, problem: _Optional[str] = ..., causes: _Optional[_Iterable[_Union[FishboneSuggestion, _Mapping]]] = ..., structured_summary: _Optional[str] = ...) -> None: ...

class StudentNeedsDataInput(_message.Message):
    __slots__ = ("identified_needs", "profile_dimension", "context")
    IDENTIFIED_NEEDS_FIELD_NUMBER: _ClassVar[int]
    PROFILE_DIMENSION_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    identified_needs: _containers.RepeatedScalarFieldContainer[str]
    profile_dimension: str
    context: str
    def __init__(self, identified_needs: _Optional[_Iterable[str]] = ..., profile_dimension: _Optional[str] = ..., context: _Optional[str] = ...) -> None: ...

class GenerateKSPContentRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "school_name", "academic_year", "swot_data", "root_cause_data", "fishbone_data", "student_needs_data", "sections_to_generate", "tone")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SCHOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    ACADEMIC_YEAR_FIELD_NUMBER: _ClassVar[int]
    SWOT_DATA_FIELD_NUMBER: _ClassVar[int]
    ROOT_CAUSE_DATA_FIELD_NUMBER: _ClassVar[int]
    FISHBONE_DATA_FIELD_NUMBER: _ClassVar[int]
    STUDENT_NEEDS_DATA_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_TO_GENERATE_FIELD_NUMBER: _ClassVar[int]
    TONE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    school_name: str
    academic_year: str
    swot_data: SWOTDataInput
    root_cause_data: RootCauseDataInput
    fishbone_data: FishboneDataInput
    student_needs_data: StudentNeedsDataInput
    sections_to_generate: _containers.RepeatedScalarFieldContainer[str]
    tone: str
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., school_name: _Optional[str] = ..., academic_year: _Optional[str] = ..., swot_data: _Optional[_Union[SWOTDataInput, _Mapping]] = ..., root_cause_data: _Optional[_Union[RootCauseDataInput, _Mapping]] = ..., fishbone_data: _Optional[_Union[FishboneDataInput, _Mapping]] = ..., student_needs_data: _Optional[_Union[StudentNeedsDataInput, _Mapping]] = ..., sections_to_generate: _Optional[_Iterable[str]] = ..., tone: _Optional[str] = ...) -> None: ...

class KSPSection(_message.Message):
    __slots__ = ("section_key", "section_title", "content", "sub_sections")
    SECTION_KEY_FIELD_NUMBER: _ClassVar[int]
    SECTION_TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SUB_SECTIONS_FIELD_NUMBER: _ClassVar[int]
    section_key: str
    section_title: str
    content: str
    sub_sections: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, section_key: _Optional[str] = ..., section_title: _Optional[str] = ..., content: _Optional[str] = ..., sub_sections: _Optional[_Iterable[str]] = ...) -> None: ...

class GenerateKSPContentResponse(_message.Message):
    __slots__ = ("success", "message", "sections", "executive_summary", "tokens_used", "latency_ms")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    EXECUTIVE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TOKENS_USED_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    sections: _containers.RepeatedCompositeFieldContainer[KSPSection]
    executive_summary: str
    tokens_used: int
    latency_ms: float
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., sections: _Optional[_Iterable[_Union[KSPSection, _Mapping]]] = ..., executive_summary: _Optional[str] = ..., tokens_used: _Optional[int] = ..., latency_ms: _Optional[float] = ...) -> None: ...

class GenerateKSPSectionRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "section_key", "section_title", "analysis_context", "school_context", "max_words")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SECTION_KEY_FIELD_NUMBER: _ClassVar[int]
    SECTION_TITLE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    SCHOOL_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    MAX_WORDS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    section_key: str
    section_title: str
    analysis_context: str
    school_context: str
    max_words: int
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., section_key: _Optional[str] = ..., section_title: _Optional[str] = ..., analysis_context: _Optional[str] = ..., school_context: _Optional[str] = ..., max_words: _Optional[int] = ...) -> None: ...

class GenerateKSPSectionResponse(_message.Message):
    __slots__ = ("success", "message", "section", "tokens_used")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SECTION_FIELD_NUMBER: _ClassVar[int]
    TOKENS_USED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    section: KSPSection
    tokens_used: int
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., section: _Optional[_Union[KSPSection, _Mapping]] = ..., tokens_used: _Optional[int] = ...) -> None: ...

class IntegrateAnalysisDataRequest(_message.Message):
    __slots__ = ("request_id", "metadata", "swot_data", "root_cause_data", "fishbone_data", "student_needs", "integration_purpose")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SWOT_DATA_FIELD_NUMBER: _ClassVar[int]
    ROOT_CAUSE_DATA_FIELD_NUMBER: _ClassVar[int]
    FISHBONE_DATA_FIELD_NUMBER: _ClassVar[int]
    STUDENT_NEEDS_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_PURPOSE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    metadata: AnalysisMetadata
    swot_data: SWOTDataInput
    root_cause_data: RootCauseDataInput
    fishbone_data: FishboneDataInput
    student_needs: StudentNeedsDataInput
    integration_purpose: str
    def __init__(self, request_id: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisMetadata, _Mapping]] = ..., swot_data: _Optional[_Union[SWOTDataInput, _Mapping]] = ..., root_cause_data: _Optional[_Union[RootCauseDataInput, _Mapping]] = ..., fishbone_data: _Optional[_Union[FishboneDataInput, _Mapping]] = ..., student_needs: _Optional[_Union[StudentNeedsDataInput, _Mapping]] = ..., integration_purpose: _Optional[str] = ...) -> None: ...

class IntegrationInsight(_message.Message):
    __slots__ = ("insight_type", "description", "confidence", "supporting_evidence")
    INSIGHT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTING_EVIDENCE_FIELD_NUMBER: _ClassVar[int]
    insight_type: str
    description: str
    confidence: float
    supporting_evidence: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, insight_type: _Optional[str] = ..., description: _Optional[str] = ..., confidence: _Optional[float] = ..., supporting_evidence: _Optional[_Iterable[str]] = ...) -> None: ...

class IntegrateAnalysisDataResponse(_message.Message):
    __slots__ = ("success", "message", "insights", "priority_actions", "integrated_summary", "tokens_used")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INSIGHTS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TOKENS_USED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    insights: _containers.RepeatedCompositeFieldContainer[IntegrationInsight]
    priority_actions: _containers.RepeatedScalarFieldContainer[str]
    integrated_summary: str
    tokens_used: int
    def __init__(self, success: _Optional[bool] = ..., message: _Optional[str] = ..., insights: _Optional[_Iterable[_Union[IntegrationInsight, _Mapping]]] = ..., priority_actions: _Optional[_Iterable[str]] = ..., integrated_summary: _Optional[str] = ..., tokens_used: _Optional[int] = ...) -> None: ...

class HealthCheckRequest(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: str
    def __init__(self, service: _Optional[str] = ...) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("healthy", "status", "version", "components")
    class ComponentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    healthy: bool
    status: str
    version: str
    components: _containers.ScalarMap[str, str]
    def __init__(self, healthy: _Optional[bool] = ..., status: _Optional[str] = ..., version: _Optional[str] = ..., components: _Optional[_Mapping[str, str]] = ...) -> None: ...

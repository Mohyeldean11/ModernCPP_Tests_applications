# Unified ASPICE Requirements Analyzer

## Overview

The **Unified ASPICE Requirements Analyzer** is a comprehensive Python application designed to evaluate software and system requirements against the **ASPICE (Automotive Software Process Improvement and Capability dEtermination)** standard. This tool supports both **SYS.2** (System Requirements) and **SWE.1** (Software Requirements) analysis processes.

### Key Features

- **Dual-Mode Analysis**: Supports both SYS.2 and SWE.1 requirement analysis types
- **Intelligent Hybrid Approach**: Combines rule-based analysis (30%) with LLM-powered assessment (70%)
- **Comprehensive Structural Analysis**: Evaluates organizational structure, grouping, and classification of requirements
- **Multi-Sheet Excel Output**: Generates detailed reports across 6 specialized worksheets
- **Quality Checklist Assessment**: 5-point quality evaluation framework
- **Smart Recommendations Engine**: Provides actionable improvement suggestions
- **Robust Error Handling**: Automatic encoding detection for CSV files
- **Interactive Menu System**: User-friendly configuration and input handling

---

## Core Concepts

### ASPICE Framework

**ASPICE** is an international standard (ISO/IEC 33004) for automotive software process assessment. It defines capability levels and best practices for software and systems engineering.

#### Base Practices (BPs)

The analyzer focuses on **4 Base Practices** for each analysis type:

**SYS.2 - System Requirements Base Practices:**
1. **BP1**: Specify system requirements
   - Focus: Clear, verifiable, complete requirement specification
   - Key Attributes: ID, Text, Object_Type, ASIL

2. **BP2**: Structure and prioritize system requirements
   - Focus: Logical organization, unique identification, prioritization
   - Key Attributes: ASIL, Object_Type, Group_Structure

3. **BP3**: Analyze system requirements
   - Focus: Correctness, completeness, technical feasibility, verification planning
   - Key Attributes: Verification_Strategy, Verification_Criteria, Review_Status

4. **BP4**: Analyze impact on system context
   - Focus: Interface impacts, operating environment, system elements
   - Key Attributes: Text, Verification_Criteria, ASIL, System_Feature

**SWE.1 - Software Requirements Base Practices:**
1. **BP1**: Specify software requirements
   - Focus: Software requirement specification quality and completeness
   - Key Attributes: ID, Text, Object_Type

2. **BP2**: Structure software requirements
   - Focus: Logical grouping, prioritization, proper identification
   - Key Attributes: ID, Object_Type, ASIL

3. **BP3**: Analyze software requirements
   - Focus: Correctness, feasibility, interdependencies, project management support
   - Key Attributes: Verification_Strategy, Verification_Criteria, Text

4. **BP4**: Analyze impact on operating environment
   - Focus: Operating environment constraints, implementation feasibility
   - Key Attributes: Text, Verification_Criteria

### Quality Checklist (5-Point Framework)

Each requirement is evaluated against 5 quality attributes:

1. **Complete**: Does it fully describe the functionality?
   - Indicators: Presence of modal verbs (shall, must, will), sufficient detail
   - Minimum length: 20 characters

2. **Correct**: Does it accurately describe the functionality?
   - Avoids: Ambiguous words (appropriate, suitable, adequate)
   - Avoids: Contradictory statements
   - Checks: Consistency of terminology

3. **Feasible**: Can the requirement be implemented?
   - Avoids: Impossible words (impossible, cannot, never, instantaneous)
   - Avoids: Unrealistic phrases (zero defects, perfect, always work)
   - Ensures: Realistic expectations

4. **Verifiable**: Can the system be tested to confirm it meets the requirement?
   - Requires: Defined verification strategy
   - Requires: Measurable criteria (values, time, counts, levels)
   - Supported by: Verification_Criteria and Verification_Strategy attributes

5. **Atomic**: Is it a single, indivisible requirement?
   - Single function: Only one primary action
   - No compound conditions: Limited conjunctions (and, or)
   - Structured: 1-3 sentences maximum

---

## Architecture & Components

### 1. Data Models (Dataclasses)

#### `StructuralAnalysis`
Captures file-level analysis results:
```python
@dataclass
class StructuralAnalysis:
    has_groups: bool                      # Whether requirements are grouped
    group_count: int                      # Number of detected groups
    groups_detected: List[str]            # Names of detected groups
    functional_requirements: int          # Count of functional requirements
    non_functional_requirements: int      # Count of non-functional requirements
    undefined_type_requirements: int      # Count of unclassified requirements
    total_requirements: int               # Total requirements in file
    functional_coverage: float            # Coverage ratio (0-1)
    structural_completeness_score: float  # Overall structural quality (0-1)
    atomic_requirements_ratio: float      # Percentage of atomic requirements
```

#### `RequirementAnalysis`
Captures individual requirement analysis results:
```python
@dataclass
class RequirementAnalysis:
    requirement_id: str                    # Unique requirement identifier
    is_compliant: bool                     # Overall ASPICE compliance status
    overall_confidence: float              # Confidence percentage (0-100)
    bp_scores: Dict[str, float]            # Base practice scores (BP1-BP4)
    violated_practices: List[str]          # List of failed base practices
    recommendations: List[str]             # Improvement suggestions
    missing_attributes: List[str]          # Missing mandatory attributes
    structural_impact: Dict[str, str]      # Impact on file structure
    quality_checklist: Dict[str, bool]     # Quality assessment results
    is_atomic: bool                        # Whether requirement is atomic
```

### 2. Main Analysis Class: `UnifiedASPICEChecker`

The core class handling all analysis operations.

**Key Methods:**

#### `analyze_file_structure(df: pd.DataFrame) -> StructuralAnalysis`
Performs comprehensive structural analysis:
- **Group Detection**: Identifies logical grouping patterns in requirements
- **Functional Classification**: Categorizes requirements as functional/non-functional
- **Atomic Analysis**: Measures percentage of atomic requirements
- **Coverage Calculation**: Evaluates classification completeness

Algorithm:
1. Scans requirement text and Object_Type fields
2. Uses keyword matching for functional/non-functional classification
3. Analyzes sentence structure for atomicity
4. Calculates composite structural completeness score

#### `assess_requirement_quality(row: pd.Series) -> Dict[str, bool]`
Evaluates the 5-point quality checklist:
- **Complete Check**: Verifies presence of modal verbs and sufficient detail
- **Correct Check**: Scans for ambiguous/contradictory language
- **Feasible Check**: Detects unrealistic or impossible requirements
- **Verifiable Check**: Confirms verification strategy and measurable criteria
- **Atomic Check**: Analyzes requirement complexity and sentence structure

#### `check_bp_compliance(bp_id: str, row: pd.Series, ...) -> float`
Rule-based compliance scoring for specific base practices:
- Separate implementations for SYS.2 (`_check_sys2_bp_compliance`) and SWE.1 (`_check_swe1_bp_compliance`)
- Scoring based on presence and quality of mandatory attributes
- Returns score 0-100

**Example - SYS.2 BP1 Scoring:**
```
Base: 30 points
+ ID exists and valid: 20 points
+ Text length > 5 chars: 30 points
+ Object_Type defined: 20 points
= Max 100 points
```

#### `build_enhanced_prompt(row: pd.Series, missing_attrs: List[str]) -> str`
Constructs LLM prompt for AI-powered analysis:
- Includes requirement data and context
- Provides base practice definitions
- Specifies LLM assessment focus areas
- Requests JSON-formatted response
- Hints at file-level context and missing data

#### `call_llm(prompt: str) -> str`
Sends prompt to local LLM (Ollama) and retrieves response:
- Uses Ollama API endpoint (default: http://98.86.11.72:11434)
- Model: Mistral 7B (configurable)
- Timeout: 120 seconds
- Falls back gracefully if LLM unavailable

#### `analyze_requirement(row: pd.Series, structural_analysis: StructuralAnalysis) -> RequirementAnalysis`
Main analysis orchestration:

1. **Rule-Based Scoring**: Calculates BP scores using defined rules
2. **LLM Analysis**: Sends enhanced prompt to LLM for validation
3. **LLM Response Parsing**: Extracts structured JSON response
4. **Score Combination**: 
   - Weights: 30% rule-based + 70% LLM-based
   - Formula: `final_score = (rule_score * 0.3) + (llm_score * 0.7)`
5. **Quality Assessment**: Combines rule and LLM quality checklist results
6. **Compliance Determination**: 
   - Requirement is compliant if no BP violations AND confidence ≥ 65%
   - Violation threshold: BP score < 60%
7. **Recommendation Generation**: Creates actionable suggestions
8. **Structural Impact Analysis**: Assesses file-level implications

#### `evaluate_requirements(df: pd.DataFrame) -> Tuple[pd.DataFrame, StructuralAnalysis, List[RequirementAnalysis]]`
Main evaluation pipeline:
1. Performs structural analysis on entire file
2. Iterates through each requirement
3. Calls `analyze_requirement` for each row
4. Compiles results into DataFrame with all analysis columns
5. Returns comprehensive results for export

#### `export_to_excel(...) -> None`
Generates multi-sheet Excel workbook:

**Sheet 1: SYS.2/SWE.1 Analysis (Main)**
- All requirement data with analysis results
- Color-coded compliance status (green/red)
- Quality checklist indicators

**Sheet 2: Summary**
- Overall statistics and metrics
- Compliance rates, confidence levels
- Structural analysis summary

**Sheet 3: BP Analysis**
- Per-practice performance metrics
- Average scores and violation counts
- Focus areas for each practice

**Sheet 4: Structural Analysis**
- Detailed structural metrics
- Group detection results
- Classification coverage analysis

**Sheet 5: Recommendations**
- Top 10 most common improvement suggestions
- Frequency of each recommendation
- Impact percentage

**Sheet 6: Quality Checklist**
- Pass rates for each quality attribute
- Overall quality scoring
- Average quality per requirement

### 3. Utility Functions

#### `load_csv_with_encoding_detection(file_path: str) -> pd.DataFrame`
Robust CSV loading with encoding auto-detection:
- Tries encodings in order: UTF-8, UTF-8-SIG, ISO-8859-1, Windows-1252, Latin1, ASCII
- Falls back to UTF-8 with error replacement if all fail
- Logs encoding information for troubleshooting

#### `validate_csv_structure(df: pd.DataFrame) -> bool`
Validates required columns:
- Checks for required: ID, Text
- Logs available columns for debugging
- Returns False if validation fails

#### `load_analysis_specific_config(base_config_path: str, analysis_type: str) -> Dict[str, Any]`
Loads configuration with type-specific overrides:
- Loads base config from config.json
- Attempts type-specific config: config_sys2.json or config_swe1.json
- Merges configurations with type-specific taking precedence
- Returns complete configuration dictionary

#### `create_example_configs() -> List[str]`
Generates template configuration files:
- **config.json**: Base configuration
- **config_sys2.json**: SYS.2-specific settings
- **config_swe1.json**: SWE.1-specific settings

#### `get_user_input() -> Tuple[str, str]`
Interactive menu for analysis type and input file selection:
- Displays menu for SYS.2 vs SWE.1
- Validates input file existence
- Handles user cancellation gracefully

### 4. Configuration System

**Configuration Files:**

```json
// config.json - Base configuration
{
  "model": "mistral:7b",
  "endpoint": "http://98.86.11.72:11434"
}

// config_sys2.json - SYS.2 specific (overrides base)
{
  "model": "mistral:7b",
  "endpoint": "http://98.86.11.72:11434",
  "output": "sys2_analysis_results.xlsx",
  "type": "SYS2",
  "description": "Configuration for SYS.2 System Requirements Analysis"
}

// config_swe1.json - SWE.1 specific (overrides base)
{
  "model": "mistral:7b",
  "endpoint": "http://98.86.11.72:11434",
  "output": "swe1_analysis_results.xlsx",
  "type": "SWE1",
  "description": "Configuration for SWE.1 Software Requirements Analysis"
}
```

**Configuration Priority:**
1. Command-line arguments (highest priority)
2. Type-specific config file (config_SYS2.json or config_SWE1.json)
3. Base config file (config.json)
4. Built-in defaults

---

## Analysis Workflow

### Step 1: Initialization
```
User runs program
  ↓
Display interactive menu
  ↓
Select analysis type (SYS.2 or SWE.1)
  ↓
Provide input CSV file path
  ↓
Load configuration (type-specific + base)
```

### Step 2: Data Loading
```
Load CSV with encoding detection
  ↓
Validate structure (ID, Text columns)
  ↓
Parse requirements into DataFrame
```

### Step 3: Structural Analysis
```
For entire file:
  - Detect logical groups
  - Classify requirements (functional/non-functional)
  - Analyze atomic decomposition
  - Calculate coverage metrics
  ↓
Result: StructuralAnalysis object
```

### Step 4: Individual Requirement Analysis
```
For each requirement:
  1. Rule-based BP scoring (30% weight)
  2. Build enhanced LLM prompt
  3. Get LLM response (70% weight)
  4. Parse LLM JSON response
  5. Combine scores (weighted average)
  6. Assess quality checklist
  7. Generate recommendations
  8. Analyze structural impact
  ↓
Result: RequirementAnalysis object per requirement
```

### Step 5: Excel Export
```
Create workbook with 6 sheets:
  - Main Analysis
  - Summary Statistics
  - BP Analysis
  - Structural Analysis
  - Recommendations
  - Quality Checklist
  ↓
Apply formatting and styling
  ↓
Save to output file
```

### Step 6: Results Display
```
Print summary statistics to console
Display multi-sheet Excel file location
```

---

## Scoring System

### Base Practice Scoring

**Score Calculation:**
- **Rule-Based**: 0-100 points based on attribute presence and quality
- **LLM-Based**: Maps status categories to scores
  - Compliant: 100
  - Relation-based: 80
  - Partial: 60
  - Non-compliant: 30
  - Unknown: 50

**Final Score Formula:**
```
Final_BP_Score = (Rule_Based_Score × 0.3) + (LLM_Score × 0.7)
Range: 0-100
```

### Overall Compliance Score
```
Overall_Confidence = Average of all 4 BP scores
Range: 0-100

Requirement is COMPLIANT if:
  - No BP violations (all scores ≥ 60%)
  - Overall_Confidence ≥ 65%
```

### Quality Checklist Scoring

Each requirement gets a quality score:
```
Quality_Score = (Number of True attributes) / 3 × 100
Attributes: Feasible, Verifiable, Atomic
Range: 0-100% (0-3 attributes possible)
```

---

## Key Attributes

### Mandatory CSV Columns

**SYS.2 Requirements:**
- `ID`: Unique requirement identifier (e.g., SYS-001)
- `Text`: Requirement description/specification
- `Object_Type`: Classification (functional, non-functional)
- `Object_Status`: Status (new, in review, in progress, accepted, approved, rejected)
- `Verification_Criteria`: How to verify the requirement
- `Verification_Strategy`: Method of verification (test, analysis, inspection, demonstration)
- `System_Feature`: Associated system feature/module
- `ASIL`: Automotive Safety Integrity Level (ASIL A-D)

**SWE.1 Requirements:**
- `ID`: Unique requirement identifier (e.g., SW-001)
- `Text`: Requirement description/specification
- `Object_Type`: Classification (functional, non-functional)
- `Object_Status`: Status (new, in review, in progress, accepted, approved, rejected)
- `Verification_Criteria`: How to verify the requirement
- `Verification_Strategy`: Method of verification (test, analysis, inspection, demonstration)
- `ASIL`: Automotive Safety Integrity Level (ASIL A-D)

---

## Data Flow Diagram

```
CSV Input File
    ↓
Encoding Detection & Validation
    ↓
DataFrame (Pandas)
    ↓
├─→ Structural Analysis Module
│   ├─ Group Detection
│   ├─ Functional Classification
│   ├─ Atomic Analysis
│   └─ Coverage Metrics
│   ↓
│   StructuralAnalysis Object
│
├─→ Per-Requirement Analysis Loop
│   ├─ Rule-Based Scoring
│   ├─ LLM Prompt Generation
│   ├─ LLM API Call
│   ├─ Response Parsing
│   ├─ Score Combination
│   ├─ Quality Assessment
│   ├─ Recommendation Generation
│   └─ Structural Impact Analysis
│   ↓
│   RequirementAnalysis Objects (List)
│
└─→ Excel Export Module
    ├─ Main Analysis Sheet
    ├─ Summary Statistics
    ├─ BP Analysis
    ├─ Structural Analysis
    ├─ Recommendations
    └─ Quality Checklist
    ↓
    Excel Workbook (.xlsx)
```

---

## LLM Integration

### Overview
The analyzer leverages **Mistral 7B** (via Ollama) for intelligent compliance assessment:

### LLM Role (70% of final score)
- Validates rule-based scoring
- Provides expert reasoning on compliance
- Suggests improvements
- Assesses quality checklist attributes
- Returns structured JSON response

### Prompt Structure
1. **Context**: Requirement data and file context
2. **Instructions**: Specific assessment principles
3. **Format Requirements**: JSON response with specific fields
4. **Examples**: Best practices for each base practice

### Error Handling
- If LLM call fails or times out, falls back to 100% rule-based scoring
- Graceful degradation with warning messages
- Analysis continues without LLM contributions

### LLM Payload
```python
{
  "model": "mistral:7b",
  "prompt": "<<enhanced prompt>>",
  "stream": False,
  "timeout": 120
}
```

### Expected Response Format
```json
{
  "BP1": {
    "status": "Compliant|Partial|Non-compliant|Relation-based|Unknown",
    "rationale": "Expert explanation",
    "suggestion": "Improvement recommendation"
  },
  "BP2": { ... },
  "BP3": { ... },
  "BP4": { ... },
  "QUALITY_CHECKLIST": {
    "Complete": true/false,
    "Correct": true/false,
    "Feasible": true/false,
    "Verifiable": true/false,
    "Atomic": true/false
  }
}
```

---

## Usage

### Basic Usage
```bash
python mohz_aspice_final\ 3.py
```
Launches interactive mode where you select analysis type and provide input file.

### With Arguments
```bash
# Run SYS.2 analysis
python "mohz_aspice_final 3.py" --type SYS2 --output sys2_results.xlsx

# Run SWE.1 analysis with custom config
python "mohz_aspice_final 3.py" --type SWE1 -c my_config.json

# Create example config files
python "mohz_aspice_final 3.py" --create-configs

# Custom LLM endpoint
python "mohz_aspice_final 3.py" --endpoint "http://localhost:11434" --model "mistral:latest"
```

### Command-Line Arguments
- `--config`, `-c`: Configuration file path (default: config.json)
- `--output`, `-o`: Output Excel file path
- `--model`: LLM model name (overrides config)
- `--endpoint`: LLM endpoint URL (overrides config)
- `--type`, `-t`: Analysis type (SYS2 or SWE1)
- `--interactive`: Force full interactive mode
- `--create-configs`: Generate example configuration files

---

## Output Files

### Excel Workbook Sheets

1. **Main Analysis Sheet** (SYS.2 or SWE.1)
   - All original requirement data
   - BP1, BP2, BP3, BP4 scores
   - Quality assessment (Is_Feasible, Is_Verifiable, Is_Atomic)
   - ASPICE compliance status
   - Violations and recommendations
   - Missing attributes
   - Color-coded for quick visual assessment

2. **Summary Sheet**
   - Total requirements analyzed
   - Compliance rate and percentage
   - Average confidence level
   - Atomic requirements count
   - Structural metrics (groups, coverage, completeness)

3. **BP Analysis Sheet**
   - Average score per base practice
   - Violation frequency
   - Focus area for each practice

4. **Structural Analysis Sheet**
   - Group detection results
   - Functional/non-functional breakdown
   - Atomic requirements ratio
   - Structural completeness score

5. **Recommendations Sheet**
   - Top 10 most common improvement suggestions
   - Frequency of each recommendation
   - Impact percentage

6. **Quality Checklist Sheet**
   - Pass rate for each quality attribute
   - Overall quality scoring methodology
   - Average quality per requirement

---

## Error Handling

The analyzer implements robust error handling:

### Encoding Issues
- Tries multiple encodings automatically
- Falls back to UTF-8 with error replacement
- Logs which encoding succeeded

### Missing Files
- Validates file existence before processing
- Provides helpful error message with path

### CSV Parsing
- Validates required columns
- Handles empty files gracefully
- Reports parser errors with context

### Invalid Data
- Handles NaN, empty, and TBD values
- Continues processing despite data quality issues
- Reports missing attributes in output

### LLM Failures
- Catches connection timeouts
- Falls back to rule-based scoring
- Logs failures for troubleshooting

---

## Dependencies

- **pandas**: Data manipulation and CSV handling
- **openpyxl**: Excel workbook creation and formatting
- **requests**: HTTP requests to LLM endpoint
- **re**: Regular expression pattern matching
- **json**: JSON parsing and generation
- **dataclasses**: Data structure definitions
- **collections**: Counter for frequency analysis

---

## Performance Considerations

### Timing Estimates
- **Structural Analysis**: < 1 second for most files
- **Per-Requirement Analysis**: 
  - Rule-based: ~ 50ms per requirement
  - LLM analysis: ~ 2-5 seconds per requirement (network dependent)
- **Excel Export**: 1-2 seconds
- **Total**: 2-5 seconds per requirement (depends on LLM availability)

### Memory Usage
- Primarily determined by CSV file size
- DataFrame kept in memory during analysis
- Excel workbook built in memory before writing

### Scalability
- Tested with up to 500+ requirements
- LLM calls are the bottleneck for large files
- Can process incrementally if needed

---

## Future Enhancements

Potential improvements for future versions:
1. **Traceability Matrix**: Map SYS.2 → SWE.1 requirement relationships
2. **Change Tracking**: Monitor requirement changes across versions
3. **Batch Processing**: Analyze multiple files in sequence
4. **Custom Base Practices**: Support for additional ASPICE processes
5. **API Interface**: REST API for integration with other tools
6. **Parallel Processing**: Multi-threaded LLM analysis for speed
7. **Database Storage**: Store results in database for trend analysis
8. **Dashboard**: Web-based visualization of results
9. **Machine Learning**: Learn from previous analyses to improve scoring
10. **Multi-language Support**: Analyze requirements in different languages

---

## Troubleshooting

### LLM Connection Failed
**Problem**: "LLM call failed" messages
**Solution**: 
- Verify Ollama is running: `ollama serve`
- Check endpoint URL in config
- Verify model availability: `ollama list`

### Invalid Encoding
**Problem**: "Unicode encoding issue" error
**Solution**:
- Ensure CSV file is saved as UTF-8
- Try converting file encoding: `iconv -f Windows-1252 -t UTF-8 file.csv > file_utf8.csv`

### Missing Required Columns
**Problem**: "Missing required columns" warning
**Solution**:
- Verify CSV has ID and Text columns
- Check column names match exactly (case-sensitive)
- Export from source tool with all required columns

### Slow Processing
**Problem**: Analysis takes very long
**Solution**:
- Check LLM endpoint is responsive
- Consider using rule-based analysis only (comment out LLM calls)
- Process smaller files first

---

## License

This tool is designed for automotive software compliance analysis in accordance with the ASPICE standard.

---

## Version

**Version**: 3.0 - Final (SYS.2 & SWE.1 Unified)
- Supports both SYS.2 and SWE.1 analysis
- BP1-BP4 focus for both analysis types
- Hybrid rule-based + LLM approach
- Multi-sheet Excel reporting
- Robust error handling and encoding detection

import pandas as pd
from schemas import (
    pipes_schema,
    cctv_schema,
    defects_schema,
    hydraulics_schema
)
from core_validation import (
    validate_by_schema,
    add_issue_with_defectkey
)

def validate_pipes(df_pipes):
    """
    Pipes validation.
    Required: Pipe_ID
    """
    issues = validate_by_schema(df_pipes, pipes_schema, use_defect=False)
    ok = not (issues["level"] == "error").any() if not issues.empty else True
    return df_pipes, issues, ok

def validate_cctv(df_cctv) :
    """
    CCTV validation
    Required: Pipe_ID
    """
    issues = validate_by_schema(df_cctv, cctv_schema, use_defect=False)
    ok = not (issues["level"] == "error").any() if not issues.empty else True
    return df_cctv, issues, ok

def validate_defects(df_defects):
    """
    Defects validation
    Extra checks:
      - Quantification must be S, M or L
    """

    issues_df = validate_by_schema(df_defects, defects_schema, use_defect=True)

    # Convert to list to collect extra issues
    extra_issues = []

    # Additional check: Quantification should be one of S, M or L
    valid_sizes = {"S", "M", "L"}
    if "Quantification" in df_defects.columns:
        mask_invalid_size = (
            ~df_defects["Quantification"].isin(valid_sizes)
            & df_defects["Quantification"].notna()
        )
        for i in df_defects.index[mask_invalid_size]:
            add_issue_with_defectkey(
                extra_issues, df_defects, i, "Quantification",
                "error",
                "⚠️ Quantification must be S, M or L.",
                df_defects.at[i, "Quantification"]
            )

    # Combine the two sets of issues into one DataFrame
    if extra_issues:
        extra_df = pd.DataFrame(extra_issues, columns=["Defect_ID", "column", "level", "message", "value"])
        issues_df = pd.concat([issues_df, extra_df], ignore_index=True)

    ok = not (issues_df["level"] == "error").any() if not issues_df.empty else True
    return df_defects, issues_df, ok

def validate_hydraulics(df_hydraulics):
    """
    Hydraulic properties validation.
    Required: Pipe_ID
    """
    issues = validate_by_schema(
        df_hydraulics,
        hydraulics_schema,
        use_defect=False
    )

    ok = not (issues["level"] == "error").any() if not issues.empty else True

    return df_hydraulics, issues, ok

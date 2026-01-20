import pandas as pd
import numpy as np
from datetime import datetime

# Messages to explain the problems
MSG_NULL     = "The value is null, please review this information"
MSG_NEG      = "The value is negative, please review this information"
MSG_NUMERIC  = "This data is supposed to be numerical; please review this information"
MSG_NOT_INT  = "The value is not an integer number; please review this information"
MSG_DUP_ID   = "Two or more pipes share the same ID"
MSG_NO_UPLOADED = "No information uploaded"

def add_issue_with_compkey(issues, df, idx, col, level, msg, val):
    """Append an issue related to Pipe_ID."""
    pipe_id = df.at[idx, "Pipe_ID"] if idx is not None and "Pipe_ID" in df.columns else None
    issues.append([pipe_id, col, level, msg, val])

def add_issue_with_defectkey(issues, df, idx, col, level, msg, val):
    """Append an issue related to Defect_ID."""
    defect_id = df.at[idx, "Defect_ID"] if idx is not None and "Defect_ID" in df.columns else None
    issues.append([defect_id, col, level, msg, val])

def validate_by_schema(df, schema, use_defect=False):
    """
    Generic schema validator.
    If use_defect=True, Defect_ID will be used instead of Pipe_ID.
    """
    issues = []  # collect issues as a list of lists
    out = df.copy()
    current_year = datetime.now().year

    # ---Select correct issue adder---
    add_issue = add_issue_with_defectkey if use_defect else add_issue_with_compkey

    # ---Missing required columns---
    for col, rules in schema.items():
        if rules.get("required", False) and col not in out.columns:
            add_issue(issues, out, None, col, "error",
                      f"Missing required column '{col}'.", None)

    # ---Per-column checks---
    for col, rules in schema.items():
        if col not in out.columns:
            continue

        series = out[col]

        # ---null/empty---
        if rules.get("null_warning", False):
            null_like = series.isna() | (series.astype("string").str.strip() == "")
            for i in out.index[null_like]:
                add_issue(issues, out, i, col, "warning", MSG_NULL, out.at[i, col])

        # ---numeric---
        if rules.get("numeric", False):
            ser_str = series.astype("string")
            numeric_coerced = pd.to_numeric(ser_str, errors="coerce")
            non_numeric_mask = ser_str.notna() & (ser_str.str.strip() != "") & numeric_coerced.isna()
            for i in out.index[non_numeric_mask]:
                add_issue(issues, out, i, col, "error", MSG_NUMERIC, out.at[i, col])
            series = numeric_coerced

        # ---integer-only---
        if rules.get("integer", False):
            if not pd.api.types.is_numeric_dtype(series):
                series = pd.to_numeric(out[col], errors="coerce")
            int_mask = series.notna() & (np.floor(series) != series)
            for i in out.index[int_mask]:
                add_issue(issues, out, i, col, "error", MSG_NOT_INT, out.at[i, col])

        # ---non-negative---
        if rules.get("non_negative", False):
            if not pd.api.types.is_numeric_dtype(series):
                series = pd.to_numeric(out[col], errors="coerce")
            neg_mask = series.notna() & (series < 0)
            for i in out.index[neg_mask]:
                add_issue(issues, out, i, col, "error", MSG_NEG, out.at[i, col])

        # ---min / max---
        if "min" in rules or "max" in rules:
            if not pd.api.types.is_numeric_dtype(series):
                series = pd.to_numeric(out[col], errors="coerce")
            if "min" in rules:
                min_mask = series.notna() & (series < rules["min"])
                for i in out.index[min_mask]:
                    add_issue(issues, out, i, col, "error",
                              f"Value is below minimum ({rules['min']}).",
                              out.at[i, col])
            if "max" in rules:
                max_mask = series.notna() & (series > rules["max"])
                for i in out.index[max_mask]:
                    add_issue(issues, out, i, col, "error",
                              f"Value exceeds maximum ({rules['max']}).",
                              out.at[i, col])

        # ---year constraints---
        if rules.get("four_digits", False):
            if not pd.api.types.is_numeric_dtype(series):
                series = pd.to_numeric(out[col], errors="coerce")
            bad_mask = series.notna() & ~series.astype("Int64").between(1000, 9999)
            for i in out.index[bad_mask]:
                add_issue(issues, out, i, col, "error",
                          "The year must have four digits; please review this information.",
                          out.at[i, col])

        if rules.get("max_year_current", False):
            if not pd.api.types.is_numeric_dtype(series):
                series = pd.to_numeric(out[col], errors="coerce")
            future_mask = series.notna() & (series > current_year)
            for i in out.index[future_mask]:
                add_issue(issues, out, i, col, "error",
                          f"The installation year is over the expected range of values; please review this information.",
                          out.at[i, col])

        if rules.get("date_format", False):
            date_parsed = pd.to_datetime(out[col], errors="coerce", format="%Y-%m-%d")
            mask_failed = date_parsed.isna() & out[col].notna()
            if mask_failed.any():
                date_parsed.loc[mask_failed] = pd.to_datetime(
                    out.loc[mask_failed, col], errors="coerce", format="%d-%m-%Y"
                )

            invalid_date_mask = date_parsed.isna() & out[col].notna()
            for i in out.index[invalid_date_mask]:
                add_issue(issues, out, i, col, "error",
                          "The installation date does not follow the expected formats (YYYY-MM-DD or DD-MM-YYYY).",
                          out.at[i, col])

        # ---duplicate error---
        if rules.get("duplicate_error", False):
            dup_mask = out[col].notna() & out[col].duplicated(keep=False)
            if dup_mask.any():
                for val, grp in out.loc[dup_mask].groupby(col):
                    for i in grp.index:
                        add_issue(issues, out, i, col, "error",
                                  MSG_DUP_ID if col == "Pipe_ID" else "Duplicate value found.",
                                  val)

    # ---Build DataFrame of issues---
    id_col_name = "Defect_ID" if use_defect else "Pipe_ID"
    issues_df = pd.DataFrame(
        issues,
        columns=[id_col_name, "column", "level", "message", "value"]
    ).sort_values(by=["level", "column", id_col_name],
                  ascending=[True, True, True])

    return issues_df
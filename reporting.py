import pandas as pd
from pathlib import Path
from typing import Tuple

def build_summary(pipes_issues, cctv_issues, defects_issues, hydraulics_issues):
    """Build summary of the results"""
    def counts(df) -> Tuple[int, int]:
        if df is None or df.empty:
            return (0, 0)
        return int((df["level"] == "error").sum()), int((df["level"] == "warning").sum())

    pe, pw = counts(pipes_issues)
    ce, cw = counts(cctv_issues)
    de, dw = counts(defects_issues)
    he, hw = counts(hydraulics_issues)
    summary = pd.DataFrame({
        "Entity": ["PIPES", "CCTV", "DEFECTS", "HYDRAULIC_PROPERTIES"],
        "Errors": [pe, ce, de, he],
        "Warnings": [pw, cw, dw, hw],
    })
    return summary


def safe_to_excel(df, sheet_name, xlw, id_col="Pipe_ID"):
    """Write df to Excel ensuring at least the id_col exists."""
    if df is None or df.empty:
        df = pd.DataFrame(columns=[id_col, "column", "level", "message","value"])
    df.to_excel(xlw, sheet_name=sheet_name, index=False)


def write_report(report_path, summary):
    """Write results"""
    with pd.ExcelWriter(report_path, engine="openpyxl") as xlw:
        summary.to_excel(xlw, sheet_name="SUMMARY", index=False)

# ---Result dialog---

def _open_path_in_os(p: Path, what: str = "file"):
    """
    Best-effort open a file or folder in the OS.
    what: 'file' or 'folder'
    """
    try:
        import os, platform, subprocess
        if what == "folder":
            target = str(p if p.is_dir() else p.parent)
        else:
            target = str(p)

        system = platform.system()
        if system == "Windows":
            os.startfile(target)
        elif system == "Darwin":
            subprocess.run(["open", target], check=False)
        else:
            subprocess.run(["xdg-open", target], check=False)
    except Exception:
        pass


def export_issues(df, name, output_dir):
    """
    Export issues to Excel if small enough, otherwise to CSV.
    Returns the export path and format.
    """
    EXCEL_MAX_ROWS = 1_048_576
    if len(df) < EXCEL_MAX_ROWS:
        path = output_dir / f"{name}.xlsx"
        df.to_excel(path, index=False)
        return path, "excel"
    else:
        path = output_dir / f"{name}.csv"
        df.to_csv(path, index=False)
        return path, "csv"
import pandas as pd
from pathlib import Path
import traceback

from sqlalchemy import create_engine

from validation_entities import (
    validate_pipes,
    validate_cctv,
    validate_defects,
    validate_hydraulics,
)

from reporting import (
    build_summary,
    write_report,
    export_issues,
    _open_path_in_os,
)

from core_validation import MSG_NO_UPLOADED

def load_input_data(
    source_type,
    source_path,
    sheet_names=None
):
    """
    Load input data from either a SQLite database or an Excel file.

    :param source_type: 'database' or 'excel'
    :param source_path: path to database or Excel file
    :param sheet_names: list of sheet names (required for Excel)
    :return: df_pipes, df_cctv, df_defects, df_hydraulics
    """

    df_hydraulics = None

    if source_type == "database":
        engine = create_engine(f"sqlite:///{source_path}")

        df_pipes = pd.read_sql_table("pipe", engine)
        df_cctv = pd.read_sql_table("inspection", engine)
        df_defects = pd.read_sql_table("defect", engine)

        try:
            df_hydraulics = pd.read_sql_table("hydraulic_properties", engine)
        except Exception:
            df_hydraulics = pd.DataFrame()

    elif source_type == "excel":
        if sheet_names is None:
            raise ValueError("sheet_names must be provided when source_type='excel'")

        data = pd.read_excel(source_path, sheet_name=sheet_names)

        df_pipes = data.get("PIPES", pd.DataFrame())
        df_cctv = data.get("CCTV", pd.DataFrame())
        df_defects = data.get("DEFECTS", pd.DataFrame())
        df_hydraulics = data.get("HYDRAULIC_PROPERTIES", pd.DataFrame())

    else:
        raise ValueError("source_type must be 'database' or 'excel'")

    return df_pipes, df_cctv, df_defects, df_hydraulics

def main(
    source_type,
    source_path,
    sheet_names=None,
    output_dir=None,
    auto_open_report=False,
    open_containing_folder=True
):
    """
    Run validation workflow
    """

    try:
        AUTO_OPEN_REPORT = auto_open_report
        OPEN_CONTAINING_FOLDER = open_containing_folder

        # --- load data ---
        df_pipes, df_cctv, df_defects, df_hydraulics = load_input_data(
            source_type=source_type,
            source_path=source_path,
            sheet_names=sheet_names
        )

        # --- output directory ---
        if output_dir is None:
            BASE_DIR = Path().resolve()
            output_dir = BASE_DIR / "Validation_Results"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        # --- validate pipes ---
        if df_pipes.empty:
            pipes_issues = pd.DataFrame(
                [{"Pipe_ID": pd.NA, "column": "pipe", "level": "warning", "message": MSG_NO_UPLOADED}]
            )
        else:
            _, pipes_issues, _ = validate_pipes(df_pipes)

        # --- validate cctv ---
        if df_cctv.empty:
            cctv_issues = pd.DataFrame(
                [{"Pipe_ID": pd.NA, "column": "inspection", "level": "warning", "message": MSG_NO_UPLOADED}]
            )
        else:
            _, cctv_issues, _ = validate_cctv(df_cctv)

        # --- validate defects ---
        if df_defects.empty:
            defects_issues = pd.DataFrame(
                [{"Defect_ID": pd.NA, "column": "defect", "level": "warning", "message": MSG_NO_UPLOADED}]
            )
        else:
            _, defects_issues, _ = validate_defects(df_defects)

        # --- validate hydraulics ---
        if df_hydraulics is None or df_hydraulics.empty:
            hydraulics_issues = pd.DataFrame(
                [{"Pipe_ID": pd.NA, "column": "hydraulic_properties", "level": "warning", "message": MSG_NO_UPLOADED}]
            )
        else:
            _, hydraulics_issues, _ = validate_hydraulics(df_hydraulics)

        # --- summary ---
        summary = build_summary(pipes_issues, cctv_issues, defects_issues, hydraulics_issues)

        report_path = output_dir / "Summary.xlsx"
        write_report(report_path, summary)

        export_issues(pipes_issues, "pipes_issues", output_dir)
        export_issues(cctv_issues, "cctv_issues", output_dir)
        export_issues(defects_issues, "defects_issues", output_dir)
        export_issues(hydraulics_issues, "hydraulics_issues", output_dir)

        print(summary.to_string(index=False))
        print(f"\nA validation report was generated at:\n{report_path}")

        if AUTO_OPEN_REPORT:
            _open_path_in_os(report_path, what="file")
        elif OPEN_CONTAINING_FOLDER:
            _open_path_in_os(report_path, what="folder")

        return df_pipes, df_cctv, df_defects, df_hydraulics, output_dir

    except Exception as e:
        tb = traceback.format_exc(limit=2)
        print("Validation failed:", e)
        print(tb)
        return None, None, None, None, None

if __name__ == "__main__":
    raise ValueError("db_path must be provided when running this script directly")
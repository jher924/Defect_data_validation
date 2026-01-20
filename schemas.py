# src/schemas.py
"""
Validation schemas for database entities.
"""

pipes_schema = {

    "Pipe_ID": {
        "required": True,
        "null_warning": True,
        "duplicate_error": True
    },

    "Manhole_up_ID": {
        "null_warning": True
    },

    "Manhole_down_ID": {
        "null_warning": True
    },

    "Diameter": {
        "numeric": True,
        "integer": True,
        "min": 0,
        "max": 4000,
        "null_warning": True
    },

    "Pipe_length": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Slope": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Depth": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Material": {
        "required": True,
        "null_warning": True
    },

    "UP_invert": {
        "numeric": True,
        "null_warning": True
    },

    "DW_invert": {
        "numeric": True,
        "null_warning": True
    },

    "DEM": {
        "numeric": True,
        "null_warning": True
    },

    "Installation_year": {
        "required": True,
        "numeric": True,
        "integer": True,
        "four_digits": True,
        "max_year_current": True,
        "non_negative": True,
        "null_warning": True
    },

    "GWL": {
        "numeric": True,
        "null_warning": True
    },

    "GWL_from_pipe": {
        "numeric": True,
        "null_warning": True
    },

    "Land_cover_s": {
        "null_warning": True
    },

    "Land_cover_group": {
        "null_warning": True
    },

    "Lan_use_s": {
        "null_warning": True
    },

    "Land_use_group": {
        "null_warning": True
    },

    "Soil_type": {
        "null_warning": True
    },

    "Distance_seawater": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Liq_vul_num": {
        "numeric": True,
        "null_warning": True
    },

    "Traffic_num": {
        "numeric": True,
        "null_warning": True
    },

    "Mean_annual": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Road_num": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Restaurants": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Properties": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Laundries": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Sewage_type": {
        "null_warning": True
    },

    "Sewer_category": {
        "null_warning": True
    },

    "Weather_station_ID": {
        "null_warning": True
    }

}

cctv_schema = {

    "Inspection_ID": {
        "required": True,
        "null_warning": True,
        "duplicate_error": True
    },

    "Pipe_ID": {
        "required": True,
        "null_warning": True
    },

    "Date": {
        "null_warning": True,
        "date_format": True
    },

    "Age_CCTV": {
        "numeric": True,
        "integer": True,
        "non_negative": True,
        "null_warning": True
    },

    "Inspection_direction": {
        "required": True,
        "null_warning": True
    },

    "Inspection_status": {
        "null_warning": True
    },

    "Survey_length": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Condition_rating": {
        "numeric": True,
        "integer": True,
        "min": 0,
        "max": 5,
        "null_warning": True
    },

    "Shape": {
        "null_warning": True
    },

    "Comments": {
        "null_warning": False
    }

}

defects_schema = {

    "Defect_ID": {
        "required": True,
        "null_warning": True,
        "duplicate_error": True
    },

    "Pipe_ID": {
        "required": True,
        "null_warning": True
    },

    "Defect_code": {
        "required": True,
        "null_warning": True
    },

    "Characterization_code": {
        "null_warning": False
    },

    "Quantification": {
        "null_warning": False
    },

    "Defect_length": {
        "numeric": True,
        "non_negative": True,
        "null_warning": False
    },

    "Longitudinal_distance": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Longitudinal_distance_normalized": {
        "numeric": True,
        "min": 0,
        "max": 1,
        "null_warning": True
    },

    "Circumferential_start": {
        "numeric": True,
        "min": 0,
        "max": 12,
        "null_warning": False
    },

    "Circumferential_end": {
        "numeric": True,
        "min": 0,
        "max": 12,
        "null_warning": False
    },

    "Observation_inspection": {
        "null_warning": True
    },

    "Comments": {
        "null_warning": False
    }

}

hydraulics_schema = {

    "Pipe_ID": {
        "required": True,
        "null_warning": True
    },

    "Wet_peak_flow_rate": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Dry_peak_flow_rate": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Wet_peak_velocity": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    },

    "Dry_peak_velocity": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True    },

    "Pipe_capacity": {
        "numeric": True,
        "non_negative": True,
        "null_warning": True
    }

}
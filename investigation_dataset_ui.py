import json
import streamlit as st
from typing import Any, Optional, List
from enum import Enum
from pages.datasets.investigation_dataset_page import (
    DrugTypeOptions,
    BowelPreparationQualityOptions,
    ComfortOptions,
    EndoscopyLocationOptions,
    YesNoOptions,
    InsufflationOptions,
    OutcomeAtTimeOfProcedureOptions,
    LateOutcomeOptions,
    CompletionProofOptions,
    FailureReasonsOptions,
    PolypClassificationOptions,
    PolypAccessOptions,
    PolypInterventionModalityOptions,
    PolypInterventionDeviceOptions,
    PolypInterventionExcisionTechniqueOptions,
    PolypTypeOptions,
    AdenomaSubTypeOptions,
    SerratedLesionSubTypeOptions,
    PolypExcisionCompleteOptions,
    PolypDysplasiaOptions,
    YesNoUncertainOptions,
    ReasonPathologyLostOptions,
    PolypInterventionSuccessOptions,
    PolypReasonLeftInSituOptions,
    AntibioticsAdministeredDrugTypeOptions,
    OtherDrugsAdministeredDrugTypeOptions,
    IVContrastAdministeredOptions,
    TaggingAgentDrugAdministeredOptions,
    AdditionalBowelPrepAdministeredOptions,
    IVBuscopanAdministeredOptions,
    ExaminationQualityOptions,
    ScanPositionOptions,
    ProcedureOutcomeOptions,
    SegmentalInadequacyOptions,
    IntracolonicSummaryCodeOptions,
    ExtracolonicSummaryCodeOptions,
)


# --- Constants ---
enum_import_string = "from pages.datasets.investigation_dataset_page import (\n    "
new_indented_line_string = ",\n    "


# --- Enum mapping ---
ENUM_MAP = {
    "YesNoOptions": YesNoOptions,
    "DrugTypeOptions": DrugTypeOptions,
    "BowelPreparationQualityOptions": BowelPreparationQualityOptions,
    "ComfortOptions": ComfortOptions,
    "EndoscopyLocationOptions": EndoscopyLocationOptions,
    "InsufflationOptions": InsufflationOptions,
    "OutcomeAtTimeOfProcedureOptions": OutcomeAtTimeOfProcedureOptions,
    "LateOutcomeOptions": LateOutcomeOptions,
    "CompletionProofOptions": CompletionProofOptions,
    "FailureReasonsOptions": FailureReasonsOptions,
    "PolypClassificationOptions": PolypClassificationOptions,
    "PolypAccessOptions": PolypAccessOptions,
    "PolypInterventionModalityOptions": PolypInterventionModalityOptions,
    "PolypInterventionDeviceOptions": PolypInterventionDeviceOptions,
    "PolypInterventionExcisionTechniqueOptions": PolypInterventionExcisionTechniqueOptions,
    "PolypTypeOptions": PolypTypeOptions,
    "AdenomaSubTypeOptions": AdenomaSubTypeOptions,
    "SerratedLesionSubTypeOptions": SerratedLesionSubTypeOptions,
    "PolypExcisionCompleteOptions": PolypExcisionCompleteOptions,
    "PolypDysplasiaOptions": PolypDysplasiaOptions,
    "YesNoUncertainOptions": YesNoUncertainOptions,
    "ReasonPathologyLostOptions": ReasonPathologyLostOptions,
    "PolypInterventionSuccessOptions": PolypInterventionSuccessOptions,
    "PolypReasonLeftInSituOptions": PolypReasonLeftInSituOptions,
    "AntibioticsAdministeredDrugTypeOptions": AntibioticsAdministeredDrugTypeOptions,
    "OtherDrugsAdministeredDrugTypeOptions": OtherDrugsAdministeredDrugTypeOptions,
    "IVContrastAdministeredOptions": IVContrastAdministeredOptions,
    "TaggingAgentDrugAdministeredOptions": TaggingAgentDrugAdministeredOptions,
    "AdditionalBowelPrepAdministeredOptions": AdditionalBowelPrepAdministeredOptions,
    "IVBuscopanAdministeredOptions": IVBuscopanAdministeredOptions,
    "ExaminationQualityOptions": ExaminationQualityOptions,
    "ScanPositionOptions": ScanPositionOptions,
    "ProcedureOutcomeOptions": ProcedureOutcomeOptions,
    "SegmentalInadequacyOptions": SegmentalInadequacyOptions,
    "IntracolonicSummaryCodeOptions": IntracolonicSummaryCodeOptions,
    "ExtracolonicSummaryCodeOptions": ExtracolonicSummaryCodeOptions,
}


# --- Utility pretty-print functions ---
def is_python_datetime_expr(val: str) -> bool:
    """
    Returns True if val looks like a Python datetime/timedelta expression.
    Args:
        val (str): The value to check.
    Returns:
        bool: True if val looks like a datetime/timedelta expression, False otherwise.
    """
    if not isinstance(val, str):
        return False
    return (
        val.startswith("datetime.today()")
        or val.startswith("datetime(")
        or "timedelta(" in val
    )


def pretty_dict(d: dict, indent: int = 4) -> str:
    """
    Pretty-print a dictionary with indentation.
    Args:
        d (dict): The dictionary to pretty-print.
        indent (int): The number of spaces to use for indentation.
    Returns:
        str: The pretty-printed dictionary.
    """
    pad = " " * indent
    inner = []
    for k, v in d.items():
        key_str = f'"{k}"' if isinstance(k, str) else str(k)
        if isinstance(v, Enum):
            val = f"{v.__class__.__name__}.{v.name}"
        elif isinstance(v, dict):
            val = pretty_dict(v, indent + 4).replace("\n", "\n" + pad)
        elif isinstance(v, list):
            val = pretty_list(v, indent + 4).replace("\n", "\n" + pad)
        elif isinstance(v, str):
            if is_python_datetime_expr(v):
                val = v
            else:
                val = f'"{v}"'
        else:
            val = str(v)
        inner.append(f"{key_str}: {val}")
    joined = (",\n" + pad).join(inner)
    return "{" + ("\n" + pad + joined + "\n" if inner else "") + "}"


def pretty_list(items: list, indent: int = 4) -> str:
    """
    Pretty-print a list with indentation.
    Args:
        items (list): The list to pretty-print.
        indent (int): The number of spaces to use for indentation.
    Returns:
        str: The pretty-printed list.
    """
    pad = " " * indent
    inner = []
    for x in items:
        if isinstance(x, dict):
            inner.append(pretty_dict(x, indent).replace("\n", "\n" + pad))
        elif isinstance(x, list):
            inner.append(pretty_list(x, indent).replace("\n", "\n" + pad))
        elif isinstance(x, Enum):
            inner.append(f"{x.__class__.__name__}.{x.name}")
        elif isinstance(x, str):
            if is_python_datetime_expr(x):
                inner.append(x)
            else:
                inner.append(f'"{x}"')
        else:
            inner.append(str(x))
    joined = (",\n" + pad).join(inner)
    return "[" + ("\n" + pad + joined + "\n" if inner else "") + "]"


# --- Load JSON field definitions ---
with open("investigation_dataset_ui_app/dataset_fields.json", "r") as f:
    FIELD_DEFS = json.load(f)


# -- Get Enums used in dictionaries ---
def get_enums_used(fields: list) -> set:
    """
    Return a set of Enum class names used in the given fields.
    """
    enums = set()
    for field in fields:
        field_type = field.get("type")
        if field_type in ENUM_MAP:
            enums.add(field_type)
    return enums


# --- Render Helper Functions ---
def _is_condition_met(field: dict, idx: Optional[int | str]) -> bool:
    """
    Check if the condition for a conditional field is met.
    Args:
        field (dict): The field definition.
        idx (int | str, optional): Index for repeated fields (e.g., polyp number).
    Returns:
        bool: True if the condition is met, False otherwise.
    """
    cond = field["conditional_on"]
    cond_field = cond["field"]
    cond_field_key = f"{cond_field}_{idx}" if idx is not None else cond_field
    cond_val = st.session_state.get(cond_field_key)
    if cond_val is None:
        cond_val = st.session_state.get(cond_field)
    expected_val = cond["value"]
    if isinstance(cond_val, Enum):
        cond_val_str = f"{cond_val.__class__.__name__}.{cond_val.name}"
    else:
        cond_val_str = str(cond_val)
    return cond_val_str == expected_val or cond_val == expected_val


def _render_selectbox_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict, options: list
) -> Any:
    """
    Render a selectbox field with given options.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The widget key.
        field (dict): The field definition.
        options (list): The list of options for the selectbox.
    Returns:
        Any: The selected option, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    default = field.get("default", options[0])
    return st.selectbox(
        f"{key} ({desc})", options, index=options.index(default), key=widget_key
    )


# --- Render Fields ---
def render_field(field: dict, idx: Optional[int | str] = None) -> Any:
    """
    Render a single field based on its definition.
    Args:
        field (dict): The field definition.
        idx (int | str, optional): Index for repeated fields (e.g., polyp number).
    Returns:
        The value entered by the user, or None if not applicable.
    """
    key = field["key"]
    desc = field.get("description", "")
    optional = field.get("optional", False)
    field_type = field["type"]
    widget_key = f"{key}_{idx}" if idx is not None else key

    # Handle conditional fields
    if "conditional_on" in field:
        if not _is_condition_met(field, idx):
            return None

    match field_type:
        case "string":
            return render_string_field(key, desc, optional, widget_key, field)
        case "integer":
            return render_integer_field(key, desc, optional, widget_key, field)
        case "integer_or_none":
            return render_integer_or_none_field(key, desc, optional, widget_key, field)
        case "float":
            return render_float_field(key, desc, optional, widget_key, field)
        case "date" | "datetime":
            return render_date_field(key, desc, optional, widget_key, field)
        case t if t in ENUM_MAP:
            return render_enum_field(key, desc, optional, widget_key, field)
        case "bool":
            return render_bool_field(key, desc, optional, widget_key, field)
        case "yes_no":
            return _render_selectbox_field(
                key, desc, optional, widget_key, field, ["yes", "no"]
            )
        case "therapeutic_diagnostic":
            return _render_selectbox_field(
                key, desc, optional, widget_key, field, ["therapeutic", "diagnostic"]
            )
        case "time":
            if not handle_optional(optional, key, desc, widget_key):
                return None
            default = field.get("default", "07:00")
            return st.text_input(
                f"{key} ({desc}) (HH:MM)", value=default, key=widget_key
            )
        case "multiselect":
            return render_multiselect_field(key, desc, optional, widget_key, field)
        case _:
            st.warning(f"Unknown field type: {field_type}")
            return None


def handle_optional(optional: bool, key: str, desc: str, widget_key: str) -> bool:
    """
    Handle optional fields by rendering a checkbox to include/exclude the field.
    Args:
        optional (bool): Whether the field is optional.
        key (str): The field key.
        desc (str): The field description.
        widget_key (str): The unique widget key for Streamlit.
    Returns:
        bool: True if the field should be rendered, False otherwise.
    """
    if optional:
        show = st.checkbox(f"Add {key} ({desc})", key=f"chk_{widget_key}")
        if not show:
            return False
    return True


def render_string_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[str]:
    """
    Render a string field.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[str]: The entered string, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    default = field.get("default", "")
    return st.text_input(f"{key} ({desc})", value=default, key=widget_key)


def render_integer_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[int]:
    """
    Render an integer field.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[int]: The entered integer, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    default = field.get("default", 0)
    val_raw = st.text_input(f"{key} ({desc})", value=str(default), key=widget_key)
    try:
        return int(val_raw)
    except ValueError:
        return None


def render_integer_or_none_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[int]:
    """
    Render an integer field that can also be None (empty).
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[int]: The entered integer, or None if empty or not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    default = field.get("default", None)
    val_raw = st.text_input(
        f"{key} ({desc})",
        value=str(default) if default is not None else "",
        key=widget_key,
    )
    stripped_val = val_raw.strip()
    is_empty = stripped_val == ""
    if is_empty:
        return None
    else:
        return int(stripped_val)


def render_float_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[float]:
    """
    Render a float field.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[float]: The entered float, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    default = field.get("default", 0.0)
    val_raw = st.text_input(f"{key} ({desc})", value=str(default), key=widget_key)
    try:
        return float(val_raw)
    except ValueError:
        return None


def render_date_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[str]:
    """
    Render a date field with quick-select options for Today, Yesterday, or a custom date.
    If a quick-select is chosen, returns a string representing the Python expression (e.g., 'datetime.today()').
    If a custom date is chosen, returns a string 'datetime(year, month, day)'.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[datetime]: The entered date as a datetime, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None

    quick_options = {
        "Custom date": None,
        "Today": "datetime.today()",
        "Yesterday": "datetime.today() - timedelta(days=1)",
        "Tomorrow": "datetime.today() + timedelta(days=1)",
    }

    quick_choice = st.selectbox(
        f"{key} ({desc}) - Quick select",
        list(quick_options.keys()),
        key=f"{widget_key}_quickselect",
    )

    if quick_choice == "Custom date":
        default = field.get("default", None)
        val = st.date_input(f"{key} ({desc})", value=default, key=widget_key)
        if val is not None:
            # Return as Python code string
            return f"datetime({val.year}, {val.month}, {val.day})"
        return None
    else:
        # Return the Python expression string for quick-selects
        return quick_options[quick_choice]


def render_enum_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[Enum]:
    """
    Render an enum field.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[Enum]: The selected enum value, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    enum_class = ENUM_MAP[field["type"]]
    options = list(enum_class)
    default = field.get("default", options[0])
    return st.selectbox(
        f"{key} ({desc})",
        options,
        format_func=lambda x: x.name,
        index=options.index(default),
        key=widget_key,
    )


def render_bool_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[bool]:
    """
    Render a boolean field.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[bool]: The entered boolean value, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    default = field.get("default", False)
    return st.checkbox(f"{key} ({desc})", value=default, key=widget_key)


def render_multiselect_field(
    key: str, desc: str, optional: bool, widget_key: str, field: dict
) -> Optional[List[str]]:
    """
    Render a multiselect field.
    Args:
        key (str): The field key.
        desc (str): The field description.
        optional (bool): Whether the field is optional.
        widget_key (str): The unique widget key for Streamlit.
        field (dict): The field definition.
    Returns:
        Optional[List[str]]: The selected options, or None if not applicable.
    """
    if not handle_optional(optional, key, desc, widget_key):
        return None
    options = field["options"]
    default = field.get("default", [])
    return st.multiselect(f"{key} ({desc})", options, default=default, key=widget_key)


def show_section_with_imports(section_name: str) -> None:
    """
    Render a section with fields and display the corresponding Python code with necessary imports.
    Args:
        section_name (str): The name of the section to show.
    """
    section = FIELD_DEFS[section_name]
    st.header(SECTION_LABELS[section_name])
    result = {}
    for field in section["fields"]:
        val = render_field(field)
        if val is not None:
            result[field["key"]] = val
    enums = get_enums_used(section["fields"])
    if enums:
        import_block = (
            enum_import_string + new_indented_line_string.join(sorted(enums)) + "\n)\n"
        )
    else:
        import_block = ""
    st.code(f"{import_block}{section_name} = {pretty_dict(result)}", language="python")


def show_drug_group_section_with_imports(section_name: str) -> None:
    """
    Render a section with drug groups allowing multiple entries and display the corresponding Python code with necessary imports.
    Args:
        section_name (str): The name of the section to show.
    """
    st.header(SECTION_LABELS[section_name])
    section = FIELD_DEFS[section_name]
    result = {}
    all_fields = []

    if "fields" in section:
        all_fields.extend(section["fields"])
        _render_single_entry_fields(section["fields"], result)

    if "groups" in section:
        for group in section["groups"]:
            all_fields.extend(group["fields"])
            _render_drug_group(section_name, group, result)

    enums = get_enums_used(all_fields)
    if enums:
        import_block = (
            enum_import_string + new_indented_line_string.join(sorted(enums)) + "\n)\n"
        )
    else:
        import_block = ""
    st.code(f"{import_block}{section_name} = {pretty_dict(result)}", language="python")


def _render_single_entry_fields(fields: list, result: dict) -> None:
    """
    Render single-entry fields and update the result dictionary.
    Args:
        fields (list): List of field definitions.
        result (dict): The result dictionary to update.
    """
    for field in fields:
        val = render_field(field)
        if val is not None:
            result[field["key"]] = val


def _render_drug_group(section_name: str, group: dict, result: dict) -> None:
    """
    Render a drug group allowing multiple entries and update the result dictionary.
    Args:
        section_name (str): The name of the section.
        group (dict): The drug group definition.
        result (dict): The result dictionary to update.
    """
    st.subheader(group["label"])
    count = st.number_input(
        f"Number of {group['label'].lower()}",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        key=f"count_{section_name}_{group['label']}",
    )
    fields = group["fields"]
    for i in range(1, count + 1):
        _render_drug_entry(fields, i, result)


def _render_drug_entry(fields: list, index: int, result: dict) -> None:
    """
    Render a single drug entry with type and dose fields side by side.
    Args:
        fields (list): List of field definitions for the drug entry.
        index (int): The index of the drug entry (1-based).
        result (dict): The result dictionary to update.
    """
    col1, col2 = st.columns([2, 1])
    type_field = fields[0].copy()
    dose_field = fields[1].copy()
    type_field["key"] = type_field["key"].replace("X", str(index))
    type_field["optional"] = False
    dose_field["key"] = dose_field["key"].replace("X", str(index))
    dose_field["optional"] = False
    with col1:
        dtype = render_field(type_field)
    with col2:
        ddose = render_field(dose_field)
    if dtype != "" or (isinstance(ddose, str) and ddose.strip() != ""):
        result[type_field["key"]] = dtype
        result[dose_field["key"]] = ddose


def show_polyp_information_and_intervention_and_histology() -> None:
    """
    Show the Polyp Information, Intervention & Histology section, allowing multiple polyps and interventions.
    Each polyp can have multiple interventions and optional histology.
    Also outputs necessary Enum imports.
    """
    st.header(SECTION_LABELS["polyp_information_and_intervention_and_histology"])
    polyp_info_fields = FIELD_DEFS["polyp_information"]["fields"]
    polyp_intervention_fields = FIELD_DEFS["polyp_intervention"]["fields"]
    polyp_histology_fields = FIELD_DEFS["polyp_histology"]["fields"]

    # Collect all fields for import analysis
    all_fields = polyp_info_fields + polyp_intervention_fields + polyp_histology_fields
    enums = get_enums_used(all_fields)
    if enums:
        import_block = (
            enum_import_string + new_indented_line_string.join(sorted(enums)) + "\n)\n"
        )
    else:
        import_block = ""

    num_polyps = st.number_input(
        "Number of polyps", min_value=0, max_value=20, value=1, step=1
    )
    polyp_information = []
    polyp_intervention = []
    polyp_histology = []

    for pi in range(1, num_polyps + 1):
        st.markdown(f"### Polyp {pi}")
        polyp_information.append(_render_polyp_info(polyp_info_fields, pi))
        polyp_intervention.append(_render_interventions(polyp_intervention_fields, pi))
        polyp_histology.append(_render_histology(polyp_histology_fields, pi))

    st.markdown("#### Output")
    st.code(
        f"{import_block}polyp_information = {pretty_list(polyp_information)}",
        language="python",
    )
    st.code(
        f"polyp_intervention = {pretty_list(polyp_intervention)}",
        language="python",
    )
    st.code(
        f"polyp_histology = {pretty_list(polyp_histology)}",
        language="python",
    )


def _render_polyp_info(fields: list, pi: int) -> dict:
    """
    Render polyp information fields for a given polyp index.
    Args:
        fields (list): List of field definitions for polyp information.
        pi (int): The polyp index (1-based).
    Returns:
        dict: The polyp information dictionary.
    """
    polyp_entry = {}
    for field in fields:
        val = render_field(field, idx=pi)
        if val is not None:
            polyp_entry[field["key"]] = val
    return polyp_entry


def _render_interventions(fields: list, pi: int) -> list:
    """
    Render multiple interventions for a given polyp index.
    Args:
        fields (list): List of field definitions for polyp interventions.
        pi (int): The polyp index (1-based).
    Returns:
        list: A list of intervention dictionaries.
    """
    interventions = []
    add_interventions = st.checkbox(
        f"Add interventions for polyp {pi}?", key=f"add_interventions_{pi}"
    )
    if not add_interventions:
        return interventions
    num_int = st.number_input(
        f"Number of interventions for polyp {pi}",
        min_value=0,
        max_value=10,
        value=1,
        step=1,
        key=f"numint_{pi}",
    )
    for ij in range(1, num_int + 1):
        st.markdown(f"**Intervention {ij}**")
        int_dict = {}
        for field in fields:
            val = render_field(field, idx=f"{pi}_{ij}")
            if val is not None:
                int_dict[field["key"]] = val
        interventions.append(int_dict)
    return interventions


def _render_histology(fields: list, pi: int) -> dict:
    """
    Render histology fields for a given polyp index.
    Args:
        fields (list): List of field definitions for polyp histology.
        pi (int): The polyp index (1-based).
    Returns:
        dict: The histology dictionary.
    """
    hist_dict = {}
    add_histology = st.checkbox(
        f"Add histology for polyp {pi}?", key=f"add_histology_{pi}"
    )
    if not add_histology:
        return hist_dict
    for field in fields:
        val = render_field(field, idx=pi)
        if val is not None:
            hist_dict[field["key"]] = val
    return hist_dict


# --- Section names ---
SECTIONS = [
    "general_information",
    "drug_information",
    "endoscopy_information",
    "completion_information",
    "failure_information",
    "polyp_information_and_intervention_and_histology",
    "contrast_tagging_and_drug",
    "tagging_agent_given_drug_information",
    "radiology_information",
    "suspected_findings",
]

SECTION_LABELS = {
    "general_information": "General Information",
    "drug_information": "Drug Information",
    "endoscopy_information": "Endoscopy Information",
    "completion_information": "Completion Information",
    "failure_information": "Failure Information",
    "polyp_information_and_intervention_and_histology": "Polyp Information, Intervention & Histology",
    "contrast_tagging_and_drug": "Contrast Tagging and Drug",
    "tagging_agent_given_drug_information": "Tagging Agent Given Drug Information",
    "radiology_information": "Radiology Information",
    "suspected_findings": "Suspected Findings",
}

# --- Main section selection ---
st.set_page_config(page_title="Investigation Dataset Builder", layout="wide")
st.sidebar.title("Sections")
section = st.sidebar.radio("Jump to", [SECTION_LABELS[s] for s in SECTIONS])

# Render the selected section
SECTION_RENDERERS = {
    "general_information": show_section_with_imports,
    "drug_information": show_drug_group_section_with_imports,
    "endoscopy_information": show_section_with_imports,
    "completion_information": show_section_with_imports,
    "failure_information": show_section_with_imports,
    "polyp_information_and_intervention_and_histology": lambda _: show_polyp_information_and_intervention_and_histology(),  # If you want imports here, update similarly
    "contrast_tagging_and_drug": show_drug_group_section_with_imports,
    "tagging_agent_given_drug_information": show_drug_group_section_with_imports,
    "radiology_information": show_section_with_imports,
    "suspected_findings": show_section_with_imports,
}

selected_key = next(k for k, v in SECTION_LABELS.items() if v == section)
renderer = SECTION_RENDERERS.get(selected_key)
if renderer:
    renderer(selected_key)
else:
    st.warning("Unknown section selected.")

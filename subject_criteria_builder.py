import streamlit as st
from classes.subject_selection_criteria_key import SubjectSelectionCriteriaKey
import json
import os
from dotenv import load_dotenv
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from classes.subject import Subject
from classes.user import User
from classes.user_role_type import UserRoleType
from utils.user_tools import UserTools
import sqlparse
from typing import Optional

# Load environment variables from local.env. Needed for DB connections
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "local.env"))

CRITERIA_JSON_PATH = os.path.join(
    os.path.dirname(__file__), "subject_criteria_builder", "criteria.json"
)
USERS_JSON_PATH = os.path.join(os.path.dirname(__file__), "users.json")


def load_criteria_metadata() -> dict:
    """
    Load criteria metadata from JSON
    Returns:
        dict: The criteria metadata loaded from the JSON file
    """
    with open(CRITERIA_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_users() -> dict:
    """
    Load user data from JSON
    Returns:
        dict: The user data loaded from the JSON file.
    """
    with open(USERS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


CRITERIA_METADATA = load_criteria_metadata()
USERS_DATA = load_users()


def get_metadata_for_key(enum_key: str) -> dict:
    """
    Get metadata for a specific criteria key.
    Args:
        enum_key (str): The key of the criteria to retrieve metadata for.
    Returns:
        dict: The metadata for the specified criteria key, or an empty dictionary if not found.
    """
    for entry in CRITERIA_METADATA:
        if entry["key"] == enum_key:
            return entry
    return {}


def build_criteria() -> dict:
    """
    Build the initial criteria dictionary.
    Returns:
        dict: The initial criteria dictionary.
    """
    return {key.description: "" for key in SubjectSelectionCriteriaKey}


def show_dependency_warnings(dependencies: Optional[list]) -> None:
    """
    Show warnings for dependencies if needed.
    Args:
        dependencies (list): A list of dependency names to check.
    """
    if dependencies:
        for dep in dependencies:
            if dep == "User":
                st.warning(
                    """This key may require a populated User object to work in playwright.

If using only the UI, please select a user from the dropdown below."""
                )
            elif dep == "Subject":
                st.warning(
                    """This key may require a populated Subject object to work in playwright.

If using only the UI, please enter an NHS number in the section below."""
                )


def render_criterion(
    label: str,
    is_expanded: bool,
    allowed_values: Optional[list],
    notes: str,
    user_value: str,
    dependencies: Optional[list] = None,
) -> str:
    """
    Render a single criterion for user input.
    Args:
        label (str): The label for the criterion.
        is_expanded (bool): Whether the criterion is expanded.
        allowed_values (Optional[list]): The list of allowed values for the criterion.
        notes (str): Any notes or descriptions for the criterion.
        user_value (str): The current value set by the user.
        dependencies (Optional[list]): Any dependencies for the criterion.
    Returns:
        str: The user-defined value for the criterion, or an empty string if not set.
    """
    if st.button(
        f"➕ {label}" if not is_expanded else f"✖ {label}",
        key=f"btn-{label}",
    ):
        st.session_state.expanded = set() if is_expanded else {label}
        st.rerun()

    if not is_expanded:
        return user_value

    with st.expander(f"Set value for: {label}", expanded=True):
        if notes:
            st.markdown(f"**Description:** {notes}")

        show_dependency_warnings(dependencies)

        if allowed_values:
            selected = st.selectbox(
                f"Select a value for '{label}'",
                [""] + allowed_values,
                key=f"select-{label}",
            )
            if selected:
                user_value = selected

        user_value = st.text_input(
            f"Or enter a value for '{label}'",
            user_value,
            key=f"input-{label}",
        )
    return user_value


def show_top_buttons() -> None:
    """
    Show the top buttons for the criteria builder.
    These are the 'Reset Criteria Builder' and 'Show/Hide Criteria/Search' buttons
    """
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Reset Criteria Builder"):
            st.session_state.criteria = build_criteria()
            st.session_state.expanded = set()
            st.session_state.selected_user = None
            st.rerun()
    with col2:
        if "hide_criteria" not in st.session_state:
            st.session_state.hide_criteria = False
        if st.session_state.hide_criteria:
            if st.button("👁️ Show Criteria/Search"):
                st.session_state.hide_criteria = False
                st.rerun()
        else:
            if st.button("🙈 Hide Criteria/Search"):
                st.session_state.hide_criteria = True
                st.rerun()


def get_filtered_keys(search_term: str) -> list:
    """
    Get a list of keys that match the search term.
    Args:
        search_term (str): What the user is searching
    Returns:
        list: A list of all criteria matching the user's search
    """
    return [
        key
        for key in SubjectSelectionCriteriaKey
        if search_term.lower() in key.description.lower()
    ]


def check_user_dependency(filtered_keys: list) -> bool:
    """
    Check if any of the filtered keys have a user dependency.
    Args:
        filtered_keys (list): The list of filtered keys to check.
    Returns:
        bool: True if any filtered key has a user dependency, False otherwise.
    """
    for key in filtered_keys:
        label = key.description
        enum_key = key.name
        metadata = get_metadata_for_key(enum_key)
        dependencies = metadata.get("dependencies", None)
        if dependencies and "User" in dependencies and st.session_state.criteria[label]:
            return True
    return False


def show_user_selection() -> User:
    """
    Show the user selection dropdown.
    Returns:
        User: The selected user object.
    Raises:
        ValueError: If user details are missing or invalid.
    """
    st.markdown("### User Selection (Required for selected criteria)")
    user_names = [k for k in USERS_DATA.keys() if not k.startswith("_")]
    user_display_names = [
        f"{name} ({USERS_DATA[name]['username']})" for name in user_names
    ]
    default_index = 0
    if st.session_state.selected_user and st.session_state.selected_user in user_names:
        default_index = user_names.index(st.session_state.selected_user)
    selected = st.selectbox(
        "Select a user:",
        user_display_names,
        index=default_index if user_names else 0,
        key="user_select",
    )
    user = User()
    if selected:
        selected_user_name = selected.split(" (")[0]
        st.session_state.selected_user = selected_user_name
        user_details = USERS_DATA[selected_user_name]
        st.markdown(f"**User:** {selected_user_name}")
        st.markdown(f"**Username:** {user_details['username']}")
        try:
            user_details_obj = UserTools.retrieve_user(selected_user_name)
            org_code = user_details_obj.get("org_code")
            user_code = user_details_obj.get("username")
            role_id = user_details_obj.get("role_id")
            if org_code is None or user_code is None or role_id is None:
                raise ValueError(
                    "Missing required user details (org_code, username, or role_id)"
                )
            user_role = UserRoleType(
                org_code=org_code, user_code=user_code, role_id=role_id
            )
            user = User.from_user_role_type(user_role)
        except Exception as e:
            st.error(f"Could not build user object: {e}")
    return user


def show_criteria(filtered_keys: list) -> None:
    """
    Show the criteria for the selected keys.
    Args:
        filtered_keys (list): The list of filtered keys to show criteria for.
    """
    for key in filtered_keys:
        label = key.description
        enum_key = key.name
        is_expanded = label in st.session_state.expanded
        metadata = get_metadata_for_key(enum_key)
        notes = metadata.get("notes", "")
        allowed_values = metadata.get("allowed_values", None)
        dependencies = metadata.get("dependencies", None)
        user_value = st.session_state.criteria[label]
        updated_value = render_criterion(
            label, is_expanded, allowed_values, notes, user_value, dependencies
        )
        st.session_state.criteria[label] = updated_value


def show_final_criteria(final_criteria: dict) -> None:
    """
    Show the final criteria dictionary.
    Args:
        final_criteria (dict): The final criteria dictionary to show.
    """
    st.subheader("Final Criteria Dictionary")
    st.code(json.dumps(final_criteria, indent=2), language="json")


def check_subject_dependency(filtered_keys: list) -> bool:
    """
    Check if any of the filtered keys have a subject dependency.
    Args:
        filtered_keys (list): The list of filtered keys to check.
    Returns:
        bool: True if any filtered key has a subject dependency, False otherwise.
    """
    for key in filtered_keys:
        label = key.description
        enum_key = key.name
        metadata = get_metadata_for_key(enum_key)
        dependencies = metadata.get("dependencies", None)
        if (
            dependencies
            and "Subject" in dependencies
            and st.session_state.criteria[label]
        ):
            return True
    return False


def show_subject_input() -> str:
    """
    Show an input for the user to enter a Subject's NHS number.
    Returns:
        str: The entered NHS number.
    """
    st.markdown("### Subject NHS Number (Required for selected criteria)")
    nhs_number = st.text_input("Enter Subject's NHS Number", key="subject_nhs_number")
    return nhs_number


def get_or_init_session_state() -> None:
    """
    Initialize the session state variables if they don't exist.
    """
    if "criteria" not in st.session_state:
        st.session_state.criteria = build_criteria()
    if "expanded" not in st.session_state:
        st.session_state.expanded = set()
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = None
    if "hide_criteria" not in st.session_state:
        st.session_state.hide_criteria = False
    if "subject_nhs_number" not in st.session_state:
        st.session_state.subject_nhs_number = ""


def get_search_and_filtered_keys() -> list:
    """
    Get the filtered keys based on the current session state.
    Returns:
        list: A list containing the the filtered keys.
    """
    if not st.session_state.get("hide_criteria", False):
        search_term = st.text_input("🔍 Search criteria:", "", key="search_term")
        filtered_keys = get_filtered_keys(search_term)
        st.write(
            f"Showing {len(filtered_keys)} of {len(SubjectSelectionCriteriaKey)} criteria"
        )
    else:
        search_term = ""
        filtered_keys = []
    return filtered_keys


def get_user_if_needed(user_dependency_needed: bool) -> User:
    """
    Get the user object if a user dependency is needed.
    Args:
        user_dependency_needed (bool): Whether a user dependency is needed.
    Returns:
        User: The populated user object if a user dependency is needed, otherwise a default User object.
    """
    user = User()
    if user_dependency_needed:
        user = show_user_selection()
    return user


def get_subject_if_needed(subject_dependency_needed: bool) -> Subject:
    """
    Get the subject object if a subject dependency is needed.
    Args:
        subject_dependency_needed (bool): Whether a subject dependency is needed.
    Returns:
        Subject: The populated subject object if a subject dependency is needed, otherwise a default Subject object.
    """
    nhs_number = ""
    subject = Subject()
    if subject_dependency_needed:
        nhs_number = show_subject_input()
        if nhs_number:
            try:
                subject = Subject().populate_subject_object_from_nhs_no(nhs_number)
            except Exception as e:
                st.error(f"Could not populate subject object: {e}")
    return subject


def show_sql_and_binds(final_criteria: dict, user: User, subject: Subject) -> None:
    """
    Show the SQL query and bind variables for the final criteria.
    Args:
        final_criteria (dict): The final criteria dictionary.
        user (User): The user object.
        subject (Subject): The subject object.
    """
    try:
        (
            query,
            bind_vars,
        ) = SubjectSelectionQueryBuilder().build_subject_selection_query(
            final_criteria, user, subject, 1
        )
        formatted_query = sqlparse.format(query, reindent=True, keyword_case="upper")
        st.subheader("Generated SQL Query")
        st.code(formatted_query, language="sql")
        if any(k.lower() == "nhs number" for k in final_criteria.keys()):
            st.subheader("Bind Variables")
            st.json(bind_vars)
    except Exception as e:
        st.error(f"Error generating SQL: {e}")


def main() -> None:
    """
    The main function to run the Streamlit app.
    """
    st.title("Interactive Criteria Builder / Subject SQL Generator")
    show_top_buttons()
    get_or_init_session_state()
    filtered_keys = get_search_and_filtered_keys()

    all_keys = list(SubjectSelectionCriteriaKey)
    user_dependency_needed = check_user_dependency(all_keys)
    subject_dependency_needed = check_subject_dependency(all_keys)

    show_criteria(filtered_keys)

    user = get_user_if_needed(user_dependency_needed)
    subject = get_subject_if_needed(subject_dependency_needed)

    final_criteria = {
        key: value for key, value in st.session_state.criteria.items() if value
    }

    show_final_criteria(final_criteria)

    if final_criteria:
        show_sql_and_binds(
            final_criteria,
            user if user_dependency_needed else User(),
            subject if subject_dependency_needed else Subject(),
        )


if __name__ == "__main__":
    main()

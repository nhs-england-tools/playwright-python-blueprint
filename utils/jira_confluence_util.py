import os
import re
import shutil
from atlassian import Jira, Confluence
from pathlib import Path
from dotenv import load_dotenv
from git import Repo
from datetime import datetime

# Paths to file locations in this project
ROOT_DIR = Path(__file__).resolve().parent.parent
LOCAL_ENV_PATH = ROOT_DIR.joinpath("local.env")
RESULTS_DIR = ROOT_DIR.joinpath("test-results")


class JiraConfluenceUtil:
    """
    This is a utility designed to analyse test artifacts and upload them to Jira
    or Confluence as required.

    For this to work correctly, the following operating system variables need to
    be set (can be done using local.env if executing locally):

    For anything requiring Jira:
    - JIRA_URL: The url of the Jira instance to connect to.
    - JIRA_PROJECT_KEY: The project key for your Jira project (this is to mitigate uploading to incorrect projects).
    - JIRA_API_KEY: The API key for the user completing the action. If running locally this should be your personal key, or a Jira bot key if running via a pipeline/workflow.
    - JIRA_TICKET_REFERENCE [Optional]: The Jira ticket to default uploading to.

    For anything requiring Confluence (currently no actions supported, but will be added in the future):
    - CONFLUENCE_URL: The url of the Confluence instance to connect to.
    - CONFLUENCE_API_KEY: The API key for the user completing the action. If running locally this should be your personal key, or a Confluence bot key if running via a pipeline/workflow.

    Args:
        results_dir (pathlib.Path | str): The results directory to scan files within. If not populated, will use [parent-dir-of-this-file]/test-results (the default settings for this project).
    """

    def __init__(self, results_dir: Path | str = RESULTS_DIR) -> None:
        load_dotenv(LOCAL_ENV_PATH, override=False)
        self.jira_url = os.getenv("JIRA_URL", "")
        self.jira_project_key = os.getenv("JIRA_PROJECT_KEY", "")
        self.jira_api_key = os.getenv("JIRA_API_KEY", "")
        self.confluence_url = os.getenv("CONFLUENCE_URL", "")
        self.confluence_api_key = os.getenv("CONFLUENCE_API_KEY", "")
        self.jira_ticket_reference = os.getenv("JIRA_TICKET_REFERENCE", "")
        self.results_dir = Path(results_dir)
        if not self.results_dir.exists():
            raise ValueError(f"The filepath provided for the results directory is invalid [{str(self.results_dir)}]")

    def _can_complete_jira_actions_check(self) -> None:
        """
        Checks all required Jira OS Environment variables are set
        """
        for key in ["JIRA_URL", "JIRA_PROJECT_KEY", "JIRA_API_KEY"]:
            if not os.getenv(key):
                raise ValueError(
                    f"The [{key}] os environment variable is required to complete any Jira actions"
                )

    def _can_complete_confluence_actions_check(self) -> None:
        """
        Checks all required Confluence OS Environment variables are set
        """
        for key in ["CONFLUENCE_URL", "CONFLUENCE_API_KEY"]:
            if not os.getenv(key):
                raise ValueError(
                    f"The [{key}] os environment variable is required to complete any Confluence actions"
                )

    def _setup_jira_client(self) -> None:
        """
        Configures the Jira client if not already set
        """
        self._can_complete_jira_actions_check()
        self.jira_client = Jira(url=self.jira_url, token=self.jira_api_key)

    def _setup_confluence_client(self) -> None:
        """
        Configures the Confluence client if not already set
        """
        self._can_complete_confluence_actions_check()
        self.confluence_client = Confluence(
            url=self.confluence_url, token=self.confluence_api_key
        )

    def get_issue_data(self, ticket_id: str) -> dict | None:
        """
        Check if Jira issue exists and returns data if it does, or None if not.
        """
        try:
            self._setup_jira_client()
            issue = self.jira_client.get_issue(ticket_id)
            return issue
        except Exception as e:
            print(f"Error checking issue: {e}")
            return None

    def get_issue_summary_in_issue_data(self, issue_data: dict) -> str | None:
        return (
            f"{issue_data["key"]} ({issue_data["fields"]["summary"]})"
            if issue_data
            else None
        )

    def check_attachment_exists_in_issue_data(
        self, issue_data: dict, filename: str
    ) -> bool:
        """
        Checks if a Jira attachment already exists.
        """
        for attachment in issue_data["fields"]["attachment"]:
            if attachment["filename"] == filename:
                return True
        return False

    def is_valid_jira_reference(self, ticket_id: str) -> bool:
        """
        Determine if the ticket reference provided is valid.
        """
        self._setup_jira_client()
        if not ticket_id:
            print("ERROR: Branch name cannot be empty")
            return False

        split_id = ticket_id.split("-")
        if split_id[0] not in [self.jira_project_key]:
            print(
                f"ERROR: Jira reference '{ticket_id}' does not begin with {self.jira_project_key}"
            )
            return False
        if not split_id[1].isnumeric():
            print(
                f"ERROR: Jira reference number value '{split_id[1]}' is not numeric"
            )
            return False

        return True

    def determine_jira_reference_local(self) -> str:
        """
        Determine the current branch name from the git repository, or return JIRA_TICKET_REFERENCE if set.

        If using git to attempt to determine the branch name, you will need to ensure that ROOT_DIR in this
        project points to the root directory of your project. This will currently assume that your branch
        is named feature/<Jira Branch Name> to determine the value to use.

        NOTE: Depending on your branch naming conventions, you may have to modify this method to work with
        any specific logic your team applies to ensure the Jira reference is extracted correctly.
        """
        branch = ""
        if self.jira_ticket_reference:
            print(f"Using OS environment-specified branch name: {self.jira_ticket_reference}")
            branch = self.jira_ticket_reference
        else:
            repo = Repo(ROOT_DIR)
            branch = repo.active_branch.name

            if branch.startswith("feature/"):
                match = re.search(r"feature\/([A-Za-z0-9]+-\d+)", branch)
                if match:
                    branch = f"{self.jira_project_key}-{match.group(1)}"

        if not self.is_valid_jira_reference(branch):
            return ""

        return branch

    def get_environment_metadata_if_available(self) -> str:
        """
        Populate environment metadata if available.

        NOTE: You will need to populate this method based on your own applications logic as
        to where it retrieves the data from. It is recommended to store the results in the
        results.json file and retrieve the values from that file if possible.
        """

        # You will need to write custom logic to make this method work as intended.
        env_metadata = ""
        return env_metadata

    def is_file_is_less_than_jira_file_limit(self, file_path: Path) -> bool:
        """
        This checks that the file provided is below the Jira file size limit (10MB).
        """
        return file_path.stat().st_size < (10 * 1024 * 1024)

    def _get_files_to_upload_to_jira(
        self,
        include_html: bool,
        include_trace_files: bool,
        include_screenshots: bool,
        include_csv: bool,
    ) -> list[dict[str, str]]:
        """
        This determines the files that should be uploaded to Jira
        """
        full_file_list = []

        if include_html:
            full_file_list.extend(list(self.results_dir.glob("*.html")))

        # Get subdirectories to check for trace files and screenshots dir
        subdirectories = [d for d in self.results_dir.iterdir() if d.is_dir()]

        if include_trace_files:
            for subdir in subdirectories:
                full_file_list.extend(list(subdir.glob("*.zip")))

        if include_screenshots:
            full_file_list.extend(list(self.results_dir.glob("*.png")))
            for subdir in subdirectories:
                if subdir.name == "screenshot":
                    full_file_list.extend(list(subdir.glob("*.png")))

        if include_csv:
            full_file_list.extend(list(self.results_dir.glob("*.csv")))

        # Check if files are too big and if so, remove them
        file_too_big_list = []
        for file in full_file_list:
            if not self.is_file_is_less_than_jira_file_limit(file):
                file_too_big_list.append(file)
                print(f"! INFO: {file.name} is too big to upload to Jira (> 10MB) so will be skipped")

        for file in file_too_big_list:
            full_file_list.remove(file)

        return self._generate_file_data_dict(full_file_list)

    def _generate_file_data_dict(self, file_list: list[Path]) -> list[dict[str, str]]:
        """
        This generates the file data information for each potential file to upload
        """
        return_list = []
        file_prefix = datetime.now().strftime("%Y%m%d%H%M%S_")

        for file in file_list:
            parent_dir = "" if file.parent.match(str(self.results_dir)) else file.parent.name

            return_list.append(
                {
                    "path": file,
                    "parent_dir": parent_dir,
                    "local_file_path": f"{parent_dir}{"/" if parent_dir else ""}{file.name}",
                    "non_overwrite_name": f"{file_prefix}{parent_dir}{"_" if parent_dir else ""}{file.name}",
                    "default_name": f"{parent_dir}{"_" if parent_dir else ""}{file.name}",
                }
            )

        return return_list

    def _accept_message(self, issue_data: dict, files_to_attach: list, overwrite_files: bool, add_comment: bool) -> bool:
        """
        This generates the accept message to manually proceed with uploading files and comment.
        """

        message = f"\nThis will upload the following files {"and add a comment" if add_comment else ""} to {self.get_issue_summary_in_issue_data(issue_data)}:\n"
        for file_info in files_to_attach:
            file_exists = self.check_attachment_exists_in_issue_data(
                issue_data, file_info["default_name"]
            )

            message += f"- {file_info["local_file_path"]} "

            if file_exists and not overwrite_files:
                message += f"(as {file_info["non_overwrite_name"]})\n"
            elif file_exists and overwrite_files:
                message += f"(as {file_info["default_name"]}) [will overwrite existing file]\n"
            else:
                message += f"(as {file_info["default_name"]})\n"

        message += "\nDo you want to proceed? [y/n]: "
        input_result = input(message).strip().lower()
        if input_result != "y":
            print("Aborting upload")
            return False

        return True

    def _upload_files_to_jira(self, issue_data: dict, files_to_attach: list, overwrite_files: bool) -> list:
        """
        This uploads the files specified to the Jira ticket referenced.
        """
        # Uploaded files
        uploaded_files = []

        # Create temp directory for modifying the filename and uploading
        temp_dir = self.results_dir.joinpath("temp")
        temp_dir.mkdir(exist_ok=True)

        for file_info in files_to_attach:
            file_exists = self.check_attachment_exists_in_issue_data(
                issue_data, file_info["default_name"]
            )

            filename_to_use = file_info["default_name"]
            if file_exists and not overwrite_files:
                filename_to_use = file_info["non_overwrite_name"]

            new_file_path = shutil.copy2(Path(file_info["path"]), temp_dir.joinpath(filename_to_use))

            try:
                self.jira_client.add_attachment(issue_data["key"], str(new_file_path))
                print(f"Added attachment with {filename_to_use} to {issue_data['key']}")
                uploaded_files.append(filename_to_use)
            except Exception as e:
                print(f"ERROR: Failed to upload {filename_to_use} to {issue_data['key']}, error: {e}")

            try:
                Path(new_file_path).unlink()
            except Exception as e:
                print(f"ERROR: Failed to remove {filename_to_use} from temp directory")

        try:
            temp_dir.rmdir()
        except Exception as e:
            print(f"ERROR: Failed to remove temp directory [{str(temp_dir)}]: {e}")

        return uploaded_files

    def _add_comment_to_jira(self, ticket_id: str, uploaded_files: list, include_env_metadata: bool) -> None:
        """
        Adds a comment to Jira in a standard format based on the files uploaded.
        """

        def _default_list_layout(report_list: list, header: str) -> str:
            """
            Default logic to show results in a bullet-pointed list.
            """
            return_str = ""
            if report_list:
                return_str += f"\n*{header}:*\n"
                for report in report_list:
                    return_str += f"* [^{report}]\n"
            return return_str

        # ---

        json_metadata = self.get_environment_metadata_if_available()
        comment = "*+Test Results+*\n"

        # Sort files based on file extension
        report_lists = {
            ".html": [],
            ".zip": [],
            ".png": [],
            ".csv": [],
        }

        for file_name in uploaded_files:
            ext = Path(file_name).suffix.lower()
            if ext in report_lists:
                report_lists[ext].append(file_name)

        # Handle standard layout for non-image files
        comment += _default_list_layout(report_lists[".html"], "HTML Reports")
        comment += _default_list_layout(report_lists[".zip"], "Trace Files")
        comment += _default_list_layout(report_lists[".csv"], "CSV Output Files")

        # Put screenshots in a table with the thumbnail
        if report_lists[".png"]:
            comment += "\n*Screenshots:*\n\n||Filename||Image||\n"
            for screenshot in report_lists[".png"]:
                comment += f"|[^{screenshot}]|!{screenshot}|thumbnail!|\n"

        if json_metadata and include_env_metadata:
            comment += f"\n*+Environment Details+*\n\n{json_metadata}"

        try:
            self.jira_client.issue_add_comment(ticket_id, comment)
            print(f"Successfully added comment to {ticket_id}")
        except Exception as e:
            print(f"Failed to add comment to Jira, exception: {e}")


    def upload_test_results_dir_to_jira(
        self,
        ticket_id: str,
        overwrite_files: bool = True,
        include_html: bool = True,
        include_trace_files: bool = True,
        include_screenshots: bool = True,
        include_csv: bool = True,
        include_env_metadata: bool = True,
        add_comment: bool = True,
        automatically_accept: bool = False,
    ) -> None:
        """
        This uploads files to a specified Jira ticket and notifies of success or failure in the console.
        """

        self._can_complete_jira_actions_check()
        # Initial Message notification
        print(f"Checking files to upload from [{self.results_dir}]...\n")

        # Check issue exists
        issue_data = self.get_issue_data(ticket_id)
        if not issue_data:
            print(f"Issue data for {ticket_id} not found, exiting upload")
            return None

        # Get list of files to upload
        files_to_attach = self._get_files_to_upload_to_jira(
            include_html, include_trace_files, include_screenshots, include_csv
        )
        if not files_to_attach:
            print("No files to upload found in test-results, exiting upload")
            return None

        # Make decision
        if not automatically_accept and not self._accept_message(issue_data, files_to_attach, overwrite_files, add_comment):
            return None

        # Upload files
        uploaded_files = self._upload_files_to_jira(issue_data, files_to_attach, overwrite_files)

        # Add comment
        if add_comment:
            self._add_comment_to_jira(ticket_id, uploaded_files, include_env_metadata)

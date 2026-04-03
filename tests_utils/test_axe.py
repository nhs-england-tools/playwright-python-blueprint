import pytest
from unittest.mock import Mock, patch, MagicMock
from utils.axe import Axe
import pytest_playwright_axe


pytestmark = [pytest.mark.utils]


@pytest.fixture
def mock_page() -> Mock:
    """Create a mock Playwright page object."""
    return Mock()


@pytest.fixture
def mock_axe_instance() -> MagicMock:
    """Create a mock axe instance with mocked run methods."""
    mock_instance = MagicMock()
    mock_instance.run.return_value = {"violations": [], "passes": []}
    mock_instance.run_list.return_value = {
        "page1": {"violations": [], "passes": []},
        "page2": {"violations": [], "passes": []}
    }
    return mock_instance


@patch('utils.axe.pytest_playwright_axe.Axe')
def test_run_with_defaults(
    mock_axe_class: MagicMock,
    mock_page: Mock,
    mock_axe_instance: MagicMock
) -> None:
    """Test run method with default parameters."""
    mock_axe_class.return_value = mock_axe_instance

    Axe.run(page=mock_page)

    # Verify Axe was instantiated correctly
    mock_axe_class.assert_called_once()
    call_kwargs = mock_axe_class.call_args.kwargs
    assert "output_directory" in call_kwargs
    assert call_kwargs["output_directory"].endswith("axe-reports")

    # Verify run was called with correct parameters
    mock_axe_instance.run.assert_called_once()
    run_kwargs = mock_axe_instance.run.call_args.kwargs
    assert run_kwargs["page"] == mock_page
    assert run_kwargs["filename"] == ""
    assert run_kwargs["context"] == ""
    assert (
        run_kwargs["options"] ==
        pytest_playwright_axe.OPTIONS_WCAG_22AA
    )
    assert run_kwargs["report_on_violation_only"] is False
    assert run_kwargs["strict_mode"] is False
    assert run_kwargs["html_report_generated"] is True
    assert run_kwargs["json_report_generated"] is True


@patch('utils.axe.pytest_playwright_axe.Axe')
def test_run_with_custom_parameters(
    mock_axe_class: MagicMock,
    mock_page: Mock,
    mock_axe_instance: MagicMock
) -> None:
    """Test run method with custom parameters."""
    mock_axe_class.return_value = mock_axe_instance
    custom_output_dir = "/custom/output"
    custom_context = '{"include": [["#main"]]}'
    custom_options = (
        '{"runOnly": {"type": "tag", "values": ["wcag2a"]}}'
    )

    Axe.run(
        page=mock_page,
        filename="custom_report",
        output_directory=custom_output_dir,
        context=custom_context,
        options=custom_options,
        report_on_violation_only=True,
        strict_mode=True,
        html_report_generated=False,
        json_report_generated=False
    )

    # Verify Axe was instantiated with custom output directory
    mock_axe_class.assert_called_once_with(
        output_directory=custom_output_dir
    )

    # Verify run was called with custom parameters
    run_kwargs = mock_axe_instance.run.call_args.kwargs
    assert run_kwargs["page"] == mock_page
    assert run_kwargs["filename"] == "custom_report"
    assert run_kwargs["context"] == custom_context
    assert run_kwargs["options"] == custom_options
    assert run_kwargs["report_on_violation_only"] is True
    assert run_kwargs["strict_mode"] is True
    assert run_kwargs["html_report_generated"] is False
    assert run_kwargs["json_report_generated"] is False


@patch('utils.axe.pytest_playwright_axe.Axe')
def test_run_list_with_defaults(
    mock_axe_class: MagicMock,
    mock_page: Mock,
    mock_axe_instance: MagicMock
) -> None:
    """Test run_list method with default parameters."""
    mock_axe_class.return_value = mock_axe_instance
    page_list = ["/page1", "/page2", "/page3"]

    Axe.run_list(
        page=mock_page,
        page_list=page_list  # pyright: ignore[reportArgumentType]
    )

    # Verify Axe was instantiated correctly
    mock_axe_class.assert_called_once()
    call_kwargs = mock_axe_class.call_args.kwargs
    assert "output_directory" in call_kwargs
    assert call_kwargs["output_directory"].endswith("axe-reports")

    # Verify run_list was called with correct parameters
    mock_axe_instance.run_list.assert_called_once()
    run_list_kwargs = mock_axe_instance.run_list.call_args.kwargs
    assert run_list_kwargs["page"] == mock_page
    assert run_list_kwargs["page_list"] == page_list
    assert run_list_kwargs["use_list_for_filename"] is True
    assert run_list_kwargs["context"] == ""
    assert (
        run_list_kwargs["options"] ==
        pytest_playwright_axe.OPTIONS_WCAG_22AA
    )
    assert run_list_kwargs["report_on_violation_only"] is False
    assert run_list_kwargs["strict_mode"] is False
    assert run_list_kwargs["html_report_generated"] is True
    assert run_list_kwargs["json_report_generated"] is True


@patch('utils.axe.pytest_playwright_axe.Axe')
def test_run_list_with_dict_entries(
    mock_axe_class: MagicMock,
    mock_page: Mock,
    mock_axe_instance: MagicMock
) -> None:
    """Test run_list method with dictionary page entries."""
    mock_axe_class.return_value = mock_axe_instance
    page_list = [
        {"url": "/page1", "name": "Home"},
        {"url": "/page2", "name": "About"}
    ]

    Axe.run_list(
        page=mock_page,
        page_list=page_list  # pyright: ignore[reportArgumentType]
    )

    # Verify page_list was passed correctly
    run_list_kwargs = mock_axe_instance.run_list.call_args.kwargs
    assert run_list_kwargs["page_list"] == page_list


@patch('utils.axe.pytest_playwright_axe.Axe')
def test_run_list_with_custom_parameters(
    mock_axe_class: MagicMock,
    mock_page: Mock,
    mock_axe_instance: MagicMock
) -> None:
    """Test run_list method with custom parameters."""
    mock_axe_class.return_value = mock_axe_instance
    page_list = ["/page1", "/page2"]
    custom_output_dir = "/custom/list/output"
    custom_context = '{"exclude": [["footer"]]}'
    custom_options = (
        '{"runOnly": {"type": "tag", "values": ["wcag2aa"]}}'
    )

    Axe.run_list(
        page=mock_page,
        page_list=page_list,  # pyright: ignore[reportArgumentType]
        use_list_for_filename=False,
        output_directory=custom_output_dir,
        context=custom_context,
        options=custom_options,
        report_on_violation_only=True,
        strict_mode=True,
        html_report_generated=False,
        json_report_generated=False
    )

    # Verify Axe was instantiated with custom output directory
    mock_axe_class.assert_called_once_with(
        output_directory=custom_output_dir
    )

    # Verify run_list was called with custom parameters
    run_list_kwargs = mock_axe_instance.run_list.call_args.kwargs
    assert run_list_kwargs["page"] == mock_page
    assert run_list_kwargs["page_list"] == page_list
    assert run_list_kwargs["use_list_for_filename"] is False
    assert run_list_kwargs["context"] == custom_context
    assert run_list_kwargs["options"] == custom_options
    assert run_list_kwargs["report_on_violation_only"] is True
    assert run_list_kwargs["strict_mode"] is True
    assert run_list_kwargs["html_report_generated"] is False
    assert run_list_kwargs["json_report_generated"] is False

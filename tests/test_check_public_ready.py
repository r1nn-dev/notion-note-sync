from scripts.check_public_ready import (
    find_blocked_tracked_paths,
    normalize_git_path,
    run_public_ready_checks,
)


def test_normalize_git_path_uses_forward_slashes() -> None:
    assert normalize_git_path(r"config\pages.json") == "config/pages.json"


def test_find_blocked_tracked_paths_flags_private_files() -> None:
    findings = find_blocked_tracked_paths(
        [
            ".env",
            ".env.example",
            ".env.local",
            "config/pages.json",
            "notes/private/lesson.md",
            "README.md",
        ]
    )

    assert [finding.path for finding in findings] == [
        ".env",
        ".env.local",
        "config/pages.json",
        "notes/private/lesson.md",
    ]


def test_run_public_ready_checks_accepts_safe_tracked_files() -> None:
    findings = run_public_ready_checks(["README.md", "notes/sample.md"])

    assert findings == []

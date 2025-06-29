import subprocess
import sys


def test_expectations_exit_code(tmp_path):
    # 1. Create a tiny “bad.csv” that violates an expectation
    bad = tmp_path / "bad.csv"
    bad.write_text("a,b\n1,2\n999,1000")

    # 2. Invoke the CLI with --expectations
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dataprof",
            "profile",
            str(bad),
            "--out",
            str(tmp_path / "out"),
            "--minimal",
            "--expectations",
        ],
        capture_output=True,
        text=True,
    )

    # 3. Assert it fails (non-zero exit) and produced the suite file
    assert result.returncode != 0, "Expected non-zero exit on validation failure"
    assert (tmp_path / "out" / "expectations.json").exists()

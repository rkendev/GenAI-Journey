import subprocess
import sys


def test_expectations_exit_code(tmp_path):
    # 1) Create a tiny CSV
    bad = tmp_path / "bad.csv"
    bad.write_text("a,b\n1,2\n999,1000")

    # 2) Invoke CLI with expectations
    outdir = tmp_path / "out"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dataprof",
            "profile",
            str(bad),
            "--out",
            str(outdir),
            "--minimal",
            "--expectations",
        ],
        capture_output=True,
        text=True,
    )

    # 3) Should exit non-zero and create expectations.json
    assert result.returncode != 0
    assert (outdir / "expectations.json").exists()

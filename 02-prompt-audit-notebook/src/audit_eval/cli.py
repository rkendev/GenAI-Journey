import audit_eval.dataset as ds
import audit_eval.grader as gr
import typer

app = typer.Typer()


@app.command()
def run(sample: float = 1.0):
    data = ds.load(sample)
    if data.empty:  # extra safety net
        typer.echo("⚠️  No rows selected — add data or use --sample 1.")
        raise typer.Exit(code=1)
    passed = sum(
        gr.grade_row(q, ref) for q, ref in zip(data["question"], data["ground_truth"])
    )
    accuracy = passed / len(data)
    typer.echo(f"Finished {len(data)} samples — accuracy {accuracy:.1%}")


@app.command()
def report():
    """Render a rich/markdown report for the most recent run."""
    from audit_eval import report as rep  # lazy import

    rep  # just importing executes the script body
    typer.echo("Report written to outputs/ and printed above.")

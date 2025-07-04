import typer
from prompt_audit.client import run_prompt
from prompt_audit.templating import build_messages

app = typer.Typer()


@app.command()
def ask(question: str):
    msgs = build_messages(question)
    answer = run_prompt(msgs, temperature=0.4, top_p=0.9)
    typer.echo("\n" + answer)


if __name__ == "__main__":
    app()

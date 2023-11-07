import os
from invoke import task


@task
def install(ctx):
    """Updating requirements.txt"""
    ctx.run("pip install -r requirements.txt")


@task
def serve(ctx, d: str = "dev"):
    """Flask run"""
    os.environ["ENV"] = d
    ctx.run("flask run")


@task
def migrate(ctx, m: str, n: str = "dev", a: str = True):
    autogenerate = "--autogenerate" if a else ""
    print(f'Running : alembic -n={n} revision {autogenerate} -m "{m}"')
    ctx.run(f'alembic -n={n} revision {autogenerate} -m "{m}"')


@task
def upgrade(ctx, n: str = "dev"):
    ctx.run(f"alembic -n={n} upgrade head")


@task
def tests(ctx, d: str = "", rf: str = None, exact: str = None):
    """Run development tests."""
    os.environ["ENV"] = "unittest"
    if exact is None:
        ctx.run(f"python -m unittest discover tests/{d}")
    else:
        if exact.strip().lower() == "services.logs":
            run_function = f".{rf}" if rf else ""
            ctx.run(
                f"python -m unittest tests.services.test_logs.TestLogs{run_function}"
            )
        elif exact.strip().lower() == "services.source_app":
            run_function = f".{rf}" if rf else ""
            ctx.run(
                f"python -m unittest tests.services.test_source_app.TestSourceApp{run_function}"
            )
        elif exact.strip().lower() == "services.project":
            run_function = f".{rf}" if rf else ""
            ctx.run(
                f"python -m unittest tests.services.test_project.TestProject{run_function}"
            )
        else:
            ctx.run(f"python -m unittest tests.{exact}")

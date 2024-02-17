from duty import duty
from duty.callables import mkdocs
from duty.context import Context


@duty
def check_docs(ctx: Context):
    """Check documentation"""
    ctx.run("mkdocs build", title="Checking documentation")


@duty(fmt="pretty")
def docs(ctx: Context):
    """Generate documentation"""
    ctx.run(
        mkdocs.build,
        command="mkdocs build -vs"
    )

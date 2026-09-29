import logging

logger = logging.getLogger("pytest")


def on_start(item) -> None:
    logger.info(f"▶ START  {item.nodeid}")


def on_end(item) -> None:
    logger.debug(f"◆ END    {item.nodeid}")


def on_report(item, call) -> None:
    if call.when != "call":
        return
    if call.excinfo is None:
        logger.info(f" PASSED {item.nodeid}")
    else:
        logger.error(
            f" FAILED {item.nodeid} — "
            f"{call.excinfo.type.__name__}: {call.excinfo.value}"
        )
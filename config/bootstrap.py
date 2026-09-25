import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from config.logging_config import LoggingConfig, setup_root_logging

@dataclass
class EnvConfig:
    """Конфиг окружения: корень проекта, .env, путь к логам."""

    project_root: Path
    env_file: str = ".env"
    log_dir: Path = Path("logs")

    @classmethod
    def from_conftest(cls, conftest_file: str) -> "EnvConfig":
        """Строит конфиг от расположения conftest.py (корень проекта)."""
        root = Path(conftest_file).resolve().parent
        return cls(project_root=root, log_dir=root / "logs")


class Bootstrap:

    def __init__(self, cfg: EnvConfig, logging_cfg: LoggingConfig | None = None):
        self.cfg = cfg
        self.logging_cfg = logging_cfg or LoggingConfig(log_dir=cfg.log_dir)

    def run(self) -> None:
        self._chdir_to_project_root()
        self._load_env()
        self._setup_logging()

    def _chdir_to_project_root(self) -> None:
        os.chdir(self.cfg.project_root)

    def _load_env(self) -> None:
        load_dotenv(dotenv_path=self.cfg.project_root / self.cfg.env_file)

    def _setup_logging(self) -> None:
        setup_root_logging(self.logging_cfg)
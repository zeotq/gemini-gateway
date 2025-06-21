from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

APP_DIR = PROJECT_ROOT / "app"
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
PROMPTS_DIR = DATA_DIR / "prompts"

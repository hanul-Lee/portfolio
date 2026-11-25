"""Regenerate public concept illustrations with .venv-fonts/bin/python."""
from pathlib import Path
from runpy import run_path
for name in ['tbm', 'kanban', 'intranet', 'erp', 'measure']:
    run_path(str(Path(__file__).with_name('build-'+name+'-concepts.py')))

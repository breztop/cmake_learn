from pathlib import Path
import argparse
import os
import subprocess

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('lesson', type=int, choices=range(1, 21))
p.add_argument('--build', type=Path)
p.add_argument('--config', default='Debug')
args = p.parse_args()
source = next((root / 'lessons').glob(f'{args.lesson:02d}-*'))
build = (args.build or Path('build') / f'{args.lesson:02d}').resolve()
name = 'assetlens.exe' if os.name == 'nt' else 'assetlens'
found = [x for x in build.rglob(name) if x.is_file() and '_deps' not in x.parts]
configured = [x for x in found if args.config in x.parts]
if configured:
    found = configured
if len(found) != 1:
    raise SystemExit(f'Expected one program in {build}, found {found}. Build the chapter first.')
raise SystemExit(subprocess.call([str(found[0]), str(source / 'data/sample')]))

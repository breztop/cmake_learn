"""Build independent lessons, run fixtures and verify the installed package consumer."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--offline', action='store_true', help='skip fmt/vcpkg/GoogleTest dependency paths')
parser.add_argument('--fmt-source', type=Path, help='local fmt 10.2.1 source for FetchContent override')
parser.add_argument('--gtest-source', type=Path, help='local googletest 1.14.0 source')
parser.add_argument('--vcpkg-root', type=Path, help='validate lesson 13 using a real vcpkg toolchain')
parser.add_argument('--config', choices=['Debug', 'Release'], default='Debug')
parser.add_argument('--generator', help='CMake generator; defaults to Ninja when g++ is available')
args = parser.parse_args()
BUILD = ROOT / 'build' / ('verify-' + args.config.lower())
BUILD.mkdir(parents=True, exist_ok=True)
LOG = BUILD / 'commands.log'
REPORT = ROOT / 'validation' / ('result-' + args.config.lower() + '.json')
REPORT.parent.mkdir(exist_ok=True)
generator = args.generator or ('Ninja' if shutil.which('ninja') and shutil.which('g++') else None)
common = ['-G', generator] if generator else []
if generator and os.name == 'nt' and shutil.which('g++') and not shutil.which('cl'):
    common += ['-DCMAKE_CXX_COMPILER=' + shutil.which('g++')]
common += ['-DCMAKE_BUILD_TYPE=' + args.config]
results = []

def run(command, cwd=ROOT, expected=0):
    command = [str(x) for x in command]
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode('utf-8', errors='replace')
    with LOG.open('a', encoding='utf-8') as log:
        log.write('COMMAND ' + json.dumps(command, ensure_ascii=False) + '\n' + output + '\n')
    if (expected == 0 and result.returncode != 0) or (expected != 0 and result.returncode == 0):
        raise RuntimeError(f'Unexpected exit {result.returncode}: {command}\n{output[-5000:]}')
    return output

def configure(source, build, extra=()):
    return run(['cmake', '-S', source, '-B', build, *common, *extra])

def build_at(build):
    return run(['cmake', '--build', build, '--config', args.config, '--parallel', '2'])

def find_exe(build, name):
    filename = name + ('.exe' if os.name == 'nt' else '')
    found = [p for p in build.rglob(filename) if p.is_file() and '_deps' not in p.parts]
    if len(found) != 1:
        raise RuntimeError(f'Expected one {filename} in {build}: {found}')
    return found[0]

def check_scan(build, source, first=False):
    exe = find_exe(build, 'assetlens')
    output = run([exe, source / 'data/sample'])
    if ('files=3' if first else 'files=3 bytes=22 skipped=0') not in output:
        raise RuntimeError('Unexpected scan output: ' + output)
    if not first:
        output = run([exe, source / 'data/sample', '--ext', '.txt'])
        if 'files=2 bytes=10 skipped=0' not in output:
            raise RuntimeError('Extension filter failed: ' + output)
        report_file = build / 'scan.json'
        run([exe, source / 'data/sample', '--json', report_file])
        report = json.loads(report_file.read_text(encoding='utf-8'))
        if report['count'] != 3 or report['bytes'] != 22 or len(report['files']) != 3:
            raise RuntimeError('JSON report mismatch')
        run([exe, source / 'data/sample/missing'], expected=1)
    return exe

started = time.time()
try:
    tiny_build, tiny_install = BUILD / 'tinyreport', BUILD / 'tinyreport-install'
    configure(ROOT / 'examples/tinyreport', tiny_build)
    build_at(tiny_build)
    run(['cmake', '--install', tiny_build, '--config', args.config, '--prefix', tiny_install])
    fmt_install = BUILD / 'fmt-install'
    for source in sorted((ROOT / 'lessons').iterdir()):
        if not source.is_dir():
            continue
        number = int(source.name[:2])
        target = BUILD / source.name
        extra = []
        if number in (12, 13) and args.offline:
            results.append({'lesson': number, 'status': 'skipped', 'reason': 'offline dependency path'})
            continue
        if number == 11:
            extra += ['-DCMAKE_PREFIX_PATH=' + tiny_install.as_posix()]
        if number == 12 and args.fmt_source:
            extra += ['-DFETCHCONTENT_SOURCE_DIR_FMT=' + args.fmt_source.resolve().as_posix()]
        if number == 13:
            if args.vcpkg_root:
                extra += ['-DCMAKE_TOOLCHAIN_FILE=' + (args.vcpkg_root.resolve() / 'scripts/buildsystems/vcpkg.cmake').as_posix()]
                if os.name == 'nt' and shutil.which('g++') and not shutil.which('cl'):
                    extra += ['-DVCPKG_TARGET_TRIPLET=x64-mingw-static', '-DVCPKG_HOST_TRIPLET=x64-mingw-static']
            else:
                extra += ['-DCMAKE_PREFIX_PATH=' + fmt_install.as_posix()]
        configure(source, target, extra)
        build_at(target)
        exe = check_scan(target, source, number == 1)
        if number == 6:
            output = run([find_exe(target, 'assetlens_dynamic'), source / 'data/sample'])
            if 'files=3 bytes=22' not in output:
                raise RuntimeError('Shared library consumer failed')
        if number == 12:
            run(['cmake', '--install', target, '--config', args.config, '--prefix', fmt_install])
        if number >= 15:
            run(['ctest', '--test-dir', target, '-C', args.config, '--output-on-failure'])
        if number == 14:
            header = target / 'generated/assetlens/schema.hpp'
            before = header.stat().st_mtime_ns
            build_at(target)
            if header.stat().st_mtime_ns != before:
                raise RuntimeError('No-op build regenerated the schema')
            header.unlink()
            build_at(target)
            if not header.exists():
                raise RuntimeError('Missing output was not regenerated')
        results.append({'lesson': number, 'status': 'passed', 'dependency_route':
                        ('vcpkg' if args.vcpkg_root else 'installed fmt; vcpkg bootstrap not exercised') if number == 13 else 'chapter CMake project'})
        print(f'PASS {source.name}', flush=True)

    final_build = BUILD / 'final'
    configure(ROOT, final_build)
    build_at(final_build)
    check_scan(final_build, ROOT)
    run(['ctest', '--test-dir', final_build, '-C', args.config, '--output-on-failure'])
    install = BUILD / 'install-original'
    relocated = BUILD / 'install-relocated'
    run(['cmake', '--install', final_build, '--config', args.config, '--prefix', install])
    # Copy, then hide the original prefix for an actual relocation check.
    shutil.copytree(install, relocated, dirs_exist_ok=True)
    hidden = BUILD / 'install-original-hidden'
    if hidden.exists():
        raise RuntimeError('A previous relocation check was interrupted: restore install-original-hidden first')
    install.rename(hidden)
    try:
        consumer_build = BUILD / 'consumer'
        configure(ROOT / 'examples/consumer', consumer_build, ['-DCMAKE_PREFIX_PATH=' + relocated.as_posix()])
        build_at(consumer_build)
        run(['ctest', '--test-dir', consumer_build, '-C', args.config, '--output-on-failure'])
    finally:
        hidden.rename(install)
    results.append({'check':'relocated-package-consumer','status':'passed'})
    run(['cpack', '--config', final_build / 'CPackConfig.cmake', '-C', args.config, '-B', BUILD / 'packages'])
    results.append({'check':'zip-package','status':'passed'})

    # Disable JSON in a separate build to verify that option() changes observable behavior.
    no_json = BUILD / 'no-json'
    configure(ROOT / 'lessons/04-cache-options', no_json, ['-DASSETLENS_ENABLE_JSON=OFF'])
    build_at(no_json)
    output = run([find_exe(no_json, 'assetlens'), ROOT / 'data/sample', '--json', no_json / 'disabled.json'], expected=1)
    if 'disabled' not in output:
        raise RuntimeError('JSON option did not affect CLI behavior')
    results.append({'check':'json-option-off','status':'passed'})

    # Failure labs must fail at their documented phase.
    missing = BUILD / 'failure-missing'
    run(['cmake', '-S', ROOT / 'examples/failures/missing-package', '-B', missing, *common,
         '-DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF', '-DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY=OFF'], expected=1)
    private = BUILD / 'failure-private'
    configure(ROOT / 'examples/failures/private-include', private)
    run(['cmake', '--build', private, '--config', args.config], expected=1)
    results.append({'check':'expected-failure-labs','status':'passed'})

    if args.gtest_source and not args.offline:
        google_build = BUILD / 'google-tests'
        configure(ROOT, google_build, ['-DASSETLENS_USE_GTEST=ON', '-DFETCHCONTENT_SOURCE_DIR_GOOGLETEST=' + args.gtest_source.resolve().as_posix()])
        build_at(google_build)
        run(['ctest', '--test-dir', google_build, '-C', args.config, '--output-on-failure'])
        results.append({'check':'real-googletest','status':'passed'})
    results.append({'check':'github-actions','status':'not-run','reason':'requires upload and GitHub-hosted runner'})
    if not args.vcpkg_root:
        results.append({'check':'vcpkg-bootstrap-and-install','status':'not-run','reason':'lesson 13 CMake consumer built against a real installed fmt instead'})
    status = 'passed'
except Exception as error:
    status = 'failed'
    results.append({'check':'execution','status':'failed','error':str(error)})
    print(str(error), file=sys.stderr)
finally:
    REPORT.write_text(json.dumps({'status':status, 'platform':sys.platform, 'config':args.config,
        'generator':generator, 'seconds':round(time.time()-started, 2), 'results':results}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
sys.exit(0 if status == 'passed' else 1)

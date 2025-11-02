import sys
import os
import subprocess

print('Working dir:', os.getcwd())
print('Python:', sys.version.replace('\n',' '))

# List mp4 files in project directory (recursive)
mp4_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.lower().endswith(('.mp4','.mov','.mkv')):
            mp4_files.append(os.path.join(root, f))
print('\nFound media files (mp4/mov/mkv):')
if mp4_files:
    for p in mp4_files[:50]:
        print(' ', p)
else:
    print('  (none found in repository root)')

# PyTorch / CUDA info
try:
    import torch
    print('\nTorch version:', torch.__version__)
    cuda_avail = torch.cuda.is_available()
    print('CUDA available:', cuda_avail)
    if cuda_avail:
        cnt = torch.cuda.device_count()
        print('CUDA device count:', cnt)
        for i in range(cnt):
            try:
                name = torch.cuda.get_device_name(i)
                props = torch.cuda.get_device_properties(i)
                print(f' device {i}:', name, ', total_memory_GB=', round(props.total_memory/1024**3,2))
            except Exception as e:
                print(' device', i, 'info error:', e)
except Exception as e:
    print('\nTorch import failed:', e)

# ffmpeg availability
print('\nChecking ffmpeg...')
try:
    res = subprocess.run(['ffmpeg','-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        first = res.stdout.splitlines()[0] if res.stdout else res.stderr.splitlines()[0]
        print('ffmpeg:', first)
    else:
        print('ffmpeg not found or returned non-zero code; stderr first line:')
        print(res.stderr.splitlines()[0] if res.stderr else '(no output)')
except FileNotFoundError:
    print('ffmpeg: not found in PATH')
except Exception as e:
    print('ffmpeg check error:', e)

# Quick ffmpeg minterpolate smoke-test: try to process first 2 seconds of first mp4 (if exists)
if mp4_files:
    sample = mp4_files[0]
    out = 'test_60fps_ffmpeg.mp4'
    print('\nAttempting short ffmpeg minterpolate smoke-test on', sample)
    cmd = ['ffmpeg','-y','-i', sample, '-t', '2', '-vf', "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60'", '-c:v','libx264','-preset','veryfast','-crf','20', out]
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
        print('ffmpeg returncode:', p.returncode)
        if os.path.exists(out):
            print('Smoke test output created:', out, 'size bytes=', os.path.getsize(out))
        else:
            print('Smoke test output not created; ffmpeg stderr (last 20 lines):')
            print('\n'.join(p.stderr.splitlines()[-20:]))
    except subprocess.TimeoutExpired:
        print('ffmpeg smoke test timed out (120s)')
    except FileNotFoundError:
        print('ffmpeg not found; cannot run smoke test')
    except Exception as e:
        print('ffmpeg smoke test error:', e)
else:
    print('\nNo media files to run ffmpeg smoke test.')

print('\nLocal environment check finished.')


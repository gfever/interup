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

# Добавляю оценщик требуемого дискового пространства
def estimate_storage(duration_secs, fps, avg_frame_size_mb):
    frames = int(duration_secs * fps)
    total_mb = frames * avg_frame_size_mb
    return frames, total_mb

print('\n=== Storage estimator (approximate) ===')
# средние размеры кадра в МБ для PNG (с запасом) по разрешениям
avg_png_mb = {
    '720p': 0.5,    # примерное значение: 0.3-0.7MB
    '1080p': 1.5,   # примерное значение: 1.0-2.0MB
    '2k': 3.5,      # примерное значение
    '4k': 9.0       # примерное значение: 6-12MB
}
# если использовать JPEG/WebP можно уменьшить примерно в 2-4 раза в зависимости от качества
jpeg_factor = 0.4  # JPEG size ≈ 40% от PNG (высокое качество)

# сценарии (секунды)
scenarios = {
    'smoke_test_2s': 2,
    'one_minute': 60,
    'ten_minutes': 600
}
# пример fps: исходный 30, цель 60
fps_list = [30, 60]

for res, avg_mb in avg_png_mb.items():
    print(f'\nResolution: {res} (avg PNG frame ~{avg_mb} MB)')
    for name, secs in scenarios.items():
        for fps in fps_list:
            frames, total_mb = estimate_storage(secs, fps, avg_mb)
            total_gb = total_mb/1024
            print(f'  {name}, {fps}fps: frames={frames}, frames_storage≈{total_mb:.0f}MB (~{total_gb:.2f}GB)')
    # JPEG/WebP estimation
    for name, secs in scenarios.items():
        frames, total_mb = estimate_storage(secs, 60, avg_mb * jpeg_factor)
        print(f'  {name}, 60fps using JPEG-like frames: frames={frames}, storage≈{total_mb:.0f}MB (~{total_mb/1024:.2f}GB)')

print('\nEstimated model weights and repo sizes (approx):')
print('  RIFE weights/repo: 0.2 - 0.6 GB (200-600 MB)')
print('  Real-ESRGAN weights/repo: 0.1 - 0.5 GB (100-500 MB)')
print('  Python packages: ~0.1 GB')

print('\nRecommendations based on limited local storage:')
print(' - For quick smoke test (2s) you need only tens to a few hundred MB depending on resolution.')
print(' - For full 1-minute 1080p processing (frames extracted at 60fps) expect ~5-7 GB for frames alone; reserve ~10-15 GB total for safety (weights + outputs + temp).')
print(' - For full 1-minute 4K processing expect ~30-40 GB for frames; reserve ~50-80 GB total. For 10 minutes 4K >300 GB — impractical locally without streaming/tiling and chunking.')
print(' - To reduce disk usage: process in segments (e.g., 30-60s), delete intermediate frames after upscaling each segment, or use JPEG/WebP instead of PNG to store frames.')
print('\nUseful cleanup commands (Windows cmd):')
print(r"  del /Q .\frames\*.png  # удалить PNG кадры в папке frames")
print(r"  rmdir /S /Q .\frames  # удалить папку frames и всё внутри")
print('\nIf you want, I can now re-run the script and show these estimates for your specific target (e.g., full 1-minute 1080p at 60fps).')

# --- Команды для выполнения вручную (Windows cmd / Kaggle bash) ---
print('\n=== Готовые команды (копируйте и выполняйте в cmd.exe или в Kaggle) ===')

windows_checks = r'''
:: Перейти в папку проекта
cd /d D:\PHPStormProjects\interup

:: Проверить файл
dir dn.mp4
if exist dn.mp4 (echo file exists) else (echo file NOT found)

:: ffprobe (метаданные)
ffprobe -v quiet -print_format json -show_format -show_streams "dn.mp4"

:: Проверить, поддерживается ли minterpolate
ffmpeg -filters | findstr minterpolate
'''

windows_smoke = r'''
:: Smoke-test 2s (minterpolate)
ffmpeg -y -t 2 -i "dn.mp4" -vf "minterpolate=mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60" -c:v libx264 -preset veryfast -crf 20 "dn_60_short.mp4"
'''

windows_remux = r'''
:: Ремукс контейнера (если есть ошибки открытия)
ffmpeg -y -i "dn.mp4" -c copy "dn_remux.mp4"
ffmpeg -v error -i "dn_remux.mp4"
'''

windows_full = r'''
:: Полная конвертация в 60 fps (baseline ffmpeg)
ffmpeg -y -i "dn.mp4" -vf "minterpolate=mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60" -c:v libx264 -preset slow -crf 18 "dn_60fps_ffmpeg.mp4"

:: Быстрая альтернатива (без интерполяции, просто реплейс fps)
ffmpeg -y -i "dn.mp4" -r 60 -c:v libx264 -preset veryfast -crf 20 "dn_60fps_dup.mp4"
'''

windows_segment = r'''
:: Разбить на 10s сегменты
mkdir segments
ffmpeg -i "dn.mp4" -c copy -f segment -segment_time 10 -reset_timestamps 1 segments\part_%03d.mp4

:: Обработка сегмента: пример для part_000.mp4 (ffmpeg fallback)
ffmpeg -y -i segments\part_000.mp4 -vf "minterpolate=mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60" -c:v libx264 -preset veryfast -crf 20 working\part_000_60fps.mp4

:: Извлечь кадры как JPG (экономит место)
mkdir working\frames_part000
ffmpeg -i working\part_000_60fps.mp4 -vsync 0 working\frames_part000\frame_%06d.jpg

:: (после апскейла) собрать обратно
ffmpeg -framerate 60 -i working\up_part000\frame_%06d_up.jpg -c:v libx264 -pix_fmt yuv420p working\part_000_60fps_4k_noaudio.mp4
ffmpeg -i working\part_000_60fps_4k_noaudio.mp4 -i segments\part_000.mp4 -c copy -map 0:v:0 -map 1:a:0 output_parts\part_000_final.mp4
'''

windows_cleanup = r'''
:: Очистка промежуточных кадров (Windows)
del /Q working\frames_part000\*.jpg
rmdir /S /Q working\frames_part000
'''

kaggle_checks = r'''
# В Kaggle (bash) выполните в ячейке терминала
cd /kaggle/working
ls -lh input/dn.mp4
ffprobe -v quiet -print_format json -show_format -show_streams input/dn.mp4
ffmpeg -filters | grep minterpolate || true
'''

kaggle_smoke = r'''
# Smoke-test 2s в Kaggle
ffmpeg -y -t 2 -i input/dn.mp4 -vf "minterpolate=mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60" -c:v libx264 -preset veryfast -crf 20 output/dn_60_short.mp4
ls -lh output/dn_60_short.mp4
'''

kaggle_rife = r'''
# RIFE (DL) на Kaggle - общий пример
git clone https://github.com/hzwer/arXiv2019-RIFE.git /kaggle/working/arXiv2019-RIFE
pip install -q -r /kaggle/working/arXiv2019-RIFE/requirements.txt
# СКАЧАЙТЕ веса согласно README и положите в /kaggle/working/arXiv2019-RIFE/train_log
python /kaggle/working/arXiv2019-RIFE/inference_video.py --exp=slomo --video /kaggle/working/input/dn.mp4 --output /kaggle/working/output/dn_60fps_rife.mp4 --fp16
'''

kaggle_realesrgan = r'''
# Real-ESRGAN (апскейл) общий пример
git clone https://github.com/xinntao/Real-ESRGAN.git /kaggle/working/Real-ESRGAN
pip install -q -r /kaggle/working/Real-ESRGAN/requirements.txt
# СКАЧАЙТЕ веса согласно README
# Извлечь кадры из 60fps видео:
ffmpeg -i /kaggle/working/output/dn_60fps_rife.mp4 -vsync 0 /kaggle/working/frames/frame_%08d.png
# Запустить Real-ESRGAN (пример, подберите tile):
python /kaggle/working/Real-ESRGAN/inference_realesrgan.py --input /kaggle/working/frames --output /kaggle/working/upscaled_frames --model RealESRGAN_x4plus --tile 400 --tile_pad 10 --fp16
# Собрать видео обратно (60fps):
ffmpeg -framerate 60 -i /kaggle/working/upscaled_frames/frame_%08d_up.png -c:v libx264 -pix_fmt yuv420p /kaggle/working/output/dn_60fps_4k_noaudio.mp4
ffmpeg -i /kaggle/working/output/dn_60fps_4k_noaudio.mp4 -i /kaggle/working/input/dn.mp4 -c copy -map 0:v:0 -map 1:a:0 /kaggle/working/output/dn_60fps_4k_with_audio.mp4
'''

print('\n-- Windows (cmd.exe) checks --')
print(windows_checks)
print('-- Windows smoke/test --')
print(windows_smoke)
print('-- Windows remux if needed --')
print(windows_remux)
print('-- Windows full conversion --')
print(windows_full)
print('-- Windows segment workflow example --')
print(windows_segment)
print('-- Windows cleanup example --')
print(windows_cleanup)

print('\n-- Kaggle (bash) checks and examples --')
print(kaggle_checks)
print('-- Kaggle smoke/test --')
print(kaggle_smoke)
print('-- Kaggle RIFE (DL) example --')
print(kaggle_rife)
print('-- Kaggle Real-ESRGAN (upscale) example --')
print(kaggle_realesrgan)

print('\n=== Конец списка команд ===')

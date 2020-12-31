# If you can't run this script, please execute the following command in PowerShell.
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

$CLOUDSCRAPER_PATH=$(python -c 'import cloudscraper as _; print(_.__path__[0])' | select -Last 1)

mkdir build 
mkdir __pycache__

pyinstaller --onefile GetData.py `
    --hidden-import ADC_function.py `
    --hidden-import core.py `
    --add-data "$CLOUDSCRAPER_PATH;cloudscraper"

rmdir -Recurse -Force build
rmdir -Recurse -Force __pycache__
rmdir -Recurse -Force GetData.spec

echo "[Make]Finish"
pause
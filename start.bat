@echo off
:: Check if .venv directory exists
if exist .venv (
    :: Navigate to .venv directory
    cd .venv\Scripts

    :: Activate virtual environment
    call activate

    :: Navigate back to the project root directory
    cd ..\..

    :: Run Flask application
    flask run
) else (
    echo .venv directory not found!
)

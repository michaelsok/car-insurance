function activate_venv() {
    # try to activate virtual environment with conda
    conda activate ./.venv || \
        # if it fails, use regular environment procedure
        . ./.venv/bin/activate || \
        # if it fails, log an error to the user and exit
        (echo ""; echo "ERROR: failed to activate the virtual environment .venv!"; return 1)
}

activate_venv && (
    echo ""
    echo "=========================================="
    echo "Virtual environment successfully activated"
    echo "You are now using this python:"
    echo "$(which python)"
    echo "=========================================="
    echo ""
)

# add current path to PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

## add environment for specific users
export FORM_GCP_PROJECT="$(gcloud config get-value project)"

# set options to exit script on error
set -e

# try to create a virtual environment with conda
(conda create -y --prefix .venv pip) || \
    # if it fails, try using virtualenv with python3
    (python3 -m venv .venv && . ./.venv/bin/activate && pip install --upgrade pip) || \
    # if it fails, log an error to the user while cleaning the environment if it was partially created
    (rm -rf .venv && echo "ERROR: failed to create the virtual environment" && exit 1);

echo ""
echo "============================================="
echo "Virtual environment successfully created"
echo "It is located at:"
echo "$(pwd)/.venv"
echo "In order to activate this virtual environment"
echo "$ source activate.sh"
echo "============================================="
echo ""

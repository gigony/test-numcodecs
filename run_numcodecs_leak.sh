#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Build image
echo "Building image using the following command:"
cmd="docker build \
     -t numcodecs:latest \
     -f ${SCRIPT_DIR}/Dockerfile.numcodecs \
     ${SCRIPT_DIR}"

echo $cmd && echo

${cmd}

if [ $? -ne 0 ]; then
    >&2 echo ' '
    >&2 echo "Build failed with error $?."
    exit $?
fi

echo "Executing container..."
echo

cmd=${1:-leak}
case "$1" in
    leak)
        docker run -it --rm \
            numcodecs \
            -c "python -u /app/fail.py"
        ;;
    patch)
        docker run -it --rm \
            numcodecs \
            -c "./patch_numcodecs.sh; python -u /app/fail.py"
        ;;
    *)
        echo "Wrong command! (Use one of [leak|patch])"
        ;;
esac
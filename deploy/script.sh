#!/bin/bash

set -ex

VAGGA=${VAGGA:-vagga}
PROJECT=twicher
CONTAINERS=( redis app )

SERVER=internal.everypony.ru
USER=deploy
PORT=142
DESTINATION=/mnt/ssd/images

type ${VAGGA}
type rsync

sync_container() {
    local NAME="$1"
    local CONTAINER_NAME=${NAME}-deploy

    # Build container
    $VAGGA _build ${CONTAINER_NAME}

    # Get version
    VERSION="$($VAGGA _version_hash --short $CONTAINER_NAME)"

    # Copy image to server
    rsync -a \
        --checksum \
        -e "ssh -p $PORT" \
        --link-dest=${DESTINATION}/${PROJECT}/${CONTAINER_NAME}.latest/ \
        .vagga/${CONTAINER_NAME}/ \
        ${USER}@${SERVER}:${DESTINATION}/${PROJECT}/${CONTAINER_NAME}.${VERSION}

    # Link as latest image
    ssh ${USER}@${SERVER} -p ${PORT} ln -sfn ${CONTAINER_NAME}.${VERSION} ${DESTINATION}/${PROJECT}/${CONTAINER_NAME}.latest

    # Add to config
    cat <<END | ssh ${USER}@${SERVER} -p ${PORT} tee -a ${DESTINATION}/${PROJECT}/config.yaml
${NAME}:
    kind: Daemon
    instances: 1
    config: /lithos/${NAME}.yaml
    image: ${CONTAINER_NAME}.${VERSION}
END
}

# Remove old config
ssh ${USER}@${SERVER} -p ${PORT} rm -f ${DESTINATION}/${PROJECT}/config.yaml

for CONTAINER in ${CONTAINERS[@]}; do
    sync_container ${CONTAINER}
done

# Switch to new config
ssh -t ${USER}@${SERVER} -p ${PORT} sudo lithos_switch ${PROJECT} ${DESTINATION}/${PROJECT}/config.yaml
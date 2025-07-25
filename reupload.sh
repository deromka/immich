#!/bin/bash

ERROR_LOG="/media/ironwolf/reupload_paths_clean.txt"

while IFS= read -r filepath; do
    if [ -f "$filepath" ]; then
        echo "Re-uploading: $filepath"

        # Transform the host path to container path
        container_path="${filepath/\/media\/ironwolf\/photos/\/import}"

        docker run --rm \
            -v "/media/ironwolf/photos:/import:ro" \
            -e IMMICH_INSTANCE_URL=http://192.168.2.54:2283/api \
            -e IMMICH_API_KEY=LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q \
            ghcr.io/immich-app/immich-cli:latest upload "$container_path"
    else
        echo "File not found: $filepath"
    fi
done < "$ERROR_LOG"


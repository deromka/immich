#!/bin/bash

immich-go upload from-folder /media/ironwolf/photos/ \
 --server http://localhost:2283 \
 --on-server-errors continue \
 --log-file upload-jul-18-2025.log \
 --log-level INFO \
 --log-type text   \
 --api-key LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q \
 --skip-verify-ssl \
 --ban-file /media/ironwolf/photos/library/ \
 --ban-file /media/ironwolf/photos/thumbs/ \
 --ban-file /media/ironwolf/photos/upload/ \
 --ban-file /media/ironwolf/photos/profile/ \
 --ban-file /media/ironwolf/photos/encoded-video/ \
 --ban-file /media/ironwolf/photos/backups/

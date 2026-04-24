#!/bin/bash

# Pastikan berada di direktori yang benar jika diperlukan
# cd /home/sepol/paddleocr

python -m paddle.distributed.launch ./PaddleOCR/tools/train.py -c ocr_finetune_det.yml

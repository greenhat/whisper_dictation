#!.venv/bin/python3
# -*- coding: utf-8 -*-
##
## Copyright 2023 Henry Kroll <nospam@thenerdshow.com>
## 
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
## MA 02110-1301, USA.
##
import os, shlex
import tempfile
import threading
from faster_whisper import WhisperModel

# model_size = "large-v2"
# model_size = "small.en"
model_size = "medium.en"

# Run on GPU with FP16
# model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
model = WhisperModel(model_size, device="cpu", compute_type="int8")

print("Start speaking. Text should appear in current window.")
def transcribe(f):
    # transcribe it
    try:
        segments, info = model.transcribe(f, beam_size=5)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        for segment in segments:
            txt = shlex.quote(segment.text)
            if segment.text != ' you':
                print('\r' + segment.text)
                os.system("xdotool type --clearmodifiers " + txt)
    except Exception as e: print(e)
    # cleanup
    os.remove(f)
    
while (1):
    # record some (more) audio
    temp_name = tempfile.gettempdir() + '/' \
    + next(tempfile._get_candidate_names()) + ".mp3"
    os.system("./record.py " + temp_name)
    
    if not os.path.getsize(temp_name):
        if os.path.exists(temp_name):
            os.remove(temp_name)
        exit()
        
    # transcribe and remove
    t1 = threading.Thread(target=transcribe, args=[temp_name])
    t1.start()

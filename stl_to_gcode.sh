#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="~/Downloads/raw_meshes/raw_meshes/*.stl"
out_path="~/workspace/blender_spag_generation/gcodes/"
i=0
for f in ~/Downloads/raw_meshes/raw_meshes/*.stl
do
  ((i=i+1))
  if [[ $i -le 150 ]]; then
    echo $f
    continue
  fi
  echo $i
  #filename="${f%.*}"
  echo $f
  #./MyProgram.exe "$filename" "Logs/$(basename "$filename" .txt)_Log$i.txt"
  #  mandoline -o "$out_path$(basename "$f").gcode" -n "$f"
  mandoline -o ~/workspace/blender_spag_generation/gcodes/$i.gcode -n "$f"
  if [[ $i -eq 500 ]]; then
    break
  fi
done
#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="~/Downloads/raw_meshes/raw_meshes/*.stl"
out_path="~/workspace/blender_spag_generation/gcodes/"
i=0
for f in *.stl
do
  ((i=i+1))
  echo $i
  #filename="${f%.*}"
  echo $f
  #./MyProgram.exe "$filename" "Logs/$(basename "$filename" .txt)_Log$i.txt"
  #  mandoline -o "$out_path$(basename "$f").gcode" -n "$f"
  mandoline -o ~/blender_spag_generation/gcodes/$i.gcode -n "$f"
  if [[ $i -eq 150 ]]; then
    break
  fi
done

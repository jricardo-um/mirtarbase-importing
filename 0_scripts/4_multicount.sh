cmd='./.venv/bin/python'
fl='./0_scripts/4_count_hp.py'
for i in {1..6}
do
   $cmd $fl $i | tee "./memoria/count$i.txt" &
done
wait
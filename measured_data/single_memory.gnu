set terminal eps solid color

set xlabel "Velikost grafu |V|+|E|"
set ylabel "Paměť [MiB]"

if (!exists("filename")) filename='pass'

set output filename.'.eps'
set key autotitle columnhead
set datafile separator ','

plot for[x = 2:6] filename.'.csv' using 1:x smooth unique

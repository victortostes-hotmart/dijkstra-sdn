#!/bin/sh 

declare -a arr=('h1' 'h3' 'h5' 'h7')

rm -Rf results
mkdir -p results
mkdir -p results/plots

for i in "${arr[@]}"
do
  cat iperf_${i}.txt | grep sec | head -15 | tr - " " | awk '{print $4, $8, $10}' > results/result_${i}.dat
  gnuplot -e "
    set terminal png;
    set output 'results/plots/${i}.png';
    set title 'UDP Flow';
    set xlabel 'Time (secs)';
    set ylabel 'Throughput (Mbps)';
    set y2label 'Jitter (ms)';
    plot 'results/result_${i}.dat' using 1:2:xtic(1) title 'Throughput' with lines, \
                                '' using 1:3:xtic(1) title 'Jitter' with lines
  "
done

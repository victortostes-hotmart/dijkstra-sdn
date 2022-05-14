#!/bin/sh 

declare -a arr=('h1' 'h3')

FILE=$1
PROTOCOL=$2
TIME=$3

if [ ! -d $FILE ]
then
  echo "$FILE does not exists."
  exit;
fi

if [ ! $PROTOCOL ]
then
  echo "Protocol is required"
  exit;
fi

if [ ! $TIME ]
then
  echo "Time is required"
  exit;
fi

cd $FILE;
# rm -Rf results
mkdir -p results
mkdir -p results/plots

if [ $PROTOCOL = "UDP" ]; then
  for i in "${arr[@]}"
  do
    cat ${PROTOCOL}_${i}.txt | grep sec | head -${TIME} | tr - " " | awk '{print $4, $8, $10}' > results/${PROTOCOL}_${i}.dat
    gnuplot -e "
      set terminal png;
      set output 'results/plots/${PROTOCOL}_${i}.png';
      set title 'UDP Flow';
      set xtics 0,1,${TIME};
      set ytics 0,1,3;
      set xrange[0:${TIME}];
      set yrange[0:3];
      set xlabel 'Time (secs)';
      set ylabel 'Throughput (Mbps)';
      set y2label 'Jitter (ms)';
      plot 'results/${PROTOCOL}_${i}.dat' using 1:2:xtic(1) title 'Throughput' with lines, \
                                  '' using 1:3:xtic(1) title 'Jitter' with lines;
    "
  done

elif [ $PROTOCOL = "TCP" ]; then
  for i in "${arr[@]}"
  do
    cat ${PROTOCOL}_${i}.txt | grep sec | head -${TIME} | tr - " " | awk '{print $4, $8}' > results/${PROTOCOL}_${i}.dat
    gnuplot -e "
      set terminal png;
      set output 'results/plots/${PROTOCOL}_${i}.png';
      set title 'TCP Flow';
      set xrange[0:${TIME}];
      set yrange[0:3];
      set xtics 0,1,${TIME};
      set ytics 0,1,3;
      set xlabel 'Time (secs)';
      set ylabel 'Throughput (Mbps)';
      plot 'results/${PROTOCOL}_${i}.dat' using 1:2:xtic(1) title 'Throughput' with lines;
    "
  done
else
  echo "Invalid protocol";
fi



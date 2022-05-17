#!/bin/sh 

FOLDER=$1
SERVERS=$2

if [ ! -d $FOLDER ]
then
  echo "$FOLDER folder does not exists."
  exit;
fi

if [ ! $SERVERS ]
then
  echo "Servers is required"
  exit;
fi

cd $FOLDER;
rm -f database_UDP.csv;
rm -f database_TCP.csv;

counter=1
until [ $counter -gt $SERVERS ]
do
  if [ -f "UDP_h$counter.txt" ]
  then
    cat UDP_h${counter}.txt \
      | grep sec \
      | awk '!/out-of-order/' \
      | awk '!/-\/-\/-\/-/' \
      | tr -d ']%()' \
      | sed -e "s/\/ /\//2" \
      | awk '{
        split($3,a,"-"); 
        split($14,b,"/"); 
        print $2,a[1],a[2],$5,$6,$7,$8,$9,$10,$13,b[1],b[2],b[3],b[4],$15,$16}
      ' \
      | sed -e "s/^/H$counter UDP /" \
      | tr -s '[:blank:]' ',' \
    >> database_UDP.csv 
  fi

  if [ -f "TCP_h$counter.txt" ]
  then
    cat TCP_h${counter}.txt \
      | grep sec \
      | awk '!/out-of-order/' \
      | awk '!/out-of-order/' \
      | tr -d ']%()' \
      | sed -e "s/- /-/g" \
      | awk '{
        split($3,a,"-"); 
        split($14,b,"/"); 
        print $2,a[1],a[2],$5,$6,$7,$8}
      ' \
      | sed -e "s/^/H$counter TCP /" \
      | tr -s '[:blank:]' ',' \
    >> database_TCP.csv 
  fi
  
  ((counter++))
done
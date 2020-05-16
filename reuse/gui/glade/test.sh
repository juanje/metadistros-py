#!/bin/sh

echo 5

sleep 1

echo "Empezamos... XXX"

for i in `seq 6 40`
	do
		echo $i
		sleep 1
		if [ $i = 15 ]; then
			echo "XXX Buscamos particiones... XXX"
		elif [ $i = 25 ]; then
			echo "XXX Formateamos y demas... XXX"
		fi
done

echo "XXX Copiando... XXX"

for i in `seq 41 98`
	do
		echo $i
		sleep 1
		if [ $i = 95 ]; then
			echo "XXX Termiando... XXX"
		fi
done

sleep 1

echo "XXX FIN XXX"


echo 99

sleep 1

echo 100


echo 101

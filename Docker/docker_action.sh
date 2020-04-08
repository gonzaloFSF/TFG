#!/bin/bash




function create {

	docker build -t gonzalofsf/tfg-simulador:test .

}

function run {

	docker run -d -p 222:22 -p $1:8080  --name prueba gonzalofsf/tfg-simulador:test

}


function delete {

	docker kill prueba
	docker rm prueba

}


function pull {

	docker pull gonzalofsf/tfg-simulador:test

}

function push {

	docker push  gonzalofsf/tfg-simulador:test

}

function logs {

	docker logs prueba

}

if [ $(id -u) != "0" ];
then

	echo "Root privileges are necesarie";
	exit 10

fi

if [ $# == 0 ];
then

	echo "One option is required";
	exit 11

fi


case $1 in

	"create")

		create;

	;;

	"run")	
		run $2;
	
	;;

	"delete")
	
		delete;
	
	;;

	"pull")
	
		pull;
	
	;;
	
	"push")
	
		push;
	
	;;
	
	"logs")
	
		logs;
	
	;;

	*)
	
		echo "Option $1 is not available";
	
	;;

esac

exit

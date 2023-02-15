#!/usr/bin/bash

#shuiguolao [--python] [--js] (参数全空时，才启用--python)
#shuiguolao -i
#shuiguolao file

SGL_BIN=$(realpath $0)
SGL_DIR=$(dirname $SGL_BIN)

#PARAMS_ALL=$@
#PARAMS_ALL+=' --python'
#主要解决传递参数含空格的问题，太恶心了
#the last -- merge prior, so first as default option 
PARAMS_ALL=('--python')
i=1
for arg in "$@"
do
	echo $arg
	PARAMS_ALL[$i]=$arg
	i=$i+1
done

#echo '>>>'${PARAMS_ALL[0]} ${PARAMS_ALL[1]}
function param_exists(){
	for arg in "${PARAMS_ALL[@]}"
	do
		if [[ $arg == $1 ]]
		then
			echo 1
		fi
	done
}


#we regard everything not starting with '-' as a script
#发现script参数，后面的参数直接全部传递给后面
#TODO 这个列表的展开还是不支持空格
child_args=()
for arg in "${PARAMS_ALL[@]}"
do
	if [[ $SCRIPT_PATH ]]
	then
		child_args+=($arg)
		#echo ">> ${child_args[@]}"
		
	elif [[ ${arg:0:1} != '-' ]]
	then
		SCRIPT_PATH=$arg
		SCRIPT_SUFFIX=${arg##*.}
		#echo $SCRIPT_PATH, $SCRIPT_SUFFIX
		# when no suffix stay same, so have the second condition,
		if [[ $SCRIPT_SUFFIX == '' ]] || [[ $SCRIPT_SUFFIX == $arg ]]
		then
			echo 'is  '$SCRIPT_PATH' a script path? quit..'
			exit -1
		fi
	fi
done


#if [[ $SCRIPT_PATH ]] && [[ -z $SCRIPT_SUFFIX ]]
#fi
for arg in "${PARAMS_ALL[@]}"
do
	if [[ $arg == '--python' ]]
	then
		VM='py'
		REPL_S="${config[py_BIN]} -i "
	elif [[ $arg == '--js' ]]
	then
		VM='js'	
		REPL_S="${config[js_BIN]} -r "
	elif [[ ${arg:0:2} == '--' ]]
	then
		echo 'unspecified scripty type: '$1
		exit -1
	fi
done


SGL_VM=$SGL_DIR/$VM
SGL_HISTORY=$SGL_VM'/history'
SGL_VIMRC_PATH=$SGL_DIR/shuiguolao.vimrc
#echo $SGL_VIMRC_PATH

REPL_CMD=$REPL_S$SGL_VM/terminal.$VM

#read config.txt and build configuration dictionary
i=1
declare -A config
while read line; do
	key=${line%=*}
	value=${line#*=}
	if [[ $key ]]
	then
		config[$key]=$value
	fi
done < $SGL_DIR/config.txt
#echo ${!config[@]}
#echo ${config[@]}

RUN_SCRIPT=''
if [[ $SCRIPT_PATH != '' ]]
then
	BIN=${config["$SCRIPT_SUFFIX"_BIN]}
	if [[ $SCRIPT_SUFFIX == 'py' ]]
	then
		RUN_SCRIPT="$BIN "$SGL_DIR/py/shuiguolao.py
	elif [[ $SCRIPT_SUFFIX == 'js' ]]
	then
		RUN_SCRIPT="$BIN -r "$SGL_DIR/js/terminal.js
	else 
		echo 'unknown script type, quit..'
		exit -1
	fi
fi


#make file name
st=`date +-%m-%d\ %H:%M:%S`
st=${st:2:-1}
#echo "The date and time are:" $st
#INPUT_FILE_NAME=$st."$VM"
#INPUT_FILE_PATH=$SGL_HISTORY/$INPUT_FILE_NAME


if [[ $RUN_SCRIPT ]]
then
	#echo $RUN_SCRIPT
	#echo $SCRIPT_PATH
	$RUN_SCRIPT "$SCRIPT_PATH" "${child_args[@]}"
elif [[ $(param_exists -i) ]]
then
	$REPL_CMD
else 
	${config[vim_BIN]} -S "$SGL_VIMRC_PATH" "shuiguolao-$VM"
fi














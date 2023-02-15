#!/usr/bin/bash

#shuiguolao [--python] [--js] (参数全空时，才启用--python)
#shuiguolao -i
#shuiguolao file

SGL_BIN=$(realpath $0)
SGL_DIR=$(dirname $SGL_BIN)


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
for arg in "$@"
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
			break
			echo 'is  '$SCRIPT_PATH' a script path? quit..'
			exit -1
		fi
	fi
done

#PARAMS_ALL=$@
#PARAMS_ALL+=' --python'
#主要解决传递参数含空格的问题，太恶心了
#the last -- merge prior, so first as default option 
#在没有检测到script_path的情况下，才追加--python做为默认
if [[ $SCRIPT_PATH == '' ]]
then
	PARAMS_ALL=('--python')
else
	PARAMS_ALL=()
fi
i=1
for arg in "$@"
do
	echo $arg
	PARAMS_ALL[$i]=$arg
	i=$i+1
done

#接下来检测--vm


for arg in "${PARAMS_ALL[@]}"
do
	if [[ $arg == '--python' ]]
	then
		VM='py'
	elif [[ $arg == '--js' ]]
	then
		VM='js'	
	elif [[ ${arg:0:2} == '--' ]]
	then
		echo 'unspecified scripty type: '$arg
		exit -1
	fi
done

#接下来检测--VM是否与SUFFIX冲突
if [[ $VM ]]
then
	if [[ $SCRIPT_SUFFIX ]] && [[ $VM != $SCRIPT_SUFFIX ]] 
	then
		echo 'conflict suffix:'$SCRIPT_SUFFIX' with --'$VM		
		exit -1
	fi
else
	VM=$SCRIPT_SUFFIX
fi


VM_BIN=${config["$VM"_BIN]}
SGL_VM=$SGL_DIR/$VM
SGL_HISTORY=$SGL_VM'/history'
SGL_VIMRC_PATH=$SGL_DIR/shuiguolao.vimrc
#注意,lib目录只能放在最后面，否则会出奇怪错误?
VM_PATH=$SGL_VM/lib:$SGL_VM/history

if [[ $VM == 'py' ]]
then
	#BIN=${config[py_BIN]}
	REPL_S="$VM_BIN -i "
	export PYTHONPATH=$PYTHONPATH:$VM_PATH
elif [[ $VM == 'js' ]]
then
	#VM='js'	
	#BIN=${config[js_BIN]}
	REPL_S="$VM_BIN -r "
	export NODE_PATH=$NODE_PATH:$VM_PATH
else
	exit -1
fi
REPL_CMD=$REPL_S$SGL_VM/lib/preload.$VM
#echo $PYTHONPATH, $NODE_PATH



#make file name
st=`date +-%m-%d\ %H:%M:%S`
st=${st:2:-1}
#echo "The date and time are:" $st

if [[ $SCRIPT_PATH ]]
then
	#echo $RUN_SCRIPT
	#echo $SCRIPT_PATH
	#$RUN_SCRIPT "$SCRIPT_PATH" "${child_args[@]}"
	$VM_BIN "$SCRIPT_PATH" "${child_args[@]}"
elif [[ $(param_exists -i) ]]
then
	echo $REPL_CMD
	$REPL_CMD
else 
	${config["vim_BIN"]} -S "$SGL_VIMRC_PATH" "shuiguolao-$VM"
fi














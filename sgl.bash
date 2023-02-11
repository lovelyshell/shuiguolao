#!/usr/bin/bash

if [[ $1 == '--python' ]] || [[ $1 == '' ]]
then
	VM='py'
elif [[ $1 == '--js' ]]
then
	VM='js'	
else
	echo 'unspecified scripty type: '$1
	exit -1
fi

SGL_BIN=$(realpath $0)
SGL_DIR=$(dirname $SGL_BIN)
SGL_VM=$SGL_DIR/$VM
SGL_HISTORY=$SGL_VM'/history'
SGL_VIMRC_PATH=$SGL_DIR/shuiguolao.vimrc
#echo $SGL_VIMRC_PATH


#make file name
st=`date +-%m-%d\ %H:%M:%S`
st=${st:2:-1}
#echo "The date and time are:" $st
#INPUT_FILE_NAME=$st."$VM"
#INPUT_FILE_PATH=$SGL_HISTORY/$INPUT_FILE_NAME



vim -S "$SGL_VIMRC_PATH" "shuiguolao-$VM"





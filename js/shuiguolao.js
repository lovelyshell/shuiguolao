#!/usr/bin/nodejs
const Path = require('path')
const subprocess = require('child_process')


console.log('hello world')
function print(x){
	console.log(x)
}
function check_js_version(){
	print(process.version)
}

check_js_version()
//print(process.execPath)
//print(__filename)
let SGL_JDIR_PATH = Path.resolve(__dirname)
let SGL_DIR_PATH = Path.dirname(SGL_JDIR_PATH)
let SGl_TDIR_PATH = Path.join(SGL_DIR_PATH, 'test')
let SGL_VIMRC_PATH = `${SGL_DIR_PATH}/shuiguolao.vimrc`
let cmd_s = `vim  -S ${SGL_VIMRC_PATH} jshuiguolao`
let cmd_options = ['-S', SGL_VIMRC_PATH, 'jshuiguolao']

const child_process = require('child_process')
var editor = process.env.EDITOR || 'vi';

var child = child_process.spawn(editor, cmd_options, {
    stdio: 'inherit'
});

child.on('exit', function (e, code) {
    console.log("finished");
});

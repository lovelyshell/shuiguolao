#!/usr/bin/nodejs
const Path = require('path')
const {File,OverWriteError} = require('../lib/File.js')
const strftime = require('../strftime.js')
const fs = require('fs')

let cwd = new File('.')
sgl_run_timestamp_s = strftime.strftime('%H:%M:%S', new Date().getTime())
console.log(`****************run ${sgl_run_timestamp_s}************`)
/***************shuiguolao version 0.1*********************
*shortcut:                                                *
*<C-N>    browse history, down                            *
*<C-P>    browse history, up                              *
*<C-S>-r  save and run file in main window                *
*<C-S>-R  save and (as root) run file in main window      *
*<C-S>-n  create a new file                               *
*created at 2023/02/11 04:34:02                           *
***********DO NOT EDIT LINES ABOVE!!***********************
***********WRITE YOUR CODE BELOW**************************/
for (f of cwd.files){ console.log(f.name, f.size) }

File.R(cwd, (f, rinfo) =>{
	if(f.name == 'history' || f.name == '.git') return false
	console.log(' '.repeat(rinfo.depth*3), f.name)
})




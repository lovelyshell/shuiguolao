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
*<C-S>-R  save and prepare to run file in main window     *
*<C-S>-N  create a new file                               *
*created at xxxx/xx/xx xx:xx:xx                           *
***********DO NOT EDIT LINES ABOVE!!***********************
***********WRITE YOUR CODE BELOW**************************/






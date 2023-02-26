#!/usr/bin/shuiguolao

require('preload.js')

import {pathToFileURL} from 'url'

// module was not imported but called directly
if (import.meta.url === 
	pathToFileURL(process.argv[1]).href) {
	console.log(`****************run\
  	${sgl_run_timestamp_s}************`)
}
/***************shuiguolao version 0.1*********
*shortcut:                                    *
*<C-N>    browse history, down                *
*<C-P>    browse history, up                  *
*<C-S>-r  save and run file                   *
*<C-S>-R  save and prepare to run file        *
*<C-S>-N  create a new file                   *
*created at xxxx/xx/xx xx:xx:xx               *
***********DO NOT EDIT LINES ABOVE!!***********
***********WRITE YOUR CODE BELOW**************/


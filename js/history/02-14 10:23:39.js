#!/usr/bin/shuiguolao

console.log(`****************run\
  ${sgl_run_timestamp_s}************`)
/***************shuiguolao version 0.1*********
*shortcut:                                    *
*<C-N>    browse history, down                *
*<C-P>    browse history, up                  *
*<C-S>-r  save and run file                   *
*<C-S>-R  save and prepare to run file        *
*<C-S>-N  create a new file                   *
*created at 2023/02/14 10:23:39               *
***********DO NOT EDIT LINES ABOVE!!***********
***********WRITE YOUR CODE BELOW**************/

for (f of cwd.files){
    console.log(f.name)
}

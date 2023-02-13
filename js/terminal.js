const Path = require('path')

const {File, OverWriteError} = require('./lib/File.js')
const strftime = require('./strftime.js')
const fs = require('fs')

let cwd = new File('.')
//sgl_run_timestamp_s = strftime.strftime('%H:%M:%S', new Date().getTime())

global.cwd = cwd
global.File = File
global.fs = fs
global.strftime = strftime
global.OverWriteError = OverWriteError
global.Path = Path
global.sgl_run_timestamp_s = strftime.strftime('%H:%M:%S', new Date().getTime())

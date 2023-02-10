"use strict";
const os = require('os')
const fs = require('fs')
const Path = require('path')

class FileMode{
	constructor(value){
		this.value = value
	}
	get value(){
		return this.perms.value
	}
	set value(x){
		//ignore this three for nodejs not implemnt it
		this.setuid = 0
		this.setgid = 0
		this.sticky = 0
		this.perms = new FilePerms(x)
	}
}

class FilePerms{
	constructor(_value){
		//call setter
		this.value = _value
	}
	set value(_value){
		this._other = new FilePerm(_value & 7)
		this._group = new FilePerm((_value >> 3) & 7)
		this._owner = new FilePerm((_value >> 6) & 7)
	}
	get value(){
		let x = this.other.value 
			+ (this.group.value << 3) + (this.owner.value << 6)
		return x
	}
	get owner(){ return this._owner}
	get group(){ return this._group}
	get other(){ return this._other}

	set owner(value){ this._owner = new FilePerm(value)}
	set group(value){ this._group = new FilePerm(value)}
	set other(value){ this._other = new FilePerm(value)}
	
	format(){
		let s = ''
		for (var key of ['_owner', '_group', '_other'])	{
			s += this[key].format('-')
		}
		return s
	}
}

class FilePerm{
	static s2i(s){
		let i = 0
		if(s.search('r') != -1) i+=4
		if(s.search('w') != -1) i+=2
		if(s.search('x') != -1) i+=1
		return i;
	}

	format(padden=''){
		var s = '';
		for(var key of ['r','w','x']){
			if(this[key]) s+=key;
			else s+= padden;
		}
		return s;
	}


	get value(){
		return this._value
	}
	set value(x){
		var i
		if(typeof(x) == 'string') { i = FilePerm.s2i(x) }
		else if (typeof(x) == 'number'){i = x }
		else if(x instanceof FilePermit){
			i = x.value 
		}
		else throw Error('unexpected argument type, need number or string')
		this._value = i
	}
	get r() {return this.value & 4}
	get w() {return this.value & 2}
	get x() {return this.value & 1}
	set r(yes) {if(yes){this.value |= 4}else{this.value &= ~4}}
	set w(yes) {if(yes){this.value |= 2}else{this.value &= ~2}}
	set x(yes) {if(yes){this.value |= 1}else{this.value &= ~1}}

	constructor(x){
		this._value = 0
		this.value = x;
	}
}

class OverWriteError extends Error{
	constructor(message){
		super(message)
		this.name = 'OverWriteError'
		Error.captureStackTrace(this, this.constructor)
	}
}

function throw_overwrite_error(f, expect_type){
	let expect_type_name = TypeNames[expect_type]
	let got_type_name = TypeNames[f.type]
	throw new OverWriteError(`dare not overwrite an existed file but different type, expect "${expect_type_name}", got "${got_type_name}" [${f.path}]`)
}

function getoseol(osname=null){
	if(osname == null)
		osname = os.platform()
	switch(osname){
		case 'freebsd':
		case 'linux':
		case 'sunos':
		case 'aix':
		case 'darwin':
			return '\n';
			break
		case 'win32':
			return '\r\n'
			break
		default:
			return null;
	}
}

let TypeNames = []
TypeNames[fs.constants.S_IFREG] = 'file'
TypeNames[fs.constants.S_IFDIR] = 'directory'
TypeNames[fs.constants.S_IFLNK] = 'symlink'

class File{
	get consts(){
		return fs.constants	
	}

	static _R(d, fn, cur_depth, max_depth, errlvl){
			function handle(err, errlvl){
					if(errlvl == 0){}
					else if(errlvl == 1){
							process.stderr.write(err.message+'\n')
					}
					else {
							throw err
					}
			}
			try{
					for(let f of d.files){
						fn(f, {depth:cur_depth})
						if(f.is_dir() && cur_depth != max_depth){
								File._R(f, fn, cur_depth+1, max_depth, errlvl)
						}
					}
			}
			catch(err){ handle(err, errlvl)}
	}

	static R(pathlike, fn, {skip_zero=0, max_depth=-1, errlvl=1}={}){
			let f;
			if(pathlike instanceof File){f = pathlike}
			else if(typeof(pathlike) == 'string'){
				f = new File(pathlike)	
			}
			else throw new Error('@pathlike, invalid argument type, require string or File')

			File._R(f, fn, 0, max_depth, errlvl)		
	}
		/*
	static R(f, fn, {skip_zero=0, max_depth=-1, lost_ok=0, skip_last=0}={}){
			if(f.isLink()){
					let depth = 0;
					while(f.isLink()){
							if(depth == 0 && skip_zero){}
							else{
								fn(f, {depth:depth})		
							}
							depth++
							if(depth == max_depth){
								break;							
							}
							try{
								f = f.target
							}
							catch(err){
								if(lost_ok) break;
								else throw err;
							}
					}
					if(!f.isLink() && !skip_last){
						fn(f, {depth:depth}	)
					}
			}
	}
	*/

	drop_data(){
		this._dict = null
		this._data = null
		this._text = null
		this._lines = null
		this._link = null
		this._target = null
	}
	drop_stat(){
			this._stat = null
	}
	drop_cache(){
			this.dropStat()
			this.dropData()
	}

	exists(){
			return fs.existsSync(this.path)
	}
	read_check(want_type){
		if(this.type != want_type){
				throw new Error(`this function does not work on file type "${this.typename}"`)
		}
	}
	write_check(want_type){
			if(this.exists() && this.type != want_type){
				throw_overwrite_error(this, want_type)
			}
	}
	constructor(path){
		let arg_path = Path.normalize(path)
		let fullpath = Path.resolve(arg_path)
		this._path = fullpath
		this._arg_path = arg_path

		this._dict = null
		this._data = null
		this._text = null
		this._lines = null
		this._link = null
		this._target = null

		this._stat = null

		this.debug_on = 1
		this._r_eol = null		//lastest eol the user passed for reading 
		this._r_encoding = null		//lastest encoding the passed for reading
	}
	get parent(){
		let ppath = Path.dirname(this.path)
		return new File(ppath)
	}
	get dict(){
			this.read_check(fs.constants.S_IFDIR)
			if(this._dict == null){
				let _dict = {}
				let list = fs.readdirSync(this.path)	
				for(var name of list){
						let f_path = Path.join(this.path, name)
						_dict[name] = new File(f_path)
				}
				this._dict = _dict
			}
			return this._dict
	}
	get list(){ return Object.keys(this.dict) }
	get files(){return Object.values(this.dict)}
	get stat(){
		if(this._stat == null){
			let _stat = fs.lstatSync(this.path)
			this._stat = _stat
		}
		return this._stat
	}
	get path(){
		return this._path
	}
	get argPath(){
		return this._arg_path
	}
	get name(){
		return Path.basename(this._path)
	}

	read_data(){
		if(this._data == null){
			let options = {encoding:null}
			let _data = fs.readFileSync(this._path, options)
			this._data = _data
		}
		return this._data;
	}
	write_data(data){
		this.drop_cache()
		fs.writeFileSync(this.path, data)
		this._data = data
	}

	read_text(encoding='utf8'){
		//re-decode if user pass another encoding
		if (this._text == null || this._r_encoding != encoding){
				this._r_encoding = encoding
				let data = this.read_data()
				let s = data.toString(encoding)
				this._text = s
		}
		return this._text
	}

	//rely on write_data drop cache
	write_text(s, encoding='utf8'){
		let buf = Buffer.from(s, encoding)
		this.write_data(buf)
		this._text = s
	}

	read_lines(eol=null){
		//re-split if user pass another eol
		if(this._lines == null || this._r_eol != eol){
				this._r_eol = eol
				if(!eol) eol = getoseol()
				let text = this.read_text()
				let lines = text.split(eol)
				this._lines = lines
		}
		return this._lines
	}

	//rely on write_raw drop cache
	write_lines(lines, eol=null, encoding='utf8'){
		if(!eol) eol = getoseol()
		let s = lines.join(eol)
		this.write_text(s, encoding=encoding)
		this._lines = lines
	}

	read_link(){
			this.read_check(fs.constants.S_IFLNK)
			if (this._link == null){
				let to = fs.readlinkSync(this.path)
				this._link = to
			}
			return this._link
	}
	
	write_link(to){
		let S_IFLNK = fs.constants.S_IFLNK
		if(this.exists()){
			if(this.type == S_IFLNK){
				fs.unlinkSync(this.path)	
			}
			else{
				throw_overwrite_error(this, S_IFLNK)	
			}
		}
		this.drop_cache()
		fs.symlinkSync(to, this.path)
		this._link = to
	}

	read_target(){
		this.read_check(fs.constants.S_IFLNK)
		if(this._target == null){
			let to = this.read_link()
			if(!Path.isAbsolute(to)){
				let pathdir = Path.dirname(this.path)
				to = Path.join(pathdir, to)
			}
			let f = new File(to)
			this._target = f
		}
		return this._target
	}

	//rely on write_link drop cache
	write_target(f){
		this.write_check(fs.constants.S_IFLNK)
		let to = f.path
		this.write_link(to)
		this._target = f
	}

	/*
	is_link(){ return this.stat.isSymbolicLinkSync() }
	is_file(){ return this.stat.isFileSync() }
	is_dir(){ return this.stat.isDirectorySync() }
	*/
	is_link(){ return this.type == fs.constants.S_IFLNK }
	is_file(){ return this.type == fs.constants.S_IFREG }
	is_dir(){ return this.type == fs.constants.S_IFDIR }

	get link(){ return this.read_link() }
	set link(s){ this.write_link(s) }
	get target(){ return this.read_target() }
	set target(f){ this.write_target(f) }

	get data(){return this.read_data()}
	get text(){return this.read_text()}
	get lines(){ return this.read_lines() }
	set data(data){this.write_data(data)}
	set text(text){this.write_text(text)}
	set lines(lines){this.write_lines(lines)}

	get dev(){return this.stat.dev}
	get ino(){return this.stat.ino}
	//get mode(){return this.stat.mode}
	get nlink(){return this.stat.nlink}
	get uid(){return this.stat.uid}
	get gid(){return this.stat.gid}
	get rdev(){return this.stat.rdev}
	get size(){return this.stat.size}
	get blksize(){return this.stat.blksize}
	get bocks(){return this.stat.blocks}
	get atime(){return this.stat.atimeMs/1000}
	get mtime(){return this.stat.mtimeMs/1000}
	get ctime(){return this.stat.ctimeMs/1000}

	get mode(){
		return new FileMode(this.stat.mode)
	}
	set mode(mode){
		let value = mode.value
		console.log('write value', parseInt(String(mode.value), 8))
		fs.chmodSync(this.path, value)
		this._stat = null
	}
	get type(){
		return this.stat.mode & fs.constants.S_IFMT;
	}
	get typename(){
			return TypeNames[this.type]
	}
	
	join(path){
			let newpath = Path.join(this.path, path)
			return new File(newpath)
	}

	chown(user=-1, group=-1){
		return fs.chownSync
	}
	chmod(mode){
			return fs.chmodSync(this.path, mode)
	}
}












exports.File = File
exports.OverWriteError = OverWriteError
exports.FileMode = FileMode

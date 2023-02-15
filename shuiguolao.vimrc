"set autowriteall
if exists('g:shuiguolao_vimrc_loaded')
	echo 'shuiguolao.vimrc can only be loaded once, finish'
	finish
else
	let g:shuiguolao_vimrc_loaded = 1
endif

if !exists('g:shuiguolao_status')
	let g:shuiguolao_status = 1
endif

let g:sgl_suffix_list = ['js', 'py']
let g:sgl_vimrc_path = expand('<sfile>:p')
let g:sgl_root_path = expand('<sfile>:p:h')
"let t:sgl_vm_type = ''

function GetStrSuffix(s)
	let segs = split(a:s, '\.')
	if len(segs) >= 2
		return segs[-1]
	else
		return ''
	endif
endfunction

function OpenTerminal()
	if t:sgl_vm_type == 'py'
		let execute_s = 'python3 -i ' . t:sgl_dir_path.'/terminal.py'
	elseif t:sgl_vm_type == 'js'
		let execute_s = 'nodejs -r ' . t:sgl_dir_path . "/terminal.js"
	endif
	execute 'terminal '. execute_s
endfunction

function SglName2VT(name)
	if a:name == 'jshuiguolao' || a:name == 'jsh' || a:name == 'shuiguolao-js' || a:name == 'js-shuiguolao'
		return 'js'
	elseif a:name == 'pshuiguolao' || a:name == 'psh' || a:name == 'shuiguolao-python' || a:name == 'shuiguolao-py' || a:name == 'py-shuiguolao'
		return 'ps'
	else 
		return ''
	endif
endfunction

function IsSglTab()
	return exists('t:sgl_vm_type') && t:sgl_vm_type != ''
endfunction
"do not use this function when initializing a SGL tab
"when >= 0, it's sgl tab(at least to be intialized)
function TabSglState()
	if g:shuoguolao_status <= 0
		"disabled manually
		return -2
	endif
	if exists('t:sgl_vm_type')
		return t:sgl_vm_type == '' ? 1 : -3
	endif

	if SglName2VT(bufname('%')) != ''
		return 0
	else
		return -1
	else
endfunction



function TryInitSglTab()
	if exists('t:sgl_vm_type')
		return
	endif

	let fname = expand('%')
	if fname == 'jshuiguolao' || fname == 'jsh' || fname == 'shuiguolao-js'
		let vt = 'js'
	elseif fname == 'pshuiguolao' || fname == 'psh'||fname == 'shuiguolao-py' || fname == 'shuiguolao-python'
		let vt = 'py'
	else
		return
	endif
	"echomsg 'fname:'.fname.'>>>vt:'.vt.'<<<<<<<<'
	call InitSglTab(vt)
endfunction

function InitSglTab(vm_type)
	""echomsg 'InitSglTab called with vm_type:'.a:vm_type
	let t:sgl_vm_type = a:vm_type

	let t:main_win_id = win_getid()
	let t:netrw_win_id = -1
	let t:netrw_open_count = 0

	let t:sgl_dir_path = g:sgl_root_path.'/'.a:vm_type
	let t:sgl_entry_path = t:sgl_dir_path.'/shuiguolao.'.a:vm_type
	let t:sgl_sample_path = t:sgl_dir_path.'/sample.'.a:vm_type

	"now we get shebang from entry file
	execute 'e '.t:sgl_entry_path
	let shebang = getline('.')
	"note !! do not mix order of two lines below
	"exit
	let t:sgl_vm_bin = shebang[2:]
	"echomsg 'shebang is '.shebang
	"echomsg 'vm_bin is '.t:sgl_vm_bin

	"map <C-S> :call RunMainWin()
	"call HardMap('<C-S>r', ':call RunMainWin(0,1)')
	"call HardMap('<C-S>R', ':call RunMainWin(1,1)')
	"call HardMap('<C-S>R', ':call RunMainWin_pre()'.':!'.t:sgl_vm_bin.' % ')
	call NewTalk()
endfunction

function HardMap(shortcut, op_s, scope)
	let l = ['map', 'imap']
	
	for m in l
		let scope_s = a:scope ? a:scope : ''
		let exe_s = m.' '. scope_s.' '.a:shortcut.' '.a:op_s
		execute exe_s
	endfor
endfunction


function NewFilePath()
	"let tstamp = localtime()
	let tstamp = strftime("%m-%d %H:%M:%S")
	let fname = tstamp.'.'.t:sgl_vm_type
	let fpath = t:sgl_dir_path.'/history/'.fname
	return fpath
endfunction

"save current file in main window and make another from simple file
function NewTalk()
	let fpath = NewFilePath()
	call win_gotoid(t:main_win_id)
	execute 'update'
	execute 'e '. t:sgl_sample_path
	execute 'w '.fpath
	execute 'e '.fpath

	"now insert create time
	call search('xxxx/xx/xx')
	normal vEEx
	let date_s = strftime('%Y/%m/%d %H:%M:%S')
	execute 'normal i'.date_s
	"normal }j
	"rely on BufEnter perform this action
	"call InitEditScr()
endfunction

"when enter a [.py/.js/..]file buffer under directory 'history', 
"we scroll screen and move cursor to a comfotable position
"necessary useful when press Enter in netrw window.
function InitEditScr()
	"echomsg 'InitEditScr() called on '.expand('%')
	if t:sgl_vm_type == 'py'
		let marker = '###'
	elseif t:sgl_vm_type == 'js'
		"use escape, *** have special meaning in vim
		let marker = '\*\*\*'
	else
		"echomsg 'unknown vm type, InitEditScr silent'
		return
	endif


	"call HardMap('<C-S>r', ':call RunMainWin(0,1)', '<buffer>')
	call HardMap('<C-S>r', ':call RunMainWin(0,1)', '<buffer>')
	"call HardMap('<C-S>R', ':call RunMainWin_pre()'.':!'.t:sgl_vm_bin.' "%" ', '<buffer>')
	call HardMap('<C-S>R', ':call RunMainWin_pre()'.':!shuiguolao "%" ', '<buffer>')
	map <buffer> <C-N> :call UpDown(1)<cr>
	map <buffer> <C-P> :call UpDown(-1)<cr>
	map <buffer> <C-S>N :call NewTalk()
	execute "normal! gg/".marker."shuiguolao\<cr>zt"
	normal }j

	"necessary sometimes
	let syntaxs = {'js':'javascript', 'py':'python'}
	execute 'set syntax='.syntaxs[t:sgl_vm_type]
	execute 'set tabstop=4'
	execute 'set shiftwidth=4'
	"echo 'in history'
endfunction

function TryInitEditScr()
	let bname = bufname('%')
	"echomsg 'try InitEditScr for '.bname

	if !exists('t:sgl_vm_type') || t:sgl_vm_type == ''
		"echomsg 'not valid t:sgl_vm_type, TryInitEditScr() quit..'
		return
	endif


	let parts = split(bname, '/')
	if  len(parts) < 2 || parts[-2] != 'history' 
		"echomsg 'parts too few or not under history/, quit'
		return
	endif
	let suffix = GetStrSuffix(bname)
	if index(g:sgl_suffix_list, suffix) == -1
		"echomsg 'not valid suffix,'.suffix.'quit'
		return
	endif
	call InitEditScr()
	"call OpenHistory()
endfunction


function OpenHistory()
	let netrw_win_nr = Win_ft2nr('netrw')
	if netrw_win_nr == -1
		let g:netrw_sort_by = 'time'
		let g:netrw_list_hide='.*.'.t:sgl_vm_type.'$'
		let g:netrw_hide= 2		"show not-hidden files only
		let g:netrw_browse_split = 4
		let history_path = expand('%:p:h')
		"echo history_path
		execute "Vex".history_path
		let t:netrw_win_id = win_getid()
		execute "vertical resize 14"
		"let g:history_win_on = 1
		"normal r
		if t:netrw_open_count == 0
			"only execute on first time intilization
			"disable banner
			normal I
		endif
		wincmd x
		let t:netrw_open_count += 1
		"echomsg 't:netrw_open_count:'.t:netrw_open_count
	endif
endfunction

function LocateDirItem()
	let l:fname = expand('%:t')
	let l:fname_ = expand('%:r')
	"echo l:fname
	normal <C-W>h
	call search(l:fname_)
endfunction

function HistoryWalk(updown)
	call win_gotoid(t:main_win_id)
	let fname = expand('%:t')
	let netrw_win_nr = Win_ft2nr('netrw')
	let t:netrw_win_id = win_getid(netrw_win_nr)
	call win_gotoid(t:netrw_win_id)
	normal ggj
	execute 'call search("'.fname.'")'
	if a:updown < 0
		let exe_s = 'normal k'
	else
		let exe_s = 'normal j'
	endif
	execute exe_s
	execute 'normal '
endfunction

function ActiveWindowByName(name)
	let l:buf_id = bufnr(a:name)
	let l:win_ids = win_finbuf(l:bufid)
	call win_gotoid(l:win_ids[0])
endfunction


"here g: rather than t: needed, i don't know why.
let g:pe_temp_file_type = ''
function Win_ft2nr(file_type)
	let win_num = winnr('$')
	let nr = 1
	while nr <= win_num
		"echo 'see'.nr
		execute nr.'windo let g:pe_temp_file_type = &ft'
		if g:pe_temp_file_type == a:file_type
			return nr
		endif
		let nr = nr + 1
	endwhile
	return -1
endfunction

function UpDown(dir)
	"execute 'update'
	call OpenHistory()
	call HistoryWalk(a:dir)
endfunction


function RunMainWin_pre()
	call win_gotoid(t:main_win_id)
	execute 'w'
endfunction
"parameter _expand whether expand '%'
function RunMainWin_cmd(sudo, _expand)
	if a:sudo
		let sudo_s = 'sudo'
	else
		let sudo_s = ''
	endif
	if a:_expand
		let name_s = '"' . expand('%') .'"'
	else
		let name_s = '"%"'
	endif
	let cmd =  '!'.sudo_s.' '.t:sgl_vm_bin.' '.name_s
	return cmd
endfunction
"newer function, for newer shebang #!shuiguolao
function RunMainWin_cmd2(sudo, _expand)
	if a:sudo
		let sudo_s = 'sudo'
	else
		let sudo_s = ''
	endif
	if a:_expand
		let name_s = '"' . expand('%') .'"'
	else
		let name_s = '"%"'
	endif
	let cmd =  '!'.sudo_s.' shuiguolao '.name_s
	return cmd
endfunction
function RunMainWin(sudo, _expand)
	call RunMainWin_pre()
	let cmd_s = RunMainWin_cmd2(a:sudo ,a:_expand)
	execute cmd_s	
endfunction


"tabpagenr('$')
"tabc not worked when single tabpage

"restore to current window
function WinDo(cmd_s)
	let currwin=winnr()
	execute 'windo ' . a:cmd_s
	execute currwin . 'wincmd w'
endfunction

function NrWinDo(win_nr, cmd_s, go_back)
	if a:go_back
		let currwin = winnr()
	endif
	let exe_s = a:win_nr.'windo '.a:cmd_s
	"echo exe_s
	execute exe_s
	if a:go_back
		execute currwin . 'wincmd w'
	endif
endfunction

function IdWinDo(win_id, cmd_s, go_back)
	let nr = win_id2win(a:win_id)
	call NrWinDo(nr, a:cmd_s, a:go_back)
endfunction

function HasWin(win_id)
	let has_win = 0
	"TODO
	let g:winid_list = []
	"echo g:main_win_id
	"echo g:winid_list
	"windo call add(g:winid_list, win_getid())
	call WinDo('call add(g:winid_list, win_getid())')
	for nr in g:winid_list
		if nr == a:win_id
			let has_win = 1
			break
		endif
	endfor
	"echo g:winid_list
	return has_win
endfunction


function CloseCurTab()
	if win_getid() == t:main_win_id
		windo q
		"echo 'xxx'
	endif
endfunction

function OnBufEnter()
	call TryInitSglTab()
	call TryInitEditScr()
endfunction

function OnWinEnter()
	if IsSglTab()
		if !HasWin(t:main_win_id)
			windo q					
		endif
	endif
endfunction

function OnWinLeave()
	if IsSglTab() 
		if win_getid() == t:main_win_id
			execute 'update'
		endif
	endif
endfunction

function OnTabNew()
	let g:tabnew_justnow = 1
endfunction
function OnTabEnter()
	if exists('t:sgl_vm_type')
		let g:netrw_list_hide='.*.'.t:sgl_vm_type.'$'
		"echomsg 'enter'.t:sgl_vm_type
	endif
	"handle TabNew event here, for that not works properly in OnTabNew()
	if exists('g:tabnew_justnow') && g:tabnew_justnow
		let g:tabnew_justnow = 0
	endif
endfunction

"disable NERDTree, I don't have other ways
autocmd! NERDTree
autocmd! NERDTreeHijackNetrw

au WinLeave * call OnWinLeave()
au WinEnter * call OnWinEnter()

au BufEnter * call OnBufEnter()
"au TabNew  * call OnTabNew()
au TabEnter  * call OnTabEnter()
"au TabEnter  * call OnTabNew()
cmap <C-A> <HOME>
"TODO this script is sourced or use -S?
call OnBufEnter()
startinsert






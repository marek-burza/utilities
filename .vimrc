" Insert mode by default
autocmd BufNewFile,BufRead * startinsert

" Autosave
autocmd TextChanged,TextChangedI * if &readonly == 0 && filereadable(bufname('%')) | silent write | endif

" Auto text wrapping
set wrap

" Enncoding
set encoding=utf-8

" Show line numbers
set number

" Status bar
set laststatus=2

" Syntax highlighting
syntax on

:imap <C-a>d <Esc>:ex .<CR>
:nmap <C-a>d :ex .<CR>
:imap <C-a>q <Esc>:q!<CR>
:nmap <C-a>q :qa!<CR>
:imap <C-a>t <Esc>:tabnew<CR>
:nmap <C-a>t :tabnew<CR>
:imap <C-a>c <Esc>:tabc<CR>
:nmap <C-a>c :tabc<CR>
:imap <C-a>n <Esc>:tabn<CR>
:nmap <C-a>n :tabn<CR>
:imap <C-a>p <Esc>:tabp<CR>
:nmap <C-a>p :tabp<CR>
:map <C-a>f :echo 'Current time is ' . strftime('%c')<CR>

" Insert mode by default
startinsert

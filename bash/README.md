Bash tips and tricks
====================

`alias`: put a keyword shortcut in your ~/.bash_profile

`cd -` : takes you back to the last directory you were in

`nohup`: no hangup, allows you to log off without killing process

`tmux`: allows you to log off remote computer while running program and re-logon to program from another computer

`ssh-keygen`: login to remote without password

`getent passwd zXXXXXXX`: find out name of person hogging all the server cpu’s

`history`: lists all the commands you’ve given

`ctrl-r`: reverse search autocompletes the line you’re typing by searching through your history

`ctrl-e` and `ctrl-a`: ghetto home and end buttons

`ls –lrth` : list,reverse,time,human readable

`~/.ssh/config`: can put server shortcut names in there to help ssh and rsycn etc.

Tips from Willem
----------------

`&` - Run a program/command in the background. Practically, append when opening a file or program to prevent the terminal from being locked. ie: 'matlab &' opens an interactive session of matlab, but allows you to continue using that shell.

`ctrl+z`, `ctrl+c` - ctrl-z puts a program to sleep and pushes it to the background, ctrl-c closes it. 

`bg`/`fg` - Unlike ctrl-Z, 'bg' will simply move the job to the background without suspending it. To see a list of current jobs (so you don't lose track of ones you've hidden/ suspended), use the 'jobs' command. Similarly, using fg will bring the most recent job back to the foreground. Otherwise, you can use bg and fg with a job number (by running 'jobs') to hide and show specific jobs (ie: bg %n where n is the job number).

`cp -l`  - Instead of copying files from one location to another, cp -l instead creates a symlink to the files you wish to copy. This is useful for modellers as you may be running many different simulations with only minor changes to the configuration of each one. In this instance, creating symlinks in each experiment, linking to (for example) input data files in the master data directory for the model, rather than copying that input data to each experiment can save a *lot* of disk space. Be warned, however, when editing these linked files - they will alter your source file!

use of `>` Prints the result of a shell command to a plain text file. Eg: want to keep track of which files a certain variable in your model appear in? `grep -r variable * > where_is_my_variable` will search for your variable and instead of returning the results in the shell, will print them to a text file.

`du -h | sort -h`   - This command displays the size of the directory (and each one within) in MB and sorts them in ascending order.

`top` or `htop` - Interactively view the processes currently running on the machine/ server you are logged into. To keep track of how much memory/ CPU time you are using, press 'u' then type in your zID and Enter to view only your processes. If you're running memory intensive scripts on the storm servers, I'd recommend always having a window open with top. It gives you process IDs so that if one of your job begins to soak up all the memory, you can kill it before you bring down the server and you incur the wrath of Martin.

`finger` - on that note, if someone is hogging all the CPU time or memory, find their zID in 'top' then use 'finger zID' to identify them in order to send them an angry email

`ls -a` - Can't find your .bashrc ? That's because it's a hidden file. Use the -a flag when you ls to see all hidden files as well.

`cd ~` - go back to the root directory.

Chris Bull's Bash functions
---------------------------

Chris sent in these handy function (or just learn how to make function)

* [*Bash function for painless rsync*](http://christopherbull.com.au/hpc/bash-function-rsync/)
* [*Grabbing paths straight to the clipboard*](http://christopherbull.com.au/hpc/bash-function-clipit/)


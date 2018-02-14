# Setup guide for the Windows Subsystem for linux


As part of Windows 10, Microsoft, in combination with Canonical has begun releasing a full linux subsystem that can be installed.  Out of the box, this system has a few limitations but with a number of smalll tweaks its possible to have a full bash terminal with dual booting or running a VM.  

## Step 1. Installing the Linux subsystem 

The exact method of install varies slightly depending on which version of windows 10 is running.  The system supports ubuntu, Fedora , openSUSE and SLES linux distros.  This guide will focus on ubuntu.

To install the WSL, follow the instructions on:
https://docs.microsoft.com/en-us/windows/wsl/install-win10

Once ubuntu is installed, running and the user account has been setup. its worth making sure its up to date. 

``` bash
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y && sudo apt-get autoremove -y
``` 
THis may take a little while.  

## Step 2. Getting graphical programs working

BY defualt the WSL doesn't ship with an x11 server which means that graphical apps like gedit and ncview will not work. 

This is a simple fix. Xming is an x11 server that can be installed on windows.  it is availabe for download from https://sourceforge.net/projects/xming/  . After installing and running xming, Some people prefer to use VcXsrv rather than xming. Both work the same way.  

Next it is nessary to connect the x11 server to the WSL. 

Right click on xming in the system tray,  select view log, then scroll down to the line that defines the DISPLAY address. It should look something like; 

``` bash
winClipboardProc - DISPLAY=127.0.0.1:0.0
# Note: the numbers adter DISPLAY= can vary from system to system
# in the case of VcXsrv its often DISPLAY=localhost:0.0
```
Next its nessary to add this to the WSL.  This can be done every time bash is run by typing 
``` bash
export DISPLAY=127.0.0.1:0.0
# (replace numbers if nessary)

# For a permanat solution add this export variable to the bashrc. 
nano ~/.bashrc
# or
echo "export DISPLAY=127.0.0.1:0.0" >> ~/.bashrc

# Now we test to make sure its working using the xeyes program
sudo apt-get install x11-apps
xeyes

# Now is a good time to add your normal alias' to the bashrc file
```
This will only work if xming is running before the wsl is opened which is kinda annoying. However, there is an easy fix. Add sming to the programs that launch when windows starts.  The full details are here https://support.microsoft.com/en-au/help/4026268/windows-change-startup-apps-in-windows-10
In simple terms, press the Windows Logo Key  + R, type shell:startup, and then select OK. This opens the Startup folder. Drop and drag the xming icon from the start bar.  

## Fixing the terrible terminal 

The windows bash terminal shoudl now be running a fully featured ubuntu subsystem.  Its now possilbe to install any programing languages and linux packages needed and for them to function properly.  While its completly functional, the windows bash terminal is also horrible. It doesn't support tabs, the copy and paste functionality is barbaric and the defualt color schemes are horrid.  Enter ComEmu.  

ConEmu is a terminal wrapper that can be downloaded from https://conemu.github.io/ . During the install process there is an option for a defualt tab. Chose bash::bash

Now its time to customise =D 
```
# First set up your favorite keyboard shortcuts
Setting > keys & Macro
Set:
paste clipboard contents > Ctrl + Shift + V # same as linux
{bash::bash} > Ctrl + Shift + T # open a new bash tab

Features > Colors 
# Set your favorite colour scheme
# im a big fan of Monokai but each to their own. There are lots of options and they are all customisable 
```

Included in this repo is a script by James Goldie. If you add its contents to the bashrc file its easy to create coloured prompt on any terminal.  


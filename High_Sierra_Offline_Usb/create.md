## Welcome to my TED talk: 
# How to create a High Sierra Usb install pendrive
### that works offline in 2024 (unsing linux)

More than once I get some old mac laptops and iMac to reformat, and is a surprise when you try to update it to the latest version supported, and find out you can't. Yes, sometimes pressing CMD+OPT+R it should install the latest available version, but then why it install Lion, when this is a Macbook8,1 macbook pro late 2011? No idea.

You say, I can install Lion and the update it to High Sierra, ***wrong!!*** You can't contact the Apple update servers, Lion is too old for anything, Opencore is an alternative right? ***wrong!!!*** OpenCore needs macos 10.10 at least. The best option is to have a usb pendrive, do a High-Sierra install and from there you can stay there or go OpenCore.
I tried lots of methods to do a usb pendrive, all of them requires internet, and when you boot from the Macos recovery pendrive, and start the install you'll get the "The recovery sever could not be contacted". 
Does Apple plugged of the recovery server, or did they upgrade it to TLS1.2 and you can't connect to them? No idea, but the only solution is to create your own offline recovery boot live usb. Enough rant, let's go.

### Download the High Sierra files and cook them

You need a linux with hfsplus installed, on Arch you can do that intalling the AUR package ***hfsprogs***[1], for your distribution look how to do it, should be easy.
Download and install ***gibMacos*** (https://github.com/corpnewt/gibMacOS) execute it, it will ask what version to download, just check that the Recovery Option is off and it will download the whole iso (actually it will download several files, the 480Mb recovery.dmg and several others, about 5Gb of files)

What you download with gibMacos are Recovery Images you need to convert those to Full Images, easier way is using MakeInstallMacos (https://github.com/doesprintfwork/MakeInstallmacOS), in there there are two python files, one for windows, and one for Mac (PackAppMacOS.py) that's the one we are using

You can do this your way, my way is:
- Edit the PackAppMacOS.py en comment the line 173:
  ```
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  change to
  # os.chdir(os.path.dirname(os.path.realpath(__file__)))
  ```
- go into the folder where gibMacos.py downloaded the whole iso and call the python PackAppMacOS.py from there(in my case is)
```
 cd ~/gibMacOS/macOS Downloads/publicrelease/041-90855 - 10.13.5 Install macOS High Sierra Beta (17F66a)/
 python ~/MakeInstallmacOS/PackAppMacOS.py
```
It will ask what to do, just press P, pack. That convert the downloaded files into full install files, and will copy them into a folder called ***SharedSupport*** .

While in there, you have to extract the 4.hfs file, that is the install program for the online recovery, that file is inside BaseSystem.dmg, we can extract it using dmg2img tool:
```
dmg2img -v -i BaseSystem.dmg -p 4 -o 4.hfs
```

### Prepare the pendrive
Now 

[1] https://aur.archlinux.org/packages/hfsprogs

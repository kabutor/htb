## Welcome to my TED talk: 
# How to create a High Sierra Usb install pendrive
### that works offline in 2024 (using linux)

More than once I get some old mac laptops and iMac to reformat, and is a surprise when you try to update it to the latest version supported, and find out you can't. Yes, sometimes pressing CMD+OPT+R it should install the latest available version, but then why it install Lion, when this is a Macbook8,1 macbook pro late 2011? No idea.

You say, I can install Lion and the update it to High Sierra, ***wrong!!*** ***The Recovery Server Could Not Be Contacted***, Lion is too old for anything, Opencore is an alternative right? ***wrong!!!*** OpenCore needs macos 10.10 at least. The best option is to have a usb pendrive, do a High-Sierra install and from there you can stay there or go OpenCore.
I tried lots of methods to do a usb pendrive, all of them requires internet, and when you boot from the Macos recovery pendrive, and start the install you'll get the "The recovery sever could not be contacted". 
Does Apple plugged of the recovery server, or did they upgrade it to TLS1.2 and you can't connect to them? [2] No idea, but the only solution is to create your own offline recovery boot live usb. Enough rant, let's go.

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
Prepare the pendrive, I'm not going into a lot of detail on how to do it, and I'm gonna use the device names below as a reference, use the ones of your pendrive, use fdisk, gdisk or gparted, we need to set it as GPT, with the following partitions:

1 - (/dev/sdb1) 200M partition ***EF00 EFI System***

2 - a 129M gap with nothing in it (I'm not 100% sure if this is needed, but I read that it is, I did it using gdisk, when you set to create a new partition it asks for the First sector of the second partition, you can type +129M and that will leave the gap)

3- (/dev/sdb2) a partition to hold all the files, about 8.5GB should be enough ***AF00 Apple HFS/HFS+*** (I also read that you need to leave a gap at the end of 129M, but if the pendrive is big, just do the 8.5Gb partition and can leave the rest empty)

Format and mount as hfsplus sdb2 on ***/mnt/pen*** mount the 4.hfs as a loop unit on ***/mnt/origin***
```
mkfs.hfsplus -v "macOS Base System" /dev/sdb2
mount -t hfsplus /dev/sdb2 /mnt/pen
mount -o loop -t hfsplus 4.hfs /mnt/origin
```
Now copy all inside the mounted 4.hfs into the pendrive
```
rsync -avxHEWz --numeric-ids --info=progress2 /mnt/origin /mnt/pen
```
Once it finish, go where you have the ***SharedSupport*** folder (the one that MakeInstallMacOS created) and move the folder with all it's contents into /mnt/pen/Install macOS High Sierra.app/Contents , you have to end with a Content/SharedSupport folder in there with all the dmg files.

### Make it bootable
Format the sdb1 partition as fat32, download Clover from sf (https://sourceforge.net/projects/cloverefiboot/files/latest/download).
Uncompress the downloaded file, open the clover iso file and move the contents of the EFI folder to /dev/sdb1 (you have to end with a BOOT and a CLOVER folder on the root of sdb1)

That's it, unmount the partitions and try it, this I manage to make it work, in 2024 :)


[1] https://aur.archlinux.org/packages/hfsprogs

[2] After posting this I came into this link that explain why it's giving such error (certificate or tls1.2 error) (https://mrmacintosh.com/how-to-fix-the-recovery-server-could-not-be-contacted-error-high-sierra-recovery-is-still-online-but-broken/)

```
nvram IASUCatalogURL="http://swscan.apple.com/content/catalogs/others/index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog"
```

[You find this useful in any way and want to thank me, you can do so with a coffee, thanks](https://www.buymeacoffee.com/kabutor)

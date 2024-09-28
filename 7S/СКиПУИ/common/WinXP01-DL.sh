#!/bin/bash
NAME="WinXP01-DL"
DISK="/VDisk/DL/WinXP01-DL.vdi"
RAM="512"
VRAM="32"
OS="WindowsXP"
HUUID="1f071410-d7f3-4c9c-acb3-0ef19fd86c07"
NETNAME="intnet"
STRNAME="IDE"
_AUDIO="none"
_ACPI="on"
_IOAPIC="on"
_PAE="on"
_HWVIRTEX="on"
_VTXVPID="on"
_CHIPSET="PIIX3"
_NIC="intnet"
_NICTYPE="Am79C973"
_USB="off"
_CONTROLLER="PIIX4"
_MTYPE="immutable"
#SHAREPATH="/home/user/share"

#main
vboxmanage createvm --name "$NAME" --ostype $OS --register 
vboxmanage modifyvm "$NAME" --memory $RAM --vram $VRAM --acpi $_ACPI --ioapic $_IOAPIC --pae $_PAE --chipset $_CHIPSET --hwvirtex $_HWVIRTEX --vtxvpid $_VTXVPID
#network 
vboxmanage modifyvm "$NAME" --nic1 $_NIC --nictype1 $_NICTYPE --intnet1 "$NETNAME"
#other
vboxmanage modifyvm "$NAME" --audio $_AUDIO --usb $_USB

#storage
vboxmanage storagectl "$NAME" --name "$STRNAME" --add ide --controller $_CONTROLLER
vboxmanage storageattach "$NAME" --storagectl "$STRNAME" --port 0 --device 0 --type hdd --medium "$DISK" --mtype $_MTYPE

vboxmanage storageattach "$NAME" --storagectl "$STRNAME" --port 0 --device 1 --type dvddrive --medium emptydrive

##share
#vboxmanage sharedfolder add "$NAME" --name share --hostpath $SHAREPATH

vboxmanage modifyvm "$NAME" --clipboard bidirectional
vboxmanage modifyvm "$NAME" --usb on --usbehci on

---
layout: post
title: How to mount samba with mount bind in large file systems
categories: tech
published: false
date: 2017-02-10
---

1. Su ThinkCenter (che fa da lato server) installato samba lato server, configurato per fare share della cartella ~/DATA con queste opzioni:

[DATA]
path = /home/demetrio/DATA
valid users = demetrio
writeable = yes 
browseable = yes 
read only = no
client lanman auth = yes

La cartella DATA è a sua volta un bind-mount fatto come:

	mkdir ~/DATA
	sudo mount -o bind /media/demetrio/Seagate\ Backup\ Plus\ Drive/Demetrio/ DATA

Il mount bind NON copia niente. Per smontarlo:
	
	sudo umount -l ~/DATA

2. Lato client (server 15) modificato /etc/fstab con la stringa

	//10.216.22.142/DATA /mnt/DEMETRIOHDD cifs username=demetrio,domain=WORKGROUP,noauto,rw,users 0 0

facendo così permetto all'utente non root di montare questa share.

Poi:

	sudo umount -a

3. Sul server 15 con utente nonroot, posso fare:

	mount.cifs //10.216.22.142/DATA /mnt/DEMETRIOHDD/




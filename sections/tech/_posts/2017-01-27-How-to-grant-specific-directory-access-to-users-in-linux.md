# Negative ACLs

You can prevent a user from accessing certain parts of the filesystem by setting access control lists. For example, to ensure that the user abcd cannot access any file under /home:

    setfacl -m user:abcd:0 /home

This approach is simple, but you must remember to block access to everything that you don't want abcd to be able to access.

# Chroot

To get positive control over what abcd can see, set up a chroot, i.e. restrict the user to a subtree of the filesystem.

You need to make all the files that the user needs (e.g. mysql and all its dependencies, if you want the user to be able to run mysql) under the chroot. Say the path to the chroot is /home/restricted/abcd; the mysql program needs to be available under /home/restricted/abcd. A symbolic link pointing outside the chroot is no good because symbolic link lookup is affected by the chroot jail. Under Linux, you can make good use of bind mounts:

    mount --rbind /bin /home/restricted/abcd/bin
    mount --rbind /dev /home/restricted/abcd/dev
    mount --rbind /etc /home/restricted/abcd/dev
    mount --rbind /lib /home/restricted/abcd/lib
    mount --rbind /proc /home/restricted/abcd/proc
    mount --rbind /sbin /home/restricted/abcd/sbin
    mount --rbind /sys /home/restricted/abcd/sys
    mount --rbind /usr /home/restricted/abcd/usr

You can also copy files (but then you'll need to take care that they're up to date).

To restrict the user to the chroot, add a ChrootDirectory directive to /etc/sshd_config.

    Match User abcd
        ChrootDirectory /home/restricted/abcd


I've found that the negative way is the most secure.


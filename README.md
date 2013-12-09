trukbot2
========

Twitch.tv chat bot work in process

After cloning or downloading make sure to edit channels.txt and botconfig.cfg

How commands work
-----------------

You add your channels to channel.txt. After this you must create three seperate files for each channel you have added (I'll make the creation of stuff automatic at some point, but right now you have to deal with this.). Each file must be named "#channelname.commands.json" "#channelname.execs.json" and "#channelname.triggers.json". These files are all written in json, I have included three example files on how it should look. You should be able to copy these, rename them and edit them to add your own commands.

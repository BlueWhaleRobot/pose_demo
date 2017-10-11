# pose_demo
Get pose of all robots in local network running Galileo navigation system

获取当前局域网内的所有机器人的位置信息并显示出来。
每台机器人人会在局域网通过UDP广播自己配置信息，包括自己的ID和各种服务端口。
程序获取到每个机器人的信息后，通过http请求，获取到每个机器人的位置。

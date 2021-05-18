# 纯真 IP 库自动更新
1. QQwryupdate 更新
![87OlQa16213074591621307459456nbeKuc](https://ops-1254326415.file.myqcloud.com/uPic/87OlQa16213074591621307459456nbeKuc.png)

2. wireshark 包过滤规则
```
http.request.method == 'GET' and http.host == 'update.cz88.net'
```

3. 下载规则
![RBOmLo16213075921621307592582PpllAi](https://ops-1254326415.file.myqcloud.com/uPic/RBOmLo16213075921621307592582PpllAi.png)
抓包发现了两个请求 /ip/copywrite.rar 和 /ip/qqwry.rar；copy 其中的 http request 头信息，Accept: text/html, */* 和 User-Agent: Mozilla/3.0 (compatible; Indy Library)，至于为什么要记录这两个头，使用浏览器打开这两个链接就知道了，是没有办法直接打开的，我们需要模拟它的桌面端，发起请求。

文件的结构如下：当我们使用上述的方式将 copywrite.rar 和 qqwry.rar 下载下来之后，怎么变成 qqwry.dat 呢？以 rar 结尾的，但并不是 rar 文件。

结构图如下：
![Pz3zmL16213076231621307623734LagrTK](https://ops-1254326415.file.myqcloud.com/uPic/Pz3zmL16213076231621307623734LagrTK.png)

qqwry.rar 的前 512(0x200) 个字节，需要用到 copywrite.rar 中的 key 进行解密。

4.代码入 [QQwryUpdater.py](./QQwryUpdater.py)
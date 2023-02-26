<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<!-- ABOUT THE PROJECT -->
## About The Project
水果捞
一个开箱即用的脚本书写和运行环境，一组有趣的库。
在这里，你可以用程序语言与操作系统交互，类似orm的方式与操作系统交互，

###Example
see `guide` in document page: [https://lovelyshell.github.io/](https://lovelyshell.github.io/)

### Prerequisites

* vim 
* python 3.6+ | nodejs

### Install
Download and unzip(or git clone) this repo to `WHERE` you like, then run command:
   ```sh
   sudo chmod 777 WHERE/shuiguolao/shuiguolao.bash
   sudo ln -s WHERE/shuiguolao/shuiguolao.bash /usr/bin/shuiguolao
   ```

### Usage
1. Edit Mode
Type `shuiguolao` in command line, you will get a vim window to write script, press `ctrl-s r` to run, and press `:q` quit.

2. Interactive Mode
   ```bash
   shuiguolao -i
   ```

3. specify the script language 
   ```bash
   shuiguolao --python
   shuiguolao --js
   ```
(currently only python,js supported)

4. use its library in xonsh
   ```python
   import sys
   sys.path.append('WHERE/shuiguolao/py/lib/') 
   from preload import *
   ```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

<!-- LICENSE -->
## License

Distributed under the GPL-v3 License. See `LICENSE` for more information.




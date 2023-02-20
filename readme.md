<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<!-- ABOUT THE PROJECT -->
## About The Project
linux上的好多问题，不单单是文本文件和语法的问题，而是设计的问题。用户需要知道自己在干什么。

1. 通常在shell解决问题吃力时，我们会切换到一门脚本语言来实现，但切换的劳动量会让我们迟疑。要新建文件，要给文件命名，选择放在哪个目录，写shebang，import基本的库，最后还要chmod 777. 
2. 所以shuiguolao典型的使用场景是，当在命令行遇到麻烦，输入shuiguolao，进入一个配置好的代码书写环境，你可以使用你熟悉的语言来解决问题，完成后按:q退回到命令行模式。
3. 通用脚本替代shell语言作为胶水后，紧接着面临的的问题是，通用脚本的库并不是为支持shell级别的编程而设计的，shell级别的编程任务通常是一些小的，临时的，性能不相干的, 相较性能和精细度，我们更注重易用性和清晰度。
4. 有了这个入口，也许我们能在改变linux的生态上有所作为。

而使用者又急急忙忙。在python里读入一个文件至少需要with open和read，加之其中的参数，此种细节不一而足都是心智负担。我们需要一些更高级的抽象来帮助我们快速的书写代码。这个抽象主要是数据结构的建立，通过把我们常见的操作对象的底层模型，反应到脚本代码的数据结构上。所以shuiguolao面向的用户是程序员，而不像bash面对更广泛的用户。

2. 脚本编程替代命令行存在一个
所以这套程序解决的第一个问题是，降低从命令行切换到脚本编程的门槛。因为它意味着
脚本编程替代命令行的第一个问题，是需要新建文件()
shell编程面临的两个问题，一个是门槛问题，当我们要解决的任务不大不小，使用脚本
所以shuiguolao由两部分构成，这两部分分别解决脚本编程
主要由两部分构成，一部分是

shuiguolao提供一个开箱即用的脚本编程环境，来支持你在命令行遇到麻烦时，能快速的切换到自己喜欢的语言来解决问题。
当你在命令行遇到麻烦时，可以输入shuiguolao


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* python 3.6+
* vim 

### Installation

Download and unzip(or git clone) this repo to `WHERE` you like, then run command:
   ```sh
   sudo chmod 777 WHERE/shuiguolao/shuiguolao
   sudo ln -s WHERE/shuiguolao/shuiguolao.bash /usr/bin/shuiguolao
   ```

shuiguolao need 

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL-v3 License. See `LICENSE` for more information.

# Build4s - A build tool for simple, standard, stable and stupid

## About
受启发于AWS CodeBuild的自动化编译打包服务，抽取其中标准化编译打包功能实现的一个本地组件。[AWS CodeBuild User Guide](https://docs.aws.amazon.com/zh_cn/codebuild/latest/userguide/welcome.html)
- Build提供了标准化的编译打包流程，可编译源代码，运行单元测试，并生成可供部署的项目。   
- Build提供了适用于最热门编程语言的预配置构建环境，只需配置简单的构建脚本就可以。   

## Requirements
- Python
- PyYAML

## Install
下载最新的Release包，通过pip命令安装：
```shell
pip install build4s
```
或者通过下载源码包或clone代码至本地，然后通过如下命令安装：
```shell
python setup.py install
```

## Usage
```shell
buildcli --spec-file=buildspec.yml --target-file=target.zip
```
使用--help查看更多使用帮助。  
--spec-file参数指定编译时使用的标准化流程文件，若为空则默认为buildspec.yml。
--target-file参数指定打包生成的压缩包文件，若为空则默认为target.zip。

## Release
- [build4s-0.0.1.zip](https://github.com/meanstrong/build4s/releases/download/v0.0.1/build4s-0.0.1.zip)

## Example
一个示例的buildspec.yml文件如下所示：
```yaml
version: 0.2
env:
  variables:
    JAVA_HOME: "/usr/lib/jvm/java-8-openjdk-amd64"

phases:
  install:
    commands:
      - echo Entered the install phase...
  pre_build:
    commands:
      - echo Entered the pre_build phase...
  build:
    commands:
      - echo Entered the build phase...
      - mvn clean package -e -Dmaven.test.skip=true
  post_build:
    commands:
      - echo Entered the post_build phase...
artifacts:
  files:
    - example.jar
    - classes/config/*
  discard-paths: no
  base-directory: target
```
将该文件置于源代码目录，在该目录下执行如下命令，即会在当前目录下生成target.zip文件。   
与自动化部署服务[Deploy4s](https://github.com/meanstrong/deploy)配合使用，效果更佳，味道更佳。
```shell
buildcli --target-file=target.zip
```

## Author
- <a href="mailto:pmq2008@gmail.com">Rocky Peng</a>

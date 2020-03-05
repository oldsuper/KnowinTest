#!/bin/bash -e
WorkUser=jenkins
TargetHostPath=/home/${WorkUser}
source ~/.bash_profile
ENV=dev
# 打包
## 检查编译环境
java -version
# NPM=`which npm`

## 获取版本号
VersionSeed=`git status | head -1 | awk '{print $NF}'`
FullVersion=1.0.${VersionSeed}
echo "FullVersion: ${FullVersion}"
## 创建打包文件备份路径
mkdir -p ${backupPath}/${projectName}/${subProjectName}
## 开始打包
packageName=${subProjectName}_${FullVersion}.tar.gz
StorePackagePath=${backupPath}/${projectName}/${subProjectName}/${packageName}
cd ${WORKSPACE}
pwd
echo "###### show WORKSPACE #####"
ls
## build begin
echo "####### begin build #######"
# cd ${subPackageName}
# $NPM install --registry=https://registry.npm.taobao.org 
gradle services:nlu:shadowJar

echo "####### build  done #######"
## build done
# cd ..

Command="tar zcvf ${backupPath}/${projectName}/${subProjectName}/${packageName} services/nlu/build sh"
echo "${Command}"
${Command}

# 启动服务
Timestamp=`date +%s`
ProjectWorkPath=${TargetHostPath}/workspace/${subProjectName}
JarPath=${ProjectWorkPath}/services/nlu/build/libs/nlu-0.1-all.jar
# LogfilePath=/data/incafe/server/log.file
ShfilePath=${ProjectWorkPath}/sh/restart-service.sh
PackageStorePath=${TargetHostPath}/data/package
WorkfolderBackupPath=${TargetHostPath}/data/backup/${projectName}/${subProjectName}

## 准备目录
ssh ${WorkUser}@${targetHost} "mkdir -p ${WorkfolderBackupPath} ${PackageStorePath}"

scp ${StorePackagePath} ${WorkUser}@${targetHost}:${PackageStorePath}

set +e
## 打包备份原工作目录并删除
echo "tar zcvf ${WorkfolderBackupPath}/${Timestamp}.tar.gz ${ProjectWorkPath} --remove-files"
ssh ${WorkUser}@${targetHost} "tar zcvf ${WorkfolderBackupPath}/${Timestamp}.tar.gz ${ProjectWorkPath} --remove-files"
set -e
## 拷贝文件过去
scp ${backupPath}/${projectName}/${subProjectName}/${packageName} ${WorkUser}@${targetHost}:${PackageStorePath}

## 解压到工作目录并启动服务
Command="source ~/.bash_profile; mkdir -p ${ProjectWorkPath};tar xvf ${PackageStorePath}/${packageName} -C ${ProjectWorkPath}; sh ${ShfilePath} ${JarPath} ${ENV}"
echo "${Command}"
ssh ${WorkUser}@${targetHost} "${Command}"
#if [ 0 = $DONE ]; then
#	echo 'OK'
#else
#	echo 'Fail'
#fi
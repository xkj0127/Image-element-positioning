
# python示例，修改完代码后使用这个开启
python funasr_wss_client.py --host "127.0.0.1" --port 10096 --mode 2pass --ssl 0

python funasr_qwen2_tools.py --host "127.0.0.1" --port 10096 --mode offline --ssl 0
使用offline，不需要判断句子风格，会自动用最后的结果

python funasr_wss_client.py --host "127.0.0.1" --port 10096 --mode offline --audio_in "D:/EdgeDownload/100.wav" --ssl 0
可以离线处理音频文件，格式是wav


docker pull registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.10 

本地电脑： mkdir -p ./funasr-runtime-resources/models  

docker save -o funasr.tar 1c2adfcff84df11cac2f5c20aa4bc62c521fa7f269f5e44848fd55cc973023b1

docker tag 1c2adfcff84df11cac2f5c20aa4bc62c521fa7f269f5e44848fd55cc973023b1 funasr_cpu:funasr_diy

docker run -p 10096:10095 -itd --privileged=true -v D:/PycharmProjects/Image-element-positioning/funasr-runtime-resources/models:/workspace/models funasr_cpu:funasr_diy


# 启动服务
docker attach f99d74b72307c69bc4233400fa8aebcd422e8bdbaf686c33dbb981b5134fe7ba

bash run_server_2pass.sh

ws://127.0.0.1:10096/

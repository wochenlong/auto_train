# auto_train
风吟关于一键炼丹的各种好用小工具

画师标签与角色特征处理依赖于此项目：https://github.com/shiertier/xl_train_json2tag

# sdeval的使用
## 依赖安装
```
pip install collections  # 不需要单独安装，collections是Python标准库的一部分
pip install tags         # 假设tags是一个第三方库
pip install webuiapi
pip install tqdm
pip install pandas
pip install sdeval       # 这个应该包含了fidelity, controllability, corrupt子模块
```
## 运行sdeval
```
python  eval_lora.py
```

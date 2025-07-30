import re
import numpy as np

# 提取频率信息的函数
def get_frequency(outcar):
    # 正则表达式匹配模式
    pattern = r"^\s+[\d]+\s+f+\s+=\s+([\d\-\.]+)\sTHz+\s+([\d\-\.]+)\s2PiTHz+\s+([\d\-\.]+)\s+cm-1+\s+([\d\-\.]+)+\smeV"
    data = []
    try:
        # 读取 OUTCAR 文件
        with open(outcar, 'r') as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                match = re.match(pattern, line)
                if match:
                    # 提取匹配到的振动频率数据并转换为浮点数
                    freq_data = [float(i) for i in match.groups()]
                    # 添加振动模式索引，如 '1 f', '2 f'
                    freq_data.append(f'{index + 1} f')
                    data.append(freq_data)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{outcar}' was not found.")
        return []

# 主程序逻辑
def main():
    outcar_file = 'OUTCAR'  # OUTCAR 文件路径
    dd = get_frequency(outcar_file)

    if not dd:
        print("No frequency data extracted. Exiting program.")
        return

    # 提取振动频率，转换为 eV
    f_list = [d[3] / 1000 for d in dd]  # 使用 cm⁻¹ 的列数据（第 4 列）

    # 常量定义
    Kb = 8.6173324E-5  # 玻尔兹曼常数，单位：eV/K
    T = 1300  # 温度，单位：K

    D, S, C = [], [], []

    # 计算无量纲参数、熵、内能
    for e in f_list:
        d = e / (Kb * T)  # 无量纲参数
        D.append(d)
        s = (d / (np.exp(d) - 1)) - np.log(1 - np.exp(-d))  # 熵公式
        S.append(s * Kb)  # 乘以玻尔兹曼常数
        c = e / (np.exp(d) - 1)  # 内能公式
        C.append(c)

    # 计算热力学量
    entropy = sum(S)  # 总熵
    TS = T * entropy  # T*S
    ZPE = 0.5 * sum(f_list)  # 零点能
    U = sum(C)  # 内能
    F_vib = ZPE + U - TS  # 振动自由能

    # 输出结果
    print("ZPE =", ZPE, "eV")
    print("TS =", TS, "eV")
    print("U =", U, "eV")
    print("F_vib = ZPE + U - TS =", F_vib, "eV")

# 程序入口
if __name__ == "__main__":
    main()


import time
import subprocess
import cv2
import azizitc as tc
import os
import sys

a = None
def get_screen_info():
    # 获取屏幕分辨率
    size_result = subprocess.run([f"{adbhome_path}", "shell", "wm", "size"], capture_output=True, text=True)
    resolution = size_result.stdout.strip().split()[-1]

    # 获取屏幕DPI
    density_result = subprocess.run([f"{adbhome_path}", "shell", "wm", "density"], capture_output=True, text=True)
    dpi = density_result.stdout.strip().split()[-1]

    print(tc.t.green("[INFO] ")+tc.t.yellow("获取到屏幕分辨率：")+f" {resolution} "+tc.t.yellow("DPI:")+f" {dpi}")
    return resolution, dpi


def get_screenshot(save_path="./temp/screenshot.png"):
    # 获取屏幕截图并保存
    with open(save_path, "wb") as f:
        subprocess.run([f"{adbhome_path}", "exec-out", "screencap", "-p"], stdout=f)
    return save_path


def find_image_on_screen(template_path, screenshot_path, threshold=0.8):
    # 读取截图和模板图片
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    # 模板匹配
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(tc.t.green("[INFO] ")+tc.t.blue(f"在屏幕坐标 {max_loc} 找到了符合的按钮"))
        return max_loc
    else:
        return None


def tap_screen(x, y):
    # 使用 adb shell input tap 点击
    subprocess.run([f"{adbhome_path}", "shell", "input", "tap", str(x), str(y)])
    print(tc.t.green("[INFO] ")+tc.t.blue(f"模拟点击屏幕坐标： ({x}, {y})"))

def use(cai):
    a = 0
    # 步骤 1: 获取屏幕信息
    a = 1
    try:
        while a == 1:
            screenshot_path = get_screenshot()
            template_path = "./ku/guo.jpg"
            match_location = find_image_on_screen(template_path, screenshot_path)
            if match_location:
                x, y = match_location
                tap_screen(x, y)
                time.sleep(1)
                a = 2
            else:
                print(tc.t.yellow("[ERROR] ")+tc.t.red("没在屏幕中找到有效的锅。"))
                a=0
        while a == 2:
            screenshot_path = get_screenshot()
            template_path = f"./ku/{cai}.jpg"
            match_location = find_image_on_screen(template_path, screenshot_path)
            if match_location:
                x, y = match_location
                tap_screen(x, y)
                time.sleep(1)
                a = 3
            else:
                print(tc.t.yellow("[ERROR] ")+tc.t.red("没在屏幕中找到有效的菜品。"))
                a=0
        while a == 3:
            screenshot_path = get_screenshot()
            template_path = "./ku/kaishi.jpg"
            match_location = find_image_on_screen(template_path, screenshot_path)
            if match_location:
                x, y = match_location
                tap_screen(x, y)
                print(tc.t.green("[INFO] 自动寻找铲子并点击中..."))
                a = 4
            else:
                print(tc.t.yellow("[ERROR] ")+tc.t.red("没在屏幕中找到有效的开始按钮。"))
                a=0
        while a == 4:
            b =False
            screenshot_path = get_screenshot()
            template_path = "./ku/cz.jpg"
            template_path2 = "./ku/shoutao.jpg"
            match_location = find_image_on_screen(template_path, screenshot_path)
            match_location2 = find_image_on_screen(template_path2, screenshot_path)
            if match_location:
                x, y = match_location
                tap_screen(x, y)
            if match_location2:
                x, y = match_location2
                tap_screen(x, y)
                print(tc.t.green("[INFO] 恭喜你完成了菜品的制作。"))
                a = 0
                time.sleep(2)
            else:
                a=4
    except KeyboardInterrupt:
        print(tc.t.yellow("[ERROR] ") + tc.t.red("程序被用户中断。"))
        exit()

def monitor_adb():
    print(tc.t.green("[INFO] ") + tc.t.blue("请接入 ADB 设备...(模拟器/手机打开ADB功能)"))

    while True:
        # 使用 subprocess 调用 adb devices 命令来获取连接的设备
        result = subprocess.run([f"{adbhome_path}", "devices"], capture_output=True, text=True)
        # 解析设备列表
        devices = result.stdout.strip().splitlines()[1:]  # 第一行是 "List of devices attached"，跳过

        # 如果检测到设备
        if devices:
            print(tc.t.green("[INFO] ") + tc.t.yellow("检测到设备接入："), devices[0].split()[0])  # 获取设备ID
            get_screen_info()  # 获取屏幕信息
            xd_adb()  # 检查应用进程
            break

        time.sleep(2)
def xd_adb():
#     使用adb shell ps | findstr com.xd.xdt获取进程是否启动，如果没任何结果就是没有启动
    print(tc.t.green("[INFO] ")+tc.t.blue("请启动心动小镇..."))
    while True:
        try:
            result = subprocess.run([f"{adbhome_path}", "shell", "ps"], capture_output=True, text=True)
            # 检查输出中是否包含com.xd.xdt
            if 'com.xd.xdt' in result.stdout:
                result = subprocess.run([f"{adbhome_path}","shell","pidof","com.xd.xdt"],capture_output=True,text=True)
                print(tc.t.green("[INFO] ")+tc.t.yellow(f"心动小镇已启动 PID:{result.stdout.replace("\n","")}"))
                break
        except KeyboardInterrupt:
            print(tc.t.yellow("[ERROR] ")+tc.t.red("程序被用户中断。"))
            exit()
def welcome():
    print(tc.t.yellow("===== 心动小镇厨神辅助 ====="))
    print(tc.t.yellow("版本:V2.1"))
    print(tc.t.yellow("适配：安卓(开启ADB) 模拟器"))
    monitor_adb()
    print(tc.t.green("[INFO] 请将灶台减少至1个并输入菜肴"))
    # print(tc.t.green("1、蓝莓果酱"))
    # print(tc.t.green("2、树莓果酱"))
    try:
        useinput = input(tc.t.green("[INFO] ")+tc.t.yellow("请输入菜肴首字母缩写："))
    except KeyboardInterrupt:
        print(tc.t.yellow("\n[ERROR] ")+tc.t.red("程序被用户中断。"))
        exit()
    while True:
        use(useinput)
def one():
    print(tc.t.green("系统环境自检测与自修复正在运行中..."))
    if getattr(sys, 'frozen', False):
        # 如果程序被打包成了单个文件
        mainpath = sys._MEIPASS
    else:
        # 否则，程序仍然是原始的 .py 文件
        mainpath = os.path.dirname(os.path.abspath(__file__))

    # 特定的路径
    specific_path = f"{mainpath}\\bin"
    global adbhome_path
    adbhome_path = f"{mainpath}\\bin\\adb.exe"

    # 获取Path环境变量
    path_variable = os.environ.get('PATH')

    if path_variable:
        # 将Path环境变量分割成多个路径
        paths = path_variable.split(';')  # Windows系统使用分号分隔路径
        # 检查特定的路径是否在列表中
        if specific_path in paths:
            # print(tc.t.green(f"'{specific_path}' 存在于Path环境变量中。"))
            print(tc.t.blue("系统自检完毕。"))
            welcome()
        else:
            # print(tc.t.red(f"'{specific_path}' 不存在于Path环境变量中。"))
            # 将path_variable写入Path环境变量
            os.environ['PATH'] = path_variable + ';' + specific_path
            # print(tc.t.green(f"'{specific_path}' 已临时添加到环境变量中。"))
            # print(tc.t.bg_red(tc.t.white(f"建议将'{specific_path}'加入系统Path中")))
            print(tc.t.blue("系统自检完毕。"))
            welcome()
    else:
        print("Path环境变量未设置。")


if __name__ == "__main__":
    one()

import os
import shutil
import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("Twitter Downloader로 다운로드한 파일이 포함된 폴더를 선택하세요.")

file_frame = Frame(root)
file_frame.pack(fill="x", padx = 5, pady = 5)

root.geometry("600x50")    # 가로x세로 사이즈
root.resizable(False, False)

dir_path = None
file_list = []

def folder_select():
    dir_path = filedialog.askdirectory(initialdir="/", title="폴더를 선택하세요")

    if dir_path == '':
        messagebox.showwarning("경고", "폴더를 선택하세요")
    else:
        res = os.listdir(dir_path)  # 선택한 전체 경로 이름

        if len(res) == 0:
            messagebox.showwarning("경고", "폴더를 선택하세요")
        else:
            for file in res:
                old_file = os.path.join(dir_path, file)                 # 원본 파일의 경로명/파일명 (전체 경로\\twitterid-1689000333853212672-20230809_044714-img1.jpg)
                new_filename = file.split(sep='-', maxsplit=2)          # 하이픈 2개까지만 문자열 나눔
                if len(new_filename) != 3:                              # new_filename의 길이가 3이 아니면 break
                    continue
                
                new_file = os.path.join(dir_path, new_filename[-1])     # "날짜_시간-접미사"만 남기도록 파일명 변경 (전체 경로\\20230809_044714-img1.jpg)
                if not os.path.exists('@' + new_filename[0]):           # 계정 이름으로 된 폴더 생성하기 (전체 경로\\@twitterid 폴더 생성)
                    os.makedirs('@' + new_filename[0])

                index = 1
                file_list = os.listdir(dir_path + '\\' + '@' + new_filename[0])
                for inner_file in file_list:
                    pure_new_file = new_file.split(sep='/')[-1].split(sep='\\')[-1]
                    pattern = '[0-9]*_[0-9]*-[a-z]*'
                    index = int(re.split(pattern, pure_new_file)[1].split(sep='.')[0])

                    # 파일명이 중복하면 index 값을 증가시킴
                    if pure_new_file == inner_file:
                        match = re.search(r'(\d+)(\.(jpg|mp4))$', new_file)
                        if match:
                            index = index + 1
                            extension = match.group(2)
                            new_file = re.sub(r'(\d+)(\.(jpg|mp4))$', str(index) + extension, new_file)

                os.rename(old_file, new_file)                           # 파일명 변경
                shutil.move(new_file, '@' + new_filename[0])            # 생성한 폴더 안으로 파일 이동

btn_active_dir = Button(file_frame, text ="폴더 선택", width = 12, padx = 5, pady= 5, command=folder_select)
btn_active_dir.pack(padx = 5, pady= 5)

root.mainloop()

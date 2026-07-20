import tkinter as tk
from tkinter import messagebox
import random
from DATa import database 
class MoodHD:
    def __init__(self, root):
        self.root = root
        self.is_placeholder = True#标状态
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("勇敢谈谈现在你的感受")
        self.root.geometry("1000x618")
        self.root.configure(bg="LightSteelBlue")
        self.root.resizable(False, False)
        tk.Label(
            self.root, 
            text="Write down 此刻你的feelings:",
            font=("Microsoft YaHei", 25, "bold"), 
            bg="LightSteelBlue", 
            fg="Black"
        ).pack(pady=(30, 10))
        #调页面，背景颜色，字体，以及标题

        self.input_field = tk.Entry(
            self.root, 
            width=40, 
            font=("Arial", 11),
            fg='grey'#设置打字框的初始布局
        )
        self.input_field.insert(0, "点击输入... 你现在还好嘛")#打字框里面的字

        self.input_field.bind('<FocusIn>', self.clear_placeholder)#清初始字，让人可以打
        self.input_field.bind('<FocusOut>', self.restore_placeholder)#取消正在打字的提示
        self.input_field.pack(pady=10, padx=20, ipady=5)#add


        self.output_area = tk.Text(
            self.root, 
            height=6, #留空间，万一子比较多
            width=45, #不能太窄，不好读
            font=("Microsoft YaHei", 10),#设字体
            bg="white", #底色
            wrap="word",
            state="disabled",#用户不能自己该

            padx=10,#预留位置
            pady=8
        )
        self.output_area.pack(pady=15, padx=15)

        tk.Button(
            self.root,
            text="获取建议",
            command=self.handle_submit,
            bg="lightblue",
            fg="Black",
            font=("Arial", 15, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(pady=10)#做显示建议的按钮

        self.status_label = tk.Label(
            self.root,
            text="输入后点击「获取建议」",
            bg="lightsteelblue",
            fg="white",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=(5, 0))#更好看
    def clear_placeholder(self, event):
        current = self.input_field.get().strip()
        if self.is_placeholder:
            self.input_field.delete(0, tk.END)
            self.input_field.config(fg='black')

    def restore_placeholder(self, event):
        current = self.input_field.get()#避免空格/误删
        if not current.strip() and current != self.PLACEHOLDER_TEXT:
            self.input_field.insert(0, self.PLACEHOLDER_TEXT)
            self.input_field.config(fg='grey')
            self.is_placeholder = True
    def detect_emotion(self, text):
        emotion_keywords = {
            "anxiety": ["焦虑", "慌", "怕", "压力", "紧张", "心跳得快", "deadline", "考试", ],
            "self_doubt": ["没用", "自卑", "废物", "后悔", "绝望", "想死", "不配", "差"],
            "sad": ["难过", "哭", "抑郁", "心碎", "失去", "空虚", "眼泪", "悲伤","走了"],
            "social": ["吵架", "背叛", "社恐", "被忽视", "冷场", "冲突", "误会"],
            "physical": ["累", "头疼", "失眠", "胸闷", "乏力", "心悸", "胃疼"]
        }
        
        text = text.lower()#小写
        for category, keywords in emotion_keywords.items():
            if any(kw in text for kw in keywords):#找关键词
                return category
        return "general"

    def handle_submit(self):
        user_input = self.input_field.get().strip()#输入
        
        if not user_input or user_input == "点击输入... 说说你现在的感受":
            messagebox.showinfo("提示", "请先描述你的感受~")
            return#提示
        try:
            emotion = self.detect_emotion(user_input)
            response = random.choice(database.get(emotion, ["先深呼吸3秒吧~"]))#保底回复
            
            self.output_area.config(state="normal")#重新写
            self.output_area.delete(1.0, tk.END)#请旧内容
            self.output_area.insert(tk.END, response)#回复
            self.output_area.config(state="disabled")#不让使用者改

            emotion_names = {
                "anxiety": "焦虑", "self_doubt": "自我怀疑", 
                "sad": "悲伤", "social": "社交困扰", 
                "physical": "身体不适", "general": "通用"
            }#分类
            self.status_label.config(
                text=f"检测到：{emotion_names.get(emotion, '通用')}情绪 | 可继续补充描述"
            )#促进表达
            
        except Exception as e:#如果error
            self.output_area.config(state="normal")
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, "系统暂时无法响应，请稍后再试")
            self.output_area.config(state="disabled")
            self.status_label.config(text="系统错误，请重试")

if __name__ == "__main__":
    root = tk.Tk()#初始化
    app = MoodHD(root)
    root.mainloop()#循环
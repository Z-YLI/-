# main.py
import os
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# 强制替换中文字体
win_font = "C:/Windows/Fonts/msyh.ttc"
if os.path.exists(win_font):
    LabelBase.register(name="Roboto", fn_regular=win_font)
    LabelBase.register(name="MyChineseFont", fn_regular=win_font)
else:
    simhei_font = "C:/Windows/Fonts/simhei.ttf"
    if os.path.exists(simhei_font):
        LabelBase.register(name="Roboto", fn_regular=simhei_font)
        LabelBase.register(name="MyChineseFont", fn_regular=simhei_font)

# 莫兰迪色系配色
COLOR_BG = get_color_from_hex('#FDFBF9')
COLOR_TEXT = get_color_from_hex('#5A4C41')
COLOR_SUB = get_color_from_hex('#B7A89B')
COLOR_BTN = get_color_from_hex('#F1EAE3')
COLOR_ACTIVE = get_color_from_hex('#D9CEC5')  # 选中的颜色


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = COLOR_TEXT
        self.font_size = '24sp'
        self.bold = True
        self.font_name = "MyChineseFont"
        with self.canvas.before:
            Color(*COLOR_BTN)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[30])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):
        self.opacity = 0.7

    def on_release(self):
        self.opacity = 1.0


class CounterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row_count = 20
        self.stitch_count = 0
        self.total_rows = 21

        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        # 去掉了Emoji，用纯文字
        title_label = Label(text='编织计数器', color=COLOR_TEXT, font_size='28sp', size_hint_y=0.1, halign='left',
                            text_size=(Window.width - 60, None), font_name="MyChineseFont", bold=True)
        layout.add_widget(title_label)

        num_layout = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        self.row_label = Label(text=str(self.row_count), color=COLOR_TEXT, font_size='80sp', font_name="MyChineseFont")
        self.stitch_label = Label(text=str(self.stitch_count), color=COLOR_TEXT, font_size='80sp',
                                  font_name="MyChineseFont")

        num_layout.add_widget(Label(text='行', color=COLOR_SUB, font_size='20sp', font_name="MyChineseFont"))
        num_layout.add_widget(self.row_label)
        num_layout.add_widget(Label(text='/', color=COLOR_SUB, font_size='50sp', font_name="MyChineseFont"))
        num_layout.add_widget(self.stitch_label)
        num_layout.add_widget(Label(text='针', color=COLOR_SUB, font_size='20sp', font_name="MyChineseFont"))
        layout.add_widget(num_layout)

        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3, spacing=30)
        self.btn_minus = RoundedButton(text='−', font_size='60sp')
        self.btn_plus = RoundedButton(text='+', font_size='60sp')

        self.btn_minus.bind(on_press=self.decrement)
        self.btn_plus.bind(on_press=self.increment)

        btn_layout.add_widget(self.btn_minus)
        btn_layout.add_widget(self.btn_plus)
        layout.add_widget(btn_layout)

        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=20)
        btn_reset = RoundedButton(text='清零重置', font_size='20sp')
        btn_reset.bind(on_press=self.reset)
        bottom_layout.add_widget(btn_reset)
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

    def increment(self, instance):
        if self.row_count < self.total_rows:
            self.row_count += 1
            self.row_label.text = str(self.row_count)

    def decrement(self, instance):
        if self.row_count > 0:
            self.row_count -= 1
            self.row_label.text = str(self.row_count)

    def reset(self, instance):
        self.row_count = 0
        self.stitch_count = 0
        self.row_label.text = '0'
        self.stitch_label.text = '0'


class ProjectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(
            Label(text='图解项目', color=COLOR_TEXT, font_size='28sp', size_hint_y=0.1, font_name="MyChineseFont",
                  bold=True))
        layout.add_widget(Label(text='这里将展示你的图解项目列表...', color=COLOR_SUB, font_size='18sp', font_name="MyChineseFont"))
        self.add_widget(layout)

class OrderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text='接单管理', color=COLOR_TEXT, font_size='28sp', size_hint_y=0.1, font_name="MyChineseFont", bold=True))
        layout.add_widget(Label(text='这里将展示你的接单列表...', color=COLOR_SUB, font_size='18sp', font_name="MyChineseFont"))
        self.add_widget(layout)

class ZhinvApp(App):
    def build(self):
        self.title = '织女管家'
        Window.clearcolor = COLOR_BG

        root = BoxLayout(orientation='vertical')

        self.sm = ScreenManager()
        self.sm.add_widget(CounterScreen(name='counter'))
        self.sm.add_widget(ProjectScreen(name='project'))
        self.sm.add_widget(OrderScreen(name='order'))

        root.add_widget(self.sm)

        nav_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5, padding=5)

        # 去掉了Emoji，纯文字导航
        self.nav_btn1 = Button(text='计 数 器', background_normal='', background_color=COLOR_ACTIVE, color=COLOR_TEXT, font_name="MyChineseFont", font_size='16sp')
        self.nav_btn2 = Button(text='图解项目', background_normal='', background_color=COLOR_BTN, color=COLOR_TEXT, font_name="MyChineseFont", font_size='16sp')
        self.nav_btn3 = Button(text='接单管理', background_normal='', background_color=COLOR_BTN, color=COLOR_TEXT, font_name="MyChineseFont", font_size='16sp')

        self.nav_btn1.bind(on_press=lambda x: self.switch_screen('counter', 1))
        self.nav_btn2.bind(on_press=lambda x: self.switch_screen('project', 2))
        self.nav_btn3.bind(on_press=lambda x: self.switch_screen('order', 3))

        nav_layout.add_widget(self.nav_btn1)
        nav_layout.add_widget(self.nav_btn2)
        nav_layout.add_widget(self.nav_btn3)

        root.add_widget(nav_layout)
        return root

    def switch_screen(self, screen_name, btn_index):
        self.sm.current = screen_name
        # 切换高亮颜色
        self.nav_btn1.background_color = COLOR_ACTIVE if btn_index == 1 else COLOR_BTN
        self.nav_btn2.background_color = COLOR_ACTIVE if btn_index == 2 else COLOR_BTN
        self.nav_btn3.background_color = COLOR_ACTIVE if btn_index == 3 else COLOR_BTN

if __name__ == '__main__':
    ZhinvApp().run()
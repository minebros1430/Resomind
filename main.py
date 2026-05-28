import numpy as np
import tempfile
import wave
import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

Window.size = (360, 640)

class AudioEngine:
    def __init__(self):
        self.sample_rate = 44100
        self.sound = None
        self.temp_file = None

    def _create_wav(self, freq, invert=False, duration=10.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        wave_data = np.sin(2 * np.pi * freq * t)
        if invert:
            wave_data = -wave_data
        
        stereo_wave = np.column_stack((wave_data, wave_data))
        audio_data = np.int16(stereo_wave * 32767)
        
        fd, path = tempfile.mkstemp(suffix='.wav')
        with os.fdopen(fd, 'wb') as f:
            with wave.open(f, 'w') as wav_file:
                wav_file.setnchannels(2)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
        return path

    def start_frequency(self, freq, invert=False):
        self.stop_audio()
        self.temp_file = self._create_wav(freq, invert, duration=60.0)
        self.sound = SoundLoader.load(self.temp_file)
        if self.sound:
            self.sound.loop = True
            self.sound.play()

    def play_white_noise(self, duration=180):
        self.stop_audio()
        noise = np.random.normal(0, 0.1, (int(self.sample_rate * duration), 2))
        audio_data = np.int16(noise * 32767)
        
        fd, path = tempfile.mkstemp(suffix='.wav')
        with os.fdopen(fd, 'wb') as f:
            with wave.open(f, 'w') as wav_file:
                wav_file.setnchannels(2)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
                
        self.temp_file = path
        self.sound = SoundLoader.load(self.temp_file)
        if self.sound:
            self.sound.play()

    def stop_audio(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except:
                pass
            self.temp_file = None

audio_engine = AudioEngine()

KV = '''
MDScreenManager:
    DisclaimerScreen:
    SetupScreen:
    DashboardScreen:
    ActiveSessionScreen:
    ResetScreen:

<DisclaimerScreen>:
    name: 'disclaimer'
    md_bg_color: 0.05, 0.05, 0.08, 1
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(20)
        MDLabel:
            text: "🔒 إخلاء المسؤولية القانونية والأمان"
            font_style: "H5"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 0.3, 0.3, 1
            bold: True
            size_hint_y: None
            height: self.texture_size[1]
        ScrollView:
            MDLabel:
                text: "هذا التطبيق أداة سمعية عصبية لتحفيز التركيز، وليس جهازاً طبياً.\\n\\n⚠️ تحذير الصرع الحسي:\\nيُمنع استخدام هذا التطبيق من قِبل الأشخاص المصابين بالصرع الحسي.\\n\\n🎧 بروتوكول التشغيل الإلكتروني:\\nيتطلب التطبيق استخدام سماعات رأس منفصلة تماماً (ستيريو)."
                font_style: "Body1"
                halign: "right"
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                size_hint_y: None
                height: self.texture_size[1]
        MDRaisedButton:
            text: "أوافق وألتزم بالبروتوكول"
            md_bg_color: 0.12, 0.6, 0.4, 1
            pos_hint: {"center_x": .5}
            size_hint_x: 0.8
            on_release: root.accept_disclaimer()

<SetupScreen>:
    name: 'setup'
    md_bg_color: 0.08, 0.1, 0.15, 1
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(30)
        pos_hint: {"center_y": .5}
        MDLabel:
            text: "📱 ResoMind\\nرنين العقل"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.2, 0.7, 0.9, 1
            bold: True
        MDLabel:
            text: "دوزن خلايا دماغك لتعلم فائق بـ \\"الرنين الجزيئي الديناميكي\\""
            font_style: "Subtitle1"
            halign: "center"
            theme_text_color: "Secondary"
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            size_hint_y: None
            height: dp(100)
            MDLabel:
                text: "كم عدد الأقسام العلمية التي تريد الحفظ فيها اليوم؟"
                font_style: "Body1"
                halign: "center"
                theme_text_color: "Primary"
                bold: True
            MDTextField:
                id: section_input
                hint_text: "أدخل عدد الأقسام (مثال: 5)"
                text: "5"
                input_filter: "int"
                halign: "center"
                mode: "rectangle"
                line_color_focus: 0.2, 0.7, 0.9, 1
                size_hint_x: 0.6
                pos_hint: {"center_x": .5}
        MDRaisedButton:
            text: "ابدأ الجلسة الديناميكية"
            md_bg_color: 0.2, 0.6, 0.8, 1
            pos_hint: {"center_x": .5}
            size_hint_x: 0.8
            on_release: root.generate_sections()

<DashboardScreen>:
    name: 'dashboard'
    md_bg_color: 0.08, 0.08, 0.12, 1
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)
        MDLabel:
            text: "🎛️ لوحة التصنيفات المتوالية"
            font_style: "H6"
            halign: "center"
            bold: True
            size_hint_y: None
            height: dp(40)
            theme_text_color: "Custom"
            text_color: 0.2, 0.7, 0.9, 1
        ScrollView:
            BoxLayout:
                id: container
                orientation: 'vertical'
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(4)
        MDRaisedButton:
            text: "إنهاء الجلسة وإعادة ضبط الدماغ"
            md_bg_color: 0.7, 0.2, 0.2, 1
            pos_hint: {"center_x": .5}
            size_hint_x: 0.9
            on_release: root.finish_session()

<ActiveSessionScreen>:
    name: 'active_session'
    md_bg_color: 0.05, 0.08, 0.12, 1
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(24)
        MDIconButton:
            icon: "arrow-right"
            pos_hint: {"right": 1}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            on_release: root.go_back()
        MDLabel:
            id: session_title
            text: "القسم الحالي"
            font_style: "H4"
            halign: "center"
            bold: True
            theme_text_color: "Custom"
            text_color: 0.2, 0.7, 0.9, 1
        MDLabel:
            id: freq_info
            text: "التردد الجزيئي الجاري حسابه: -- هرتز"
            font_style: "Subtitle1"
            halign: "center"
            theme_text_color: "Secondary"
        MDLabel:
            id: timer_label
            text: "00:00"
            font_style: "H2"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        MDLabel:
            id: status_label
            text: "الحالة: جاهز لبدء الموجة"
            font_style: "Body1"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.6, 0.6, 0.6, 1
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(16)
            size_hint_y: None
            height: dp(140)
            MDRaisedButton:
                id: btn_start_freq
                text: "🎧 ابدأ التردد"
                font_size: "18sp"
                md_bg_color: 0.12, 0.6, 0.4, 1
                size_hint_x: 1
                on_release: root.start_frequency_session()
            MDRaisedButton:
                id: btn_stabilize
                text: "⏸️ تثبيت وتصفير"
                font_size: "18sp"
                md_bg_color: 0.8, 0.4, 0.12, 1
                size_hint_x: 1
                disabled: True
                on_release: root.start_stabilization_phase()

<ResetScreen>:
    name: 'reset'
    md_bg_color: 0.02, 0.02, 0.05, 1
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(30)
        pos_hint: {"center_y": .5}
        MDLabel:
            text: "🧠 Neuro-Reset\\nإعادة ضبط الدماغ"
            font_style: "H4"
            halign: "center"
            bold: True
            theme_text_color: "Custom"
            text_color: 0.5, 0.8, 0.2, 1
        MDLabel:
            id: reset_timer
            text: "03:00"
            font_style: "H3"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.5, 0.8, 0.2, 1
        MDRaisedButton:
            text: "خروج وتكرار الجلسة"
            md_bg_color: 0.2, 0.2, 0.3, 1
            pos_hint: {"center_x": .5}
            size_hint_x: 0.8
            on_release: root.exit_app()
'''

class DisclaimerScreen(MDScreen):
    def accept_disclaimer(self):
        self.manager.current = 'setup'

class SetupScreen(MDScreen):
    def generate_sections(self):
        try:
            n_sections = int(self.ids.section_input.text)
            if n_sections <= 0: raise ValueError
        except ValueError:
            n_sections = 5
        delta_f = 10.0 / n_sections
        base_gamma = 35.0
        dashboard = self.manager.get_screen('dashboard')
        dashboard.build_dynamic_dashboard(n_sections, delta_f, base_gamma)
        self.manager.current = 'dashboard'

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sections_data = []
        self.last_accessed_index = -1

    def build_dynamic_dashboard(self, n, delta_f, base_gamma):
        container = self.ids.container
        container.clear_widgets()
        self.sections_data = []
        self.last_accessed_index = -1 
        for i in range(n):
            freq = base_gamma + (i * delta_f) + (delta_f / 2.0)
            section_name = f"القسم {i+1}"
            self.sections_data.append({"index": i, "name": section_name, "frequency": freq})
            card = MDCard(orientation='vertical', padding=16, size_hint_y=None, height=110, md_bg_color=(0.12, 0.15, 0.2, 1), radius=[12, 12, 12, 12], elevation=2)
            lbl_title = MDLabel(text=f"📂 {section_name}", font_style="H6", theme_text_color="Custom", text_color=(1, 1, 1, 1), halign="right")
            lbl_freq = MDLabel(text=f"التردد الموزون: {freq:.3f} هرتز", font_style="Caption", theme_text_color="Secondary", halign="right")
            btn_enter = MDRaisedButton(text="دخول القسم", md_bg_color=(0.2, 0.7, 0.9, 1), pos_hint={"left": 1}, on_release=lambda x, idx=i: self.enter_section(idx))
            card.add_widget(lbl_title)
            card.add_widget(lbl_freq)
            card.add_widget(btn_enter)
            container.add_widget(card)

    def enter_section(self, index):
        if index != self.last_accessed_index + 1:
            dialog = MDDialog(title="⚠️ خرق بروتوكول التوالي", text="يجب الدخول إلى الأقسام بالترتيب التصاعدي الدقيق وبدون تخطي أو تكرار.", buttons=[MDRaisedButton(text="مفهوم", on_release=lambda x: dialog.dismiss())])
            dialog.open()
            return
        self.last_accessed_index = index
        session_screen = self.manager.get_screen('active_session')
        session_screen.setup_session(self.sections_data[index])
        self.manager.current = 'active_session'

    def finish_session(self):
        self.manager.current = 'reset'
        self.manager.get_screen('reset').start_neuro_reset()

class ActiveSessionScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_time = 0
        self.timer_event = None
        self.current_freq = 40.0
        self.phase = "idle"

    def setup_session(self, data):
        self.current_data = data
        self.current_freq = data["frequency"]
        self.ids.session_title.text = data["name"]
        self.ids.freq_info.text = f"التردد الجزيئي الموزون: {self.current_freq:.3f} هرتز"
        self.reset_ui()

    def reset_ui(self):
        self.session_time = 0
        self.ids.timer_label.text = "00:00"
        self.ids.status_label.text = "الحالة: جاهز لبدء الموجة"
        self.ids.status_label.text_color = (0.6, 0.6, 0.6, 1)
        self.ids.btn_start_freq.disabled = False
        self.ids.btn_stabilize.disabled = True
        self.phase = "idle"

    def start_frequency_session(self):
        self.phase = "reading"
        self.ids.btn_start_freq.disabled = True
        self.ids.btn_stabilize.disabled = False
        self.ids.status_label.text = "⚡ جاري بث الموجة..."
        self.ids.status_label.text_color = (0.12, 0.6, 0.4, 1)
        audio_engine.start_frequency(self.current_freq, invert=False)
        if self.timer_event: Clock.unschedule(self.timer_event)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.phase == "reading":
            self.session_time += 1
        elif self.phase == "stabilizing":
            self.session_time -= 1
            if self.session_time <= 0:
                self.end_stabilization_phase()
        mins, secs = divmod(self.session_time, 60)
        self.ids.timer_label.text = f"{mins:02d}:{secs:02d}"

    def start_stabilization_phase(self):
        self.phase = "stabilizing"
        self.ids.btn_stabilize.disabled = True
        self.ids.status_label.text = "⏸️ تصفير ومعكوس الطور (180°)..."
        self.ids.status_label.text_color = (0.8, 0.4, 0.12, 1)
        audio_engine.start_frequency(self.current_freq, invert=True)

    def end_stabilization_phase(self):
        Clock.unschedule(self.timer_event)
        audio_engine.stop_audio()
        self.manager.current = 'dashboard'

    def go_back(self):
        audio_engine.stop_audio()
        if self.timer_event: Clock.unschedule(self.timer_event)
        self.manager.current = 'dashboard'

class ResetScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remaining_time = 180
        self.reset_event = None

    def start_neuro_reset(self):
        self.remaining_time = 180
        audio_engine.play_white_noise(self.remaining_time)
        if self.reset_event: Clock.unschedule(self.reset_event)
        self.reset_event = Clock.schedule_interval(self.update_reset_timer, 1)

    def update_reset_timer(self, dt):
        self.remaining_time -= 1
        mins, secs = divmod(self.remaining_time, 60)
        self.ids.reset_timer.text = f"{mins:02d}:{secs:02d}"
        if self.remaining_time <= 0:
            self.exit_app()

    def exit_app(self):
        if self.reset_event: Clock.unschedule(self.reset_event)
        audio_engine.stop_audio()
        self.manager.current = 'setup'

class ResoMindApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        return Builder.load_string(KV)

if __name__ == '__main__':
    ResoMindApp().run()

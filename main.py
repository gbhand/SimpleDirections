from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from googlemaps import *

import core

class Input(GridLayout):
    
    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Starting Address'))
        self.start = TextInput(multiline=False)
        self.add_widget(self.start)
        self.add_widget(Label(text='Destination Address'))
        self.end = TextInput(multiline=False)
        self.add_widget(self.end)
        
    def check_valid(self):
        if len(self.start.text + self.end.text) > 0:
            return True
        else:
            return False
        
    def clear(self):
        self.start.text = ""
        self.end.text = ""
        
    def get_waypoints(self):
        return [self.start.text, self.end.text]
        
class Output(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Output, self).__init__(**kwargs)
        self.orientation = "vertical"
        
    def test(self):
        self.add_widget(Label(text="This worked!"))
        
    def get_route(self, waypoints):
        data = core.find_route(waypoints)
        info = data.get("info")
        
        for line in info:
            self.add_widget(Label(text=line))
        
        steps = data.get("steps")
        
        for step in steps:
            box = BoxLayout(orientation="horizontal")
            textbox = BoxLayout(orientation='vertical')
            raw_text = step.get("text")
            if  "font-size" in raw_text:
                raw_text = raw_text.replace('</div>', '')
                str = raw_text.split('<div style="font-size:0.9em">')
                
                text = Label(text=str[0])
                subtext = Label(text=str[1], font_size=10)
                textbox.add_widget(text)
                textbox.add_widget(subtext)
            else:
                text = Label(text=raw_text)
                textbox.add_widget(text)
            box.add_widget(textbox)
            distance = Label(text=step.get("distance"))
            
            
            box.add_widget(distance)
            self.add_widget(box)

class InterfaceManager(BoxLayout):
    
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size,
                                   pos=self.pos)
                                   
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

# listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)

        title = Label(text="SimpleDirections")
        
        input = Input()
        
        submit = Button(text="Submit", size_hint=(0.2, 0.2), halign="center")
        submit.bind(on_press=self.show_result)
        self.title = title
        self.input = input
        self.submit = submit
        
        reset = Button(text="Reset", size_hint=(0.2, 0.2))
        reset.bind(on_press=self.show_home)
        self.reset = reset
        
        output = Output()
        self.output = output
        self.add_widget(title)
        self.add_widget(input)
        self.add_widget(submit)
        
    def show_result(self, button):
        if self.input.check_valid() == False:
            return
        
        try:
            self.output.get_route(self.input.get_waypoints())
        except googlemaps.exceptions.TransportError as e:
            print(e)
            return
        self.clear_widgets()
        self.add_widget(self.output)
        self.add_widget(self.reset)
        
    def show_home(self, button):
        self.clear_widgets()
        self.input.clear()
        self.output.clear_widgets()
        self.add_widget(self.title)
        self.add_widget(self.input)
        self.add_widget(self.submit)

class Directions(App):
    def build(self):
        return InterfaceManager(orientation="vertical")
        
        
if __name__ == '__main__':
    Directions().run()

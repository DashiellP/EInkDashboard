from applets.base import Applet, View


class WeatherApplet(Applet):
    id = "weather"
    name = "Weather"
    
    def on_start(self) -> None:
        self.context.request_redraw()

    def build_view(self):
        template = self.load_template_file("templates/full.html")
        context = {"test_value": "this is a test"}
        return View(
            template,
            context
        )
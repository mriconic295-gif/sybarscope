from urllib.parse import urlparse
import re

class TechDetector:
    def __init__(self, url: str, html: str):
        self.url = url
        self.html = html

    def detect(self) -> list:
        techs = []
        # Simple pattern based detection
        if 'wordpress' in self.html.lower():
            techs.append("WordPress")
        if 'drupal' in self.html.lower():
            techs.append("Drupal")
        if 'joomla' in self.html.lower():
            techs.append("Joomla")
        if 'jquery' in self.html.lower():
            techs.append("jQuery")
        if 'bootstrap' in self.html.lower():
            techs.append("Bootstrap")
        if 'react' in self.html.lower():
            techs.append("React")
        if 'angular' in self.html.lower():
            techs.append("Angular")
        if 'vue' in self.html.lower():
            techs.append("Vue.js")
        return list(set(techs))

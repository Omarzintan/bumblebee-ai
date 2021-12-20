import speedtest
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "internet_speed_test"
        self.patterns = [
            "run internet speed test",
            "test internet speed",
            "how fast is my internet"
        ]
        self.bs = bumblebee_api.get_speech()

    def action(self, spoken_text: str = "", arguments_list: list = []):
        s = speedtest.Speedtest()

        self.bs.respond("Testing...\n")

        downloadSpeed = s.download() / 1048576
        uploadSpeed = s.upload() / 1048576
        pingResult = round(s.results.ping)

        self.bs.respond(f"Download speed: {downloadSpeed:.2f} Mbps\n")
        self.bs.respond(f"Upload speed: {uploadSpeed:.2f} Mbps\n")
        self.bs.respond(f"Ping: {pingResult} ms\n")

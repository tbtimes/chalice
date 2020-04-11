import requests
import boto3


class ChaliceError(Exception):
    pass


class Event:
    status = ""
    source = ""
    channel = ""
    gateway = ""
    payload = {}

    def __init__(self, **kwargs):
        self.source = kwargs.get("source")
        self.status = kwargs.get("status")
        self.payload = kwargs.get("payload")
        self.channel = kwargs.get("channel")
        self.gateway = kwargs.get("gateway")
        # TODO: subclass ChaliceError with specifics
        if not self.source:
            raise ChaliceError()
        if not self.status:
            raise ChaliceError()
        if not self.channel:
            raise ChaliceError()
        if not self.gateway:
            raise ChaliceError()

    def publish(self):
        ep = f"https://{self.gateway}/{self.channel}"
        return requests.post(ep, json=self.to_json())

    def __repr__(self):
        return f"{self.status}{{ source={self.source} }}"

    def __iter__(self):
        yield "source", self.source
        yield "status", self.status
        yield "payload", self.payload
        yield "channel", self.channel,
        yield "gateway", self.gateway

    def to_json(self):
        return dict((x, y) for x, y in iter(self))

class UnknownEvent(object):
    pass


class ArchiveSuccess(Event):
    def __init__(self, **kwargs):
        DEFAULTS = {"status": "ArchiveSuccess", "channel": "api-covid-archiver"}
        z = {**DEFAULTS, **kwargs}
        super().__init__(**z)


class PackBegin(Event):
    def __init__(self, **kwargs):
        DEFAULTS = {"status": "PackBegin", "channel": "api-covid-pack"}
        z = {**DEFAULTS, **kwargs}
        super().__init__(**z)

class PackWorkerBegin(Event):
    def __init__(self, **kwargs):
        DEFAULTS = {"status": "PackWorkerBegin", "channel": "api-covid-pack-worker"}
        z = {**DEFAULTS, **kwargs}
        if not z.get("payload", None):
            raise err.PackWorkerNoPayload()
        super().__init__(**z)
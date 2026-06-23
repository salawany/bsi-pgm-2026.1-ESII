from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, evento: dict) -> None:
        pass


class Subject:
    def __init__(self):
        self._observers = []

    def registrar_observer(self, obs: Observer) -> None:
        self._observers.append(obs)

    def notificar(self, evento: dict) -> None:
        for obs in self._observers:
            obs.update(evento)
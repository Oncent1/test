from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from direct.task import Task
import random

class QuantumCity(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self._init_controls()
        self.player = self.loader.loadModel('models/box')
        self.player.reparentTo(self.render)
        self.player.setScale(0.5, 0.5, 1.0)
        self.player.setColor(1, 0, 0, 1)
        self.player.setPos(0, 0, 0.5)
        self.camera_distance = 8
        self.first_person = False

        self._build_city()
        self.taskMgr.add(self.update, 'update')

    def _init_controls(self):
        self.accept('escape', self.userExit)
        self.keys = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'turn_left': False,
            'turn_right': False,
        }
        for key in ['w', 's', 'a', 'd', 'arrow_left', 'arrow_right']:
            self.accept(key, self._set_key, [key, True])
            self.accept(f'{key}-up', self._set_key, [key, False])
        self.accept('c', self._toggle_view)
        self.accept('q', self._quantum_leap)

    def _set_key(self, key, value):
        mapping = {
            'w': 'forward',
            's': 'backward',
            'a': 'left',
            'd': 'right',
            'arrow_left': 'turn_left',
            'arrow_right': 'turn_right',
        }
        if key in mapping:
            self.keys[mapping[key]] = value

    def _toggle_view(self):
        self.first_person = not self.first_person

    def _quantum_leap(self):
        x = random.uniform(-25, 25)
        y = random.uniform(-25, 25)
        self.player.setPos(x, y, 0.5)

    def _build_city(self):
        for i in range(-10, 11, 2):
            for j in range(-10, 11, 2):
                if i == 0 and j == 0:
                    continue
                b = self.loader.loadModel('models/box')
                b.reparentTo(self.render)
                sx = random.uniform(0.5, 2.0)
                sy = random.uniform(0.5, 2.0)
                sz = random.uniform(1.0, 6.0)
                b.setScale(sx, sy, sz)
                b.setPos(i * 2, j * 2, sz / 2)
                b.setColor(random.random(), random.random(), random.random(), 1)

    def update(self, task):
        dt = globalClock.getDt()
        pos = self.player.getPos()
        hpr = self.player.getHpr()
        speed = 10
        turn_speed = 60
        if self.keys['forward']:
            pos += self.player.getQuat().getForward() * (speed * dt)
        if self.keys['backward']:
            pos -= self.player.getQuat().getForward() * (speed * dt)
        if self.keys['left']:
            pos -= self.player.getQuat().getRight() * (speed * dt)
        if self.keys['right']:
            pos += self.player.getQuat().getRight() * (speed * dt)
        if self.keys['turn_left']:
            hpr.x -= turn_speed * dt
        if self.keys['turn_right']:
            hpr.x += turn_speed * dt
        self.player.setPos(pos)
        self.player.setHpr(hpr)

        if self.first_person:
            self.camera.reparentTo(self.player)
            self.camera.setPos(0, 0, 1)
            self.camera.setHpr(0, 0, 0)
        else:
            self.camera.reparentTo(self.render)
            cam_pos = pos - self.player.getQuat().getForward() * self.camera_distance + Vec3(0,0,3)
            self.camera.setPos(cam_pos)
            self.camera.lookAt(self.player)

        return Task.cont


if __name__ == '__main__':
    app = QuantumCity()
    app.run()

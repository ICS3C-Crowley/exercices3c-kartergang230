import tkinter as tk
import random
import time
import sys

WIDTH, HEIGHT = 400, 600
FPS = 60
FRAME_MS = int(1000 / FPS)

PLAYER_W, PLAYER_H = 40, 70
LANE_MARGIN = 50

OB_MIN_W, OB_MAX_W = 40, 80
OB_MIN_H, OB_MAX_H = 20, 40
OB_SPAWN_INTERVAL = 700  # ms

class Player:
    def __init__(self):
        self.w = PLAYER_W
        self.h = PLAYER_H
        self.x = WIDTH//2 - self.w//2
        self.y = HEIGHT - self.h - 20
        self.speed = 6
        self.color = '#ffcc00'
    def rect(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)

class Obstacle:
    def __init__(self, speed):
        self.w = random.randint(OB_MIN_W, OB_MAX_W)
        self.h = random.randint(OB_MIN_H, OB_MAX_H)
        self.x = random.randint(0, WIDTH - self.w)
        self.y = -self.h - 10
        self.color = '#c0392b'
        self.speed = speed
    def rect(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)

def rects_collide(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

class GameApp:
    def __init__(self, root):
        self.root = root
        root.title("Mini-jeu Voiture (Tkinter)")
        self.frame = tk.Frame(root, bg='#222')
        self.frame.pack(padx=10, pady=10)

        self.hud = tk.Frame(self.frame, bg='#222')
        self.hud.pack(fill='x')
        self.score_var = tk.StringVar(value="Score: 0")
        self.score_label = tk.Label(self.hud, textvariable=self.score_var, fg='white', bg='#222')
        self.score_label.pack(side='left')

        self.start_btn = tk.Button(self.hud, text="Démarrer", command=self.start_game)
        self.start_btn.pack(side='left', padx=6)
        self.restart_btn = tk.Button(self.hud, text="Recommencer", command=self.restart_game, state='disabled')
        self.restart_btn.pack(side='left')

        self.canvas = tk.Canvas(self.frame, width=WIDTH, height=HEIGHT, bg='#2c2c2c', highlightthickness=0)
        self.canvas.pack()

        self.instructions = tk.Label(self.frame, text="Flèches ← → ou A/D pour se déplacer. Évitez les obstacles.", bg='#222', fg='#ccc')
        self.instructions.pack(pady=6)

        # game state
        self.player = Player()
        self.obstacles = []
        self.keys = set()
        self.running = False
        self.game_over = False
        self.score = 0
        self.speed = 2.0
        self.last_spawn = 0
        self.last_time = int(time.time() * 1000)

        # bindings
        root.bind("<KeyPress>", self.on_keydown)
        root.bind("<KeyRelease>", self.on_keyup)

        # draw initial screen
        self.draw()

    def on_keydown(self, event):
        self.keys.add(event.keysym)
        # allow restart with 'r' if game over
        if self.game_over and event.keysym.lower() == 'r':
            self.restart_game()

    def on_keyup(self, event):
        if event.keysym in self.keys:
            self.keys.remove(event.keysym)

    def start_game(self):
        if self.running:
            return
        self.reset_state()
        self.running = True
        self.start_btn.config(state='disabled')
        self.restart_btn.config(state='disabled')
        self.loop()

    def restart_game(self):
        self.reset_state()
        self.running = True
        self.game_over = False
        self.start_btn.config(state='disabled')
        self.restart_btn.config(state='disabled')
        self.loop()

    def reset_state(self):
        self.player = Player()
        self.obstacles = []
        self.keys = set()
        self.game_over = False
        self.score = 0
        self.speed = 2.0
        self.last_spawn = int(time.time() * 1000)
        self.score_var.set("Score: 0")
        self.canvas.delete("all")
        self.draw()

    def spawn_obstacle(self):
        self.obstacles.append(Obstacle(self.speed))

    def update(self):
        now = int(time.time() * 1000)
        dt = now - self.last_time
        self.last_time = now

        # controls
        if ('Left' in self.keys) or ('a' in self.keys) or ('A' in self.keys):
            self.player.x -= self.player.speed
        if ('Right' in self.keys) or ('d' in self.keys) or ('D' in self.keys):
            self.player.x += self.player.speed
        self.player.x = max(0, min(self.player.x, WIDTH - self.player.w))

        # spawn
        if now - self.last_spawn > OB_SPAWN_INTERVAL:
            self.last_spawn = now
            self.spawn_obstacle()
            self.speed += 0.05

        # update obstacles
        new_obs = []
        for ob in self.obstacles:
            ob.y += ob.speed
            if ob.y > HEIGHT:
                self.score += 1
                self.score_var.set(f"Score: {self.score}")
            else:
                new_obs.append(ob)
        self.obstacles = new_obs

        # collisions
        for ob in self.obstacles:
            if rects_collide(self.player.rect(), ob.rect()):
                self.game_over = True
                self.running = False
                break

    def draw(self):
        self.canvas.delete("all")
        # road
        self.canvas.create_rectangle(LANE_MARGIN, 0, WIDTH - LANE_MARGIN, HEIGHT, fill='#333', outline='')
        # center dashed line
        dash_h = 20
        gap = 14
        x_center = WIDTH // 2
        y = - (int(time.time() * 1000) // 5 % (dash_h + gap))
        while y < HEIGHT:
            self.canvas.create_rectangle(x_center-2, y, x_center+2, y+dash_h, fill='white', outline='')
            y += dash_h + gap

        # player
        x1, y1, x2, y2 = self.player.rect()
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.player.color, outline='', width=0)
        # windows
        self.canvas.create_rectangle(x1+6, y1+8, x2-6, y1+8 + (self.player.h//3), fill='#1e1e1e', outline='')

        # obstacles
        for ob in self.obstacles:
            ox1, oy1, ox2, oy2 = ob.rect()
            self.canvas.create_rectangle(ox1, oy1, ox2, oy2, fill=ob.color, outline='')

        if self.game_over:
            self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='black', stipple='gray25')
            self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20, text="GAME OVER", fill='white', font=('Helvetica', 24))
            self.canvas.create_text(WIDTH//2, HEIGHT//2 + 10, text=f"Score: {self.score}", fill='white', font=('Helvetica', 16))
            self.restart_btn.config(state='normal')
            self.start_btn.config(state='normal')

    def loop(self):
        if not self.running:
            self.draw()
            return
        self.update()
        self.draw()
        if self.running:
            self.root.after(FRAME_MS, self.loop)
        else:
            # ended this frame
            self.draw()

def main():
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
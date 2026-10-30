
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NO SIGNAL — Dino Run</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --cyan: #63f5ff;
    --orange: #ff9e55;
    --bg: #070b14;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    overflow: hidden;
    background: var(--bg);
    color: white;
    font-family: 'Rajdhani', sans-serif;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 5;
    opacity: .12;
    background: repeating-linear-gradient(
        to bottom, transparent 0px, transparent 3px,
        #a4d9ff 4px
    );
}

.ambient {
    position: fixed;
    width: 65vw;
    height: 65vw;
    top: -35vw;
    left: 17%;
    background: #164b81;
    filter: blur(130px);
    opacity: .22;
    pointer-events: none;
}

.app {
    position: relative;
    z-index: 1;
    width: min(1200px, 96vw);
    height: 100vh;
    max-height: 850px;
    margin: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 22px 0;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8px 22px;
    gap: 12px;
}

.brand {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(13px, 2vw, 19px);
    font-weight: 900;
    letter-spacing: 3px;
}

.brand span { color: var(--cyan); }

.status {
    font-size: 12px;
    letter-spacing: 2px;
    color: #90a9bd;
}

.live {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--cyan);
    margin-right: 8px;
    box-shadow: 0 0 12px var(--cyan);
}

.panel {
    position: relative;
    width: 100%;
    border: 1px solid #25435a;
    background: #08111d;
    box-shadow: 0 0 55px #12395b22, inset 0 0 40px #0d284022;
    overflow: hidden;
}

.panel::before, .panel::after {
    content: "";
    position: absolute;
    z-index: 4;
    width: 35px;
    height: 35px;
    pointer-events: none;
}

.panel::before {
    top: -1px;
    left: -1px;
    border-top: 2px solid var(--cyan);
    border-left: 2px solid var(--cyan);
}

.panel::after {
    bottom: -1px;
    right: -1px;
    border-bottom: 2px solid var(--cyan);
    border-right: 2px solid var(--cyan);
}

.hud {
    position: absolute;
    top: 22px;
    left: 25px;
    right: 25px;
    z-index: 3;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
}

.hud-label {
    color: #6b8ba5;
    font-size: 11px;
    letter-spacing: 2px;
}

.hud-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 21px;
    margin-top: 5px;
    color: var(--cyan);
    text-shadow: 0 0 15px #63f5ff55;
}

.best .hud-value { color: var(--orange); }

#game {
    display: block;
    width: 100%;
    height: clamp(300px, 51vh, 470px);
    touch-action: manipulation;
    cursor: pointer;
}

.overlay {
    position: absolute;
    inset: 0;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px 15px;
    text-align: center;
    background: linear-gradient(180deg, #050a14a8, #07101b45);
    transition: opacity .25s;
}

.overlay.hidden {
    opacity: 0;
    pointer-events: none;
}

.eyebrow {
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    letter-spacing: 5px;
    color: var(--cyan);
    margin-bottom: 16px;
}

h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(29px, 6vw, 70px);
    line-height: 1.12;
    margin: 0;
    font-weight: 900;
    letter-spacing: -2px;
    text-shadow: 0 0 45px #63f5ff32;
}

h1 span {
    display: block;
    color: transparent;
    -webkit-text-stroke: 1px var(--cyan);
}

.subtitle {
    color: #a3b7c9;
    font-size: 16px;
    letter-spacing: 2px;
    margin: 17px 0 26px;
}

button {
    font-family: 'Orbitron', sans-serif;
    cursor: pointer;
    color: #07111a;
    background: var(--cyan);
    border: 1px solid var(--cyan);
    padding: 15px 30px;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 2px;
    box-shadow: 0 0 30px #63f5ff25;
    transition: .2s;
}

button:hover {
    background: white;
    box-shadow: 0 0 35px #63f5ff77;
    transform: translateY(-2px);
}

.hint {
    color: #7892a8;
    font-size: 12px;
    letter-spacing: 2px;
    margin-top: 19px;
}

.bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    padding: 19px 8px 0;
    color: #7892a8;
    font-size: 12px;
    letter-spacing: 1px;
}

.controls {
    display: flex;
    gap: 17px;
    flex-wrap: wrap;
}

.key {
    color: var(--cyan);
    border: 1px solid #25435a;
    padding: 4px 8px;
    margin-right: 5px;
}

#toast {
    position: absolute;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 3;
    font-family: 'Orbitron', sans-serif;
    color: var(--orange);
    font-size: 10px;
    letter-spacing: 3px;
    white-space: nowrap;
    pointer-events: none;
}

@media(max-width:600px) {
    .app { width: 94vw; padding: 14px 0; }
    .topbar { padding-bottom: 14px; }
    #game { height: 54vh; }
    .hud { top: 15px; left: 14px; right: 14px; }
    .hud-value { font-size: 16px; }
    .bottom { font-size: 10px; }
    .controls { gap: 8px; }
    .status { font-size: 9px; letter-spacing: 1px; }
}
</style>
</head>

<body>
<div class="ambient"></div>

<main class="app">
    <header class="topbar">
        <div class="brand">NO<span>SIGNAL</span> / 001</div>
        <div class="status"><i class="live"></i> SYSTEM OFFLINE</div>
    </header>

    <section class="panel">
        <div class="hud">
            <div>
                <div class="hud-label">DISTANCE</div>
                <div class="hud-value" id="score">00000</div>
            </div>
            <div class="best" style="text-align:right">
                <div class="hud-label">PERSONAL BEST</div>
                <div class="hud-value" id="best">00000</div>
            </div>
        </div>

        <canvas id="game"></canvas>

        <div class="overlay" id="overlay">
            <div class="eyebrow" id="eyebrow">CONNECTION LOST // 00:00</div>
            <h1 id="headline">THE LAST<span>RUNNER.</span></h1>
            <p class="subtitle" id="subtitle">
                NO INTERNET. NO LIMITS.
            </p>
            <button id="start">INITIALIZE RUN &nbsp; →</button>
            <div class="hint" id="hint">SPACE / ↑ TO JUMP</div>
        </div>

        <div id="toast">SURVIVE THE SILENCE</div>
    </section>

    <footer class="bottom">
        <div class="controls">
            <span><b class="key">SPACE</b> JUMP</span>
            <span><b class="key">↑</b> JUMP</span>
            <span><b class="key">↓</b> DUCK</span>
        </div>
        <div>BUILD 01.26 &nbsp; // &nbsp; ENDLESS MODE</div>
    </footer>
</main>

<script>
(() => {
    const canvas = document.getElementById('game');
    const ctx = canvas.getContext('2d');
    const overlay = document.getElementById('overlay');
    const startBtn = document.getElementById('start');
    const scoreEl = document.getElementById('score');
    const bestEl = document.getElementById('best');
    const headline = document.getElementById('headline');
    const subtitle = document.getElementById('subtitle');
    const eyebrow = document.getElementById('eyebrow');
    const hint = document.getElementById('hint');
    const toast = document.getElementById('toast');

    let W = 900, H = 430, ground;
    let running = false, started = false, dead = false;
    let score = 0, best = 0, speed = 360;
    let time = 0, spawn = 0, last = 0, flash = 0;
    let obstacles = [], particles = [], clouds = [];
    let duck = false;
    let dino = { x: 100, y: 0, vy: 0, h: 48, w: 35, onGround: true };
    const gravity = 1900;

    try {
        best = Number(localStorage.getItem('nosignal-best')) || 0;
    } catch(e) {}
    bestEl.textContent = fmt(best);

    function fmt(n) {
        return String(Math.floor(n)).padStart(5, '0');
    }

    function resize() {
        const r = canvas.getBoundingClientRect();
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        W = Math.max(300, r.width);
        H = Math.max(260, r.height);
        canvas.width = Math.round(W * dpr);
        canvas.height = Math.round(H * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ground = H - 48;
        dino.x = Math.max(38, W * 0.12);
        if (!started || dino.onGround) dino.y = ground - dino.h;
        clouds = Array.from({length: 8}, (_, i) => ({
            x: i * W / 6 + Math.random() * 70,
            y: 75 + Math.random() * H * .35,
            s: .5 + Math.random() * 1.1
        }));
        draw();
    }

    function rand(a, b) { return a + Math.random() * (b - a); }

    function start() {
        score = 0;
        speed = 360;
        time = 0;
        spawn = 1;
        obstacles = [];
        particles = [];
        dead = false;
        running = true;
        started = true;
        duck = false;
        flash = 0;
        dino.h = 48;
        dino.w = 35;
        dino.y = ground - dino.h;
        dino.vy = 0;
        dino.onGround = true;
        overlay.classList.add('hidden');
        toast.textContent = 'SURVIVE THE SILENCE';
        last = performance.now();
        requestAnimationFrame(loop);
    }

    function endGame() {
        running = false;
        dead = true;
        flash = .35;
        for (let i = 0; i < 22; i++) {
            particles.push({
                x: dino.x + dino.w / 2,
                y: dino.y + dino.h / 2,
                vx: rand(-220, 220),
                vy: rand(-260, 100),
                life: rand(.3, .8)
            });
        }
        best = Math.max(best, Math.floor(score));
        try { localStorage.setItem('nosignal-best', best); } catch(e) {}
        bestEl.textContent = fmt(best);
        headline.innerHTML = 'RUN <span>TERMINATED.</span>';
        subtitle.textContent = 'DISTANCE ACHIEVED: ' + fmt(score);
        eyebrow.textContent = 'SYSTEM FAILURE // REBOOT REQUIRED';
        startBtn.textContent = 'RETRY MISSION  ↻';
        hint.textContent = 'PRESS SPACE OR CLICK TO RESTART';
        overlay.classList.remove('hidden');
        toast.textContent = 'SIGNAL LOST';
        draw();
    }

    function jump() {
        if (!started || dead) {
            start();
            return;
        }
        if (!running) return;
        if (dino.onGround) {
            dino.vy = -690;
            dino.onGround = false;
            for (let i = 0; i < 7; i++) {
                particles.push({
                    x: dino.x + 15, y: ground - 3,
                    vx: rand(-90, 40), vy: rand(-100, -15),
                    life: rand(.2, .45)
                });
            }
        }
    }

    function spawnObstacle() {
        const type = Math.random() < .22 && score > 150 ? 'bird' : 'cactus';
        const size = rand(.8, 1.25);
        obstacles.push({
            type, x: W + 30,
            w: type === 'bird' ? 42 : 24 * size,
            h: type === 'bird' ? 25 : 42 * size,
            y: type === 'bird' ? ground - rand(70, 100) : ground,
            size,
            wing: 0
        });
        spawn = rand(0.85, 1.5) * Math.max(.66, 360 / speed);
    }

    function circle(x, y, r, color) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
    }

    function drawBackground() {
        const sky = ctx.createLinearGradient(0, 0, 0, H);
        sky.addColorStop(0, '#081323');
        sky.addColorStop(.6, '#14273b');
        sky.addColorStop(1, '#1c2936');
        ctx.fillStyle = sky;
        ctx.fillRect(0, 0, W, H);

        // Moon
        circle(W * .78, H * .23, 34, '#b3e7f6');
        circle(W * .78 + 10, H * .23 - 7, 31, '#101d30');

        // Stars
        for (let i = 0; i < 65; i++) {
            const x = ((i * 137.5) % W);
            const y = (i * 71.3) % (ground * .68);
            ctx.globalAlpha = .25 + .55 * Math.abs(Math.sin(time * .7 + i));
            circle(x, y, i % 8 === 0 ? 1.5 : .7, '#c7f4ff');
        }
        ctx.globalAlpha = 1;

        // Far mountains
        ctx.beginPath();
        ctx.moveTo(0, ground);
        for (let x = 0; x <= W + 30; x += 30) {
            const y = ground - 65 -
                Math.sin(x * .011 + time * .07) * 26 -
                Math.sin(x * .023) * 16;
            ctx.lineTo(x, y);
        }
        ctx.lineTo(W, ground);
        ctx.closePath();
        ctx.fillStyle = '#142b40';
        ctx.fill();

        // Moving dunes
        ctx.beginPath();
        ctx.moveTo(0, ground);
        for (let x = 0; x <= W + 20; x += 20) {
            const y = ground - 20 -
                Math.sin(x * .009 + time * .35) * 15;
            ctx.lineTo(x, y);
        }
        ctx.lineTo(W, ground);
        ctx.closePath();
        ctx.fillStyle = '#203448';
        ctx.fill();

        // Ground
        ctx.fillStyle = '#0b1723';
        ctx.fillRect(0, ground, W, H - ground);

        ctx.strokeStyle = '#63f5ff';
        ctx.shadowBlur = 12;
        ctx.shadowColor = '#63f5ff';
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(0, ground);
        ctx.lineTo(W, ground);
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Moving ground marks
        ctx.strokeStyle = '#345166';
        ctx.lineWidth = 2;
        const offset = (time * speed * .65) % 80;
        for (let x = -80 + offset; x < W; x += 80) {
            ctx.beginPath();
            ctx.moveTo(x, ground + 20);
            ctx.lineTo(x + 30, ground + 20);
            ctx.stroke();
        }

        // Distant illuminated city
        for (let i = 0; i < 18; i++) {
            const x = ((i * 91 - time * 15) % (W + 100) + W + 100) % (W + 100);
            const bh = 15 + (i * 17 % 37);
            ctx.fillStyle = '#101e30';
            ctx.fillRect(x, ground - bh, 18 + (i % 3) * 7, bh);
            if (i % 3 === 0) {
                ctx.fillStyle = '#63f5ff77';
                ctx.fillRect(x + 5, ground - bh + 7, 2, 3);
            }
        }
    }

    function drawDino() {
        const x = dino.x, y = dino.y;
        const h = dino.h, w = dino.w;
        ctx.save();
        ctx.translate(x, y);

        ctx.shadowColor = '#63f5ff';
        ctx.shadowBlur = 14;
        ctx.fillStyle = '#b5faff';

        // Tail
        ctx.beginPath();
        ctx.moveTo(3, h * .62);
        ctx.lineTo(-9, h * .55);
        ctx.lineTo(-4, h * .72);
        ctx.lineTo(4, h * .75);
        ctx.fill();

        // Body
        ctx.fillRect(4, h * .35, w - 9, h * .48);

        // Neck and head
        ctx.fillRect(w - 17, h * .12, 11, h * .43);
        ctx.fillRect(w - 19, h * .05, 19, h * .32);

        // Eye
        ctx.shadowBlur = 0;
        circle(w - 5, h * .14, 2, '#07111b');

        // Legs animate while running
        const step = running && dino.onGround ? Math.sin(time * 23) * 6 : 0;
        ctx.fillStyle = '#78dce9';
        if (duck) {
            ctx.fillRect(5, h * .62, w - 4, h * .23);
            ctx.fillRect(9, h * .8, 7, h * .16);
            ctx.fillRect(24, h * .8, 7, h * .16);
        } else {
            ctx.fillRect(7, h * .72, 8, h * .25 + step);
            ctx.fillRect(23, h * .72, 8, h * .25 - step);
            ctx.fillRect(5, h * .93 + step, 12, 3);
            ctx.fillRect(21, h * .93 - step, 12, 3);
        }
        ctx.restore();
    }

    function drawCactus(o) {
        const x = o.x, y = o.y, h = o.h, w = o.w;
        ctx.save();
        ctx.shadowColor = '#ff9e55';
        ctx.shadowBlur = 12;
        ctx.fillStyle = '#ff9e55';
        ctx.fillRect(x + w * .35, y - h, w * .32, h);
        ctx.fillRect(x, y - h * .58, w * .38, h * .12);
        ctx.fillRect(x, y - h * .58, w * .13, h * .25);
        ctx.fillRect(x + w * .58, y - h * .75, w * .34, h * .12);
        ctx.fillRect(x + w * .79, y - h * .75, w * .13, h * .25);
        ctx.restore();
    }

    function drawBird(o) {
        const flap = Math.sin(time * 15) * 9;
        ctx.save();
        ctx.strokeStyle = '#ffbf82';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#ff9e55';
        ctx.shadowBlur = 9;
        ctx.beginPath();
        ctx.moveTo(o.x, o.y);
        ctx.lineTo(o.x + 12, o.y - flap);
        ctx.lineTo(o.x + 23, o.y);
        ctx.lineTo(o.x + 34, o.y - flap);
        ctx.lineTo(o.x + 43, o.y);
        ctx.stroke();
        ctx.restore();
    }

    function draw() {
        drawBackground();
        obstacles.forEach(o => o.type === 'bird' ? drawBird(o) : drawCactus(o));
        if (!dead || running) drawDino();

        particles.forEach(p => {
            ctx.globalAlpha = Math.max(0, p.life);
            circle(p.x, p.y, 2.5, '#63f5ff');
        });
        ctx.globalAlpha = 1;

        if (flash > 0) {
            ctx.fillStyle = `rgba(255,90,70,${Math.min(.3, flash)})`;
            ctx.fillRect(0, 0, W, H);
        }
    }

    function loop(now) {
        if (!running) return;
        const dt = Math.min((now - last) / 1000, .035);
        last = now;
        time += dt;
        score += dt * speed * .06;
        speed = Math.min(760, 360 + score * .45);

        scoreEl.textContent = fmt(score);
        spawn -= dt;
        if (spawn <= 0) spawnObstacle();

        dino.h = duck && dino.onGround ? 29 : 48;
        if (dino.onGround) dino.y = ground - dino.h;
        else {
            dino.vy += gravity * dt;
            dino.y += dino.vy * dt;
            if (dino.y >= ground - dino.h) {
                dino.y = ground - dino.h;
                dino.vy = 0;
                dino.onGround = true;
            }
        }

        obstacles.forEach(o => {
            o.x -= speed * dt;
            if (o.type === 'bird') o.wing += dt * 10;
        });
        obstacles = obstacles.filter(o => o.x + o.w > -20);

        particles.forEach(p => {
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.vy += 500 * dt;
            p.life -= dt;
        });
        particles = particles.filter(p => p.life > 0);
        flash = Math.max(0, flash - dt);

        // Collision hitboxes
        const dx = dino.x + 7, dy = dino.y + 5;
        const dw = dino.w - 12, dh = dino.h - 8;

        for (const o of obstacles) {
            const oy = o.type === 'bird' ? o.y - 8 : o.y - o.h;
            const oh = o.type === 'bird' ? 20 : o.h;
            if (dx + dw > o.x + 4 && dx < o.x + o.w - 4 &&
                dy + dh > oy + 3 && dy < oy + oh) {
                endGame();
                return;
            }
        }

        draw();
        requestAnimationFrame(loop);
    }

    startBtn.addEventListener('click', start);

    document.addEventListener('keydown', e => {
        if (['Space', 'ArrowUp', 'ArrowDown'].includes(e.code)) {
            e.preventDefault();
        }
        if (e.code === 'Space' || e.code === 'ArrowUp') {
            if (!e.repeat) jump();
        }
        if (e.code === 'ArrowDown') duck = true;
    });

    document.addEventListener('keyup', e => {
        if (e.code === 'ArrowDown') duck = false;
    });

    canvas.addEventListener('pointerdown', e => {
        e.preventDefault();
        jump();
    });

    window.addEventListener('resize', resize);

    // Initial title screen
    resize();
    draw();
})();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(debug=True)

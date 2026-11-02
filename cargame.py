

from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>APEX RUSH 3D</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.152.2/three.min.js"></script>

<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#030813;color:white;font-family:Arial;overflow:hidden}
#game{position:fixed;inset:0;z-index:0}
canvas{display:block}
button{cursor:pointer;font-family:inherit;touch-action:manipulation}
.hud{position:absolute;z-index:3;top:20px;left:22px;right:22px;
display:flex;justify-content:space-between;align-items:center;pointer-events:none}
.logo{font-size:25px;font-weight:900;letter-spacing:4px}
.cyan{color:#54dfff}
.panel{background:#071526dc;border:1px solid #24536b;
border-radius:12px;padding:12px 20px}
.small{font-size:11px;letter-spacing:2px;color:#91a9c5}
.big{font-size:23px;font-weight:bold;margin-top:5px}
#progressBox{position:absolute;z-index:3;top:105px;left:24px;width:180px;pointer-events:none}
.track{height:5px;background:#263a4b;margin-top:8px;border-radius:5px}
#progress{height:5px;background:#51ddff;width:0%;border-radius:5px}
#environment{font-size:11px;color:#9cd9ed;margin-top:8px;letter-spacing:2px}
#pause{position:absolute;z-index:5;right:24px;top:105px;
background:#071526e8;color:white;border:1px solid #54dfff;
padding:10px 18px;border-radius:8px}
#overlay{position:absolute;z-index:10;inset:0;display:flex;
align-items:center;justify-content:center;padding:15px;
background:linear-gradient(90deg,#030813ef,#03081380,#030813e8)}
#overlay.hidden{display:none!important}
.menu{width:min(900px,100%);text-align:center;padding:45px 25px;
border:1px solid #24536b;border-radius:28px;background:#07101eeF;
box-shadow:0 0 80px #00bfff16}
h1{font-size:clamp(42px,8vw,100px);font-weight:1000;letter-spacing:6px}
.menu p{color:#a6b5cb;font-size:clamp(13px,2vw,22px);
line-height:1.8;margin:20px auto;max-width:750px}
.levels{display:flex;justify-content:center;gap:12px;
flex-wrap:wrap;margin:28px 0}
.level{border:1px solid #29465e;border-radius:13px;padding:17px 20px;
min-width:160px;color:#b8cce0}
.level strong{display:block;color:#58dcff;margin-bottom:8px}
.level.active{border-color:#4de3ff;background:#102a40}
#startBtn{background:linear-gradient(110deg,#55c9f6,#3175f4);
color:white;border:0;border-radius:12px;padding:19px 42px;
font-size:20px;font-weight:900;letter-spacing:3px;
box-shadow:0 0 25px #168cff35}
#startBtn:hover{filter:brightness(1.15);transform:scale(1.04)}
#startBtn:focus-visible,#pause:focus-visible,.control:focus-visible{
outline:3px solid white;outline-offset:4px}
#message{color:#54e1ff;margin-top:22px;font-size:14px}
.controls{position:absolute;z-index:5;bottom:22px;left:0;right:0;
display:flex;justify-content:space-between;padding:0 28px;pointer-events:none}
.control{width:68px;height:68px;border-radius:50%;pointer-events:auto;
background:#061b32d9;color:white;border:1px solid #42dfff;font-size:27px;
user-select:none;-webkit-user-select:none}
.control:active{background:#0875a9}
@media(max-width:600px){
.hud{top:10px;left:10px;right:10px}
.logo{font-size:15px;letter-spacing:2px}
.panel{padding:8px 10px}
.big{font-size:16px}
#progressBox{top:75px;left:12px}
#pause{top:75px;right:12px}
.menu{padding:28px 12px}
.level{min-width:130px;padding:12px}
.controls{padding:0 18px;bottom:12px}
.control{width:58px;height:58px}
}
</style>
</head>

<body>
<div id="game"></div>

<div class="hud">
  <div class="logo">APEX <span class="cyan">RUSH</span></div>
  <div class="panel">
    <div class="small">SPEED</div>
    <div class="big"><span id="speed">0</span> KM/H</div>
  </div>
  <div class="panel">
    <div class="small">DISTANCE</div>
    <div class="big"><span id="distance">0</span> M</div>
  </div>
</div>

<div id="progressBox">
  <div class="small">LEVEL PROGRESS</div>
  <div class="track"><div id="progress"></div></div>
  <div id="environment">SNOW MOUNTAIN</div>
</div>

<button id="pause" type="button">Ⅱ PAUSE</button>

<div class="controls">
  <button class="control" id="left" type="button">◀</button>
  <button class="control" id="right" type="button">▶</button>
</div>

<div id="overlay">
  <div class="menu">
    <h1>APEX <span class="cyan">RUSH</span></h1>
    <p id="description">
      ENTER THE WORLD OF EXTREME SUPERCAR RACING.
      THREE WORLDS. THREE MACHINES. ONE CHAMPION.
    </p>

    <div class="levels">
      <div class="level active" id="card1">
        <strong>01 / FROST BLADE</strong>SNOW
      </div>
      <div class="level" id="card2">
        <strong>02 / DIRT DOMINATOR</strong>MUD
      </div>
      <div class="level" id="card3">
        <strong>03 / PHANTOM X</strong>HIGHWAY
      </div>
    </div>

    <button id="startBtn" type="button">START ENGINE</button>
    <div id="message">ARROW KEYS / A-D TO DRIVE • AVOID OBSTACLES</div>
  </div>
</div>

<script>
"use strict";

// ====================================
// APEX RUSH 3D
// ====================================

const $ = id => document.getElementById(id);

if (!window.THREE) {
    $("message").textContent =
        "Three.js could not load. Check your internet connection.";
    throw new Error("Three.js unavailable");
}

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9cb6cc);
scene.fog = new THREE.Fog(0x9cb6cc, 35, 145);

const camera = new THREE.PerspectiveCamera(
    65, innerWidth / innerHeight, .1, 500
);
camera.position.set(0, 6, 12);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    powerPreference:"high-performance"
});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
$("game").appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xcceaff,0x333344,2));

const sun = new THREE.DirectionalLight(0xffffff,2.5);
sun.position.set(-10,20,10);
sun.castShadow = true;
scene.add(sun);

const glow = new THREE.PointLight(0x00cfff,30,40);
glow.position.set(0,6,-10);
scene.add(glow);

// Materials

const roadMat = new THREE.MeshStandardMaterial({
    color:0x252b35,roughness:.9
});
const snowMat = new THREE.MeshStandardMaterial({color:0xd9e8f6});
const mudMat = new THREE.MeshStandardMaterial({color:0x49301e});
const nightMat = new THREE.MeshStandardMaterial({color:0x101c29});
const tireMat = new THREE.MeshStandardMaterial({color:0x080a0d});
const glassMat = new THREE.MeshPhysicalMaterial({
    color:0x071a31,metalness:.8,roughness:.12
});

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(400,500),snowMat
);
ground.rotation.x=-Math.PI/2;
ground.position.set(0,-.12,-180);
scene.add(ground);

const road = new THREE.Mesh(
    new THREE.PlaneGeometry(12,500),roadMat
);
road.rotation.x=-Math.PI/2;
road.position.set(0,0,-180);
road.receiveShadow=true;
scene.add(road);

// Road markings

const marks=[];
for(let i=0;i<45;i++){
    for(const x of [-2,2]){
        const m=new THREE.Mesh(
            new THREE.BoxGeometry(.09,.025,4),
            new THREE.MeshBasicMaterial({color:0xffffff})
        );
        m.position.set(x,.035,-i*10);
        scene.add(m);
        marks.push(m);
    }
}

// Road barriers

for(const x of [-6.15,6.15]){
    const rail=new THREE.Mesh(
        new THREE.BoxGeometry(.2,.45,500),
        new THREE.MeshStandardMaterial({color:0x456178})
    );
    rail.position.set(x,.22,-180);
    scene.add(rail);
}

// ====================================
// PROCEDURAL SUPERCARS
// ====================================

const colors=[0xc4eaff,0xff681f,0xe51e45];

function makeCar(color,level){

    const car=new THREE.Group();

    const paint=new THREE.MeshPhysicalMaterial({
        color,metalness:.8,roughness:.18,
        clearcoat:1,clearcoatRoughness:.08
    });

    function part(w,h,d,mat,x,y,z){
        const mesh=new THREE.Mesh(
            new THREE.BoxGeometry(w,h,d),mat
        );
        mesh.position.set(x,y,z);
        mesh.castShadow=true;
        car.add(mesh);
        return mesh;
    }

    // Main chassis
    part(1.9,.48,3.8,paint,0,.65,0);

    // Front nose
    part(1.65,.23,1.3,paint,0,.52,-2);

    // Cockpit
    part(1.42,.56,1.65,glassMat,0,1.1,-.15);

    // Rear spoiler
    part(2.05,.12,.3,paint,0,1.13,1.75);

    // Sporty side panels
    for(const x of [-.94,.94]){
        part(.12,.22,2.4,paint,x,.45,.05);
    }

    // Wheels
    const wheels=[];
    for(const x of [-1,1]){
        for(const z of [-1.25,1.25]){
            const wheel=new THREE.Mesh(
                new THREE.CylinderGeometry(.4,.4,.24,24),
                tireMat
            );
            wheel.rotation.z=Math.PI/2;
            wheel.position.set(x,.4,z);
            wheel.castShadow=true;
            car.add(wheel);
            wheels.push(wheel);
        }
    }

    // Headlights and rear lamps
    for(const x of [-.62,.62]){
        part(.45,.1,.08,
            new THREE.MeshBasicMaterial({color:0x8ceeff}),
            x,.65,-2.08);
    }

    part(1.3,.12,.08,
        new THREE.MeshBasicMaterial({color:0xff143c}),
        0,.7,1.96);

    // Level-specific extra details
    if(level===2){
        part(.25,.45,.6,paint,-.8,1.15,.9);
        part(.25,.45,.6,paint,.8,1.15,.9);
    }
    if(level===3){
        part(2.15,.09,.4,paint,0,1.4,1.7);
    }

    const underglow=new THREE.PointLight(color,15,6);
    underglow.position.y=.2;
    car.add(underglow);

    car.position.set(0,0,5);
    car.userData.wheels=wheels;
    return car;
}

let player=makeCar(colors[0],1);
scene.add(player);

// ====================================
// SCENERY
// ====================================

const scenery=[];

function makeTree(x,z){

    const group=new THREE.Group();

    const trunk=new THREE.Mesh(
        new THREE.CylinderGeometry(.15,.22,2,8),
        new THREE.MeshStandardMaterial({color:0x493322})
    );
    trunk.position.y=1;
    group.add(trunk);

    const leaves=new THREE.Mesh(
        new THREE.ConeGeometry(1.1,3,8),
        new THREE.MeshStandardMaterial({color:0xe4efff})
    );
    leaves.position.y=3;
    group.add(leaves);

    group.position.set(x,0,z);
    scene.add(group);
    scenery.push(group);
}

for(let i=0;i<45;i++){
    makeTree(-10,-i*10);
    makeTree(10,-i*10);
}

// ====================================
// LEVELS
// ====================================

let level=1;
const LEVEL_DISTANCE=900;

function setEnvironment(){

    const env=[
        {
            bg:0x9cb6cc,
            fog:0xb8d2e8,
            ground:snowMat,
            name:"❄ SNOW MOUNTAIN"
        },
        {
            bg:0x514335,
            fog:0x756047,
            ground:mudMat,
            name:"MUD OFF-ROAD"
        },
        {
            bg:0x050719,
            fog:0x11152e,
            ground:nightMat,
            name:"NEON HIGHWAY"
        }
    ][level-1];

    scene.background.set(env.bg);
    scene.fog.color.set(env.fog);
    ground.material=env.ground;
    $("environment").textContent=env.name;

    for(let i=1;i<=3;i++){
        $("card"+i).classList.toggle("active",i===level);
    }
}

function upgradeCar(n){

    level=n;
    scene.remove(player);
    player=makeCar(colors[level-1],level);
    scene.add(player);

    setEnvironment();

    $("message").textContent=
        "NEW SUPERCAR UNLOCKED: "+
        ["FROST BLADE","DIRT DOMINATOR","PHANTOM X"][level-1];
}

function updateLevel(){

    const next=Math.min(3,Math.floor(distance/LEVEL_DISTANCE)+1);

    if(next!==level) upgradeCar(next);

    const progress=Math.min(
        100,(distance%LEVEL_DISTANCE)/LEVEL_DISTANCE*100
    );
    $("progress").style.width=progress+"%";

    if(level===3){
        $("progress").style.width=
            Math.min(100,(distance-1800)/LEVEL_DISTANCE*100)+"%";
    }
}

// ====================================
// OBSTACLES
// ====================================

let obstacles=[];

function spawnObstacle(){

    const group=new THREE.Group();

    const color=level===1?0x9ac9ee:
                level===2?0x9b572c:0xff304f;

    const block=new THREE.Mesh(
        new THREE.BoxGeometry(1.5,1.3,1.7),
        new THREE.MeshStandardMaterial({
            color,metalness:.45,roughness:.4
        })
    );

    block.position.y=.7;
    block.castShadow=true;
    group.add(block);

    const lamp=new THREE.PointLight(0xff254c,4,5);
    lamp.position.y=1.5;
    group.add(lamp);

    group.position.set(
        [-3,0,3][Math.floor(Math.random()*3)],
        0,-120
    );

    scene.add(group);
    obstacles.push(group);
}

function hit(a,b){
    return Math.abs(a.position.x-b.position.x)<1.45 &&
           Math.abs(a.position.z-b.position.z)<2.3;
}

// ====================================
// INPUT SYSTEM
// ====================================

let lane=0;
let running=false;
let paused=false;
let distance=0;
let speed=0;
let spawnTimer=0;
let lastTime=0;
let animationId=null;

function left(){
    if(!running||paused)return;
    lane=Math.max(-1,lane-1);
}

function right(){
    if(!running||paused)return;
    lane=Math.min(1,lane+1);
}

function onKeyDown(e){

    if(["ArrowLeft","ArrowRight"," "].includes(e.key)){
        e.preventDefault();
    }

    if(e.repeat)return;

    if(e.key==="ArrowLeft"||e.key.toLowerCase()==="a")left();
    if(e.key==="ArrowRight"||e.key.toLowerCase()==="d")right();

    if(e.code==="Space"){
        if(!running && !paused) startGame();
        else if(running) pauseGame();
        else if(paused) resumeGame();
    }
}

window.addEventListener("keydown",onKeyDown);

function bindControl(id,action){

    const button=$(id);

    button.addEventListener("pointerdown",e=>{
        e.preventDefault();
        action();
    });
}

bindControl("left",left);
bindControl("right",right);

// ====================================
// GAME FLOW
// ====================================

function clearObstacles(){
    obstacles.forEach(o=>scene.remove(o));
    obstacles=[];
}

function startGame(){

    if(running)return;

    clearObstacles();

    distance=0;
    speed=0;
    lane=0;
    level=1;
    spawnTimer=0;

    scene.remove(player);
    player=makeCar(colors[0],1);
    scene.add(player);

    setEnvironment();

    running=true;
    paused=false;

    $("overlay").classList.add("hidden");
    $("startBtn").textContent="START ENGINE";
    $("startBtn").onclick=null;

    lastTime=performance.now();
}

function pauseGame(){

    if(!running)return;

    running=false;
    paused=true;

    showMenu("GAME PAUSED","Your race is waiting.","RESUME RACE");
}

function resumeGame(){

    if(!paused)return;

    paused=false;
    running=true;

    $("overlay").classList.add("hidden");
    lastTime=performance.now();
}

function showMenu(title,description,buttonText){

    $("overlay").classList.remove("hidden");
    $("overlay").querySelector("h1").innerHTML=title;
    $("description").textContent=description;
    $("startBtn").textContent=buttonText;
}

function finishGame(){

    if(!running)return;

    running=false;
    paused=false;

    fetch("/api/score",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            score:Math.floor(distance),
            level
        })
    }).catch(()=>{});

    showMenu(
        "RACE <span class='cyan'>OVER</span>",
        "DISTANCE: "+Math.floor(distance)+
        " METERS | LEVEL: "+level,
        "RACE AGAIN"
    );
}

// Explicit button handlers
$("startBtn").addEventListener("click",()=>{
    if(paused){
        resumeGame();
    }else{
        startGame();
    }
});

$("pause").addEventListener("click",()=>{
    if(running)pauseGame();
    else if(paused)resumeGame();
});

// ====================================
// ANIMATION LOOP
// ====================================

function animate(time){

    animationId=requestAnimationFrame(animate);

    if(!running){
        renderer.render(scene,camera);
        return;
    }

    const dt=Math.min((time-lastTime)/1000,.05);
    lastTime=time;

    // Acceleration
    const maxSpeed=[280,340,420][level-1];
    speed=Math.min(maxSpeed,speed+90*dt);

    const movement=speed*dt*.095;
    distance+=movement;

    updateLevel();

    // Player steering
    const targetX=lane*3;

    player.position.x+=(targetX-player.position.x)*8*dt;
    player.rotation.z=(targetX-player.position.x)*-.06;

    player.userData.wheels.forEach(w=>{
        w.rotation.x+=movement*.7;
    });

    // Road markings
    marks.forEach(m=>{
        m.position.z+=movement;
        if(m.position.z>10)m.position.z-=450;
    });

    // Scenery
    scenery.forEach(s=>{
        s.position.z+=movement;
        if(s.position.z>15){
            s.position.z=-430-Math.random()*30;
        }
    });

    // Spawn traffic
    spawnTimer+=dt;
    if(spawnTimer>Math.max(.55,1.5-level*.2)){
        spawnObstacle();
        spawnTimer=0;
    }

    // Obstacle movement
    for(let i=obstacles.length-1;i>=0;i--){

        const o=obstacles[i];
        o.position.z+=movement;

        if(hit(player,o)){
            finishGame();
            break;
        }

        if(o.position.z>15){
            scene.remove(o);
            obstacles.splice(i,1);
        }
    }

    // Camera follow
    camera.position.x+=(player.position.x*.35-camera.position.x)*4*dt;
    camera.position.y+=(6-camera.position.y)*2*dt;
    camera.lookAt(player.position.x*.25,1,-7);

    // HUD
    $("speed").textContent=Math.floor(speed);
    $("distance").textContent=Math.floor(distance);

    renderer.render(scene,camera);
}

function resize(){

    camera.aspect=innerWidth/innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth,innerHeight);
}

window.addEventListener("resize",resize);

// Initialize
setEnvironment();
requestAnimationFrame(animate);

</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/api/score", methods=["POST"])
def score():
    data = request.get_json(silent=True) or {}

    try:
        points = max(0, int(data.get("score", 0)))
        level = max(1, min(3, int(data.get("level", 1))))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid score"}), 400

    return jsonify({
        "status": "success",
        "score": points,
        "level": level
    })


@app.route("/api/health")
def health():
    return jsonify({"status": "APEX RUSH is running"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

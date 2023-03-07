
//import '/style.css';
import * as THREE from 'three';
import {OrbitControls} from 'https://unpkg.com/three@0.141.0/examples/jsm/controls/OrbitControls.js';

import { MathUtils } from 'three';

// Setup

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector('#bg'),
});

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(30);
camera.position.setX(-3);

renderer.render(scene, camera);

// Torus

const geometry = new THREE.TorusGeometry(10, 3, 16, 100);
const material = new THREE.MeshStandardMaterial({ color: 0xff6347 });
const torus = new THREE.Mesh(geometry, material);

scene.add(torus);

//lights 
const pointLight = new THREE.PointLight(0xffffff)
pointLight.position.set(5,5,5)

const ambientLight = new THREE.AmbientLight(0xffffff)

scene.add(pointLight, ambientLight)

//helpers

const gridhelper = new THREE.GridHelper(200,50)
//scene.add(gridhelper)
const lightHelper = new THREE.PointLightHelper(pointLight)

//const controls = new OrbitControls(camera, renderer.domElement);


const spaceTexture = new THREE.TextureLoader().load('/static/images/skytrimsky.png')
scene.background = spaceTexture

function addStar(){
  const geometry = new THREE.SphereGeometry(0.25, 24, 24);
  const material = new THREE.MeshStandardMaterial({color: 0xffffff})
  const star = new THREE.Mesh(geometry, material)
  const [x,y,z] = Array(3).fill().map(()=> THREE.MathUtils.randFloatSpread(100))
  star.position.set(x,y,z)
  scene.add(star)
}
Array(200).fill().forEach(addStar)
//moon

const moonTexture = new THREE.TextureLoader().load("/static/images/moon.jpg")
const normalTexture = new THREE.TextureLoader().load("/static/images/normal.jpg")

const moon = new THREE.Mesh(
  new THREE.SphereGeometry(3,32,32),
  new THREE.MeshStandardMaterial({
    map:moonTexture,
    normalMap:normalTexture
  })
)
moon.position.z = 30
moon.position.x = -10

scene.add(moon)
//box
const boxTexture = new THREE.TextureLoader().load("static/images/ell.png")
const box = new THREE.Mesh(
  new THREE.BoxGeometry(2.5,2.5,2.5),
  new THREE.MeshBasicMaterial({map:boxTexture})
)

scene.add(box)
box.position.x = 2
box.position.y = 1
box.position.z = -5
function moveCamera() {
  const t = document.body.getBoundingClientRect().top;
  moon.rotation.x += 0.05;
  moon.rotation.y += 0.075;
  moon.rotation.z += 0.05;
  
  box.rotation.x +=0.01
  box.rotation.y +=0.001

  camera.position.z = t * -.01;
  camera.position.x = t * -0.0002;
  camera.rotation.y = t * -0.0002;
}

document.body.onscroll = moveCamera;
moveCamera();

function animate() {
  requestAnimationFrame(animate);

  torus.rotation.x += 0.01;
  torus.rotation.y += 0.005;
  //torus.rotation.z += 0.01;
  //moon.rotation.x += 0.005;

  //controls.update();
  renderer.render(scene, camera);
}

animate();
// const raycaster = new THREE.Raycaster();
// const clickMouse = new THREE.Vector2();
// const moveMouse = new THREE. Vector2();
// var clickable = THREE.Object3D;

// window.addEventListener('click', event => {
//   clickMouse.x = (event.clientX / window.innerWidth)*2 -1;
//   clickMouse.y = -(event.clientY / window.innerHeight)*2 -1;
//   raycaster.setFromCamera(clickMouse, camera)
//   const found = raycaster.intersectObjects(scene.children);

//   if (found.length > 0 && found[0].object==box ){

//   }
  
  
// })


// Create a THREE.js scene
//const scene = new THREE.Scene();

// Create a camera and set its position
//const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
// camera.position.set(0, 0, 5);

// // Create a renderer and set its size
// //const renderer = new THREE.WebGLRenderer();
// //renderer.setSize(window.innerWidth, window.innerHeight);
// //document.body.appendChild(renderer.domElement);

// // Create a particle system with a single particle
// const particleGeometry = new THREE.Geometry();
// particleGeometry.vertices.push(new THREE.Vector3(0, 0, 0));
// const particleMaterial = new THREE.PointsMaterial({
//   color: 0xffffff,
//   size: 0.05,
// });
// const particleSystem = new THREE.Points(particleGeometry, particleMaterial);
// scene.add(particleSystem);

// // Define the vertex shader
// const vertexShader = `
//   uniform float time;
//   uniform vec2 resolution;

//   void main() {
//     vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
//     gl_PointSize = 10.0 * (1.0 / -mvPosition.z);
//     gl_Position = projectionMatrix * mvPosition;
//   }
// `;

// // Define the fragment shader
// const fragmentShader = `
//   uniform float time;
//   uniform vec2 resolution;

//   void main() {
//     vec2 p = (gl_FragCoord.xy * 2.0 - resolution.xy) / min(resolution.x, resolution.y);
//     float aspectRatio = resolution.x / resolution.y;

//     float intensity = 0.3;
//     float glow = 0.1;

//     for (int i = 0; i < 10; i++) {
//       float t = time * (1.0 - float(i) / 10.0);
//       vec2 q = vec2(2.0, 1.0) * p.xy * (i / 10.0);
//       float c = sin(dot(q, q) + t) / length(q + vec2(cos(t), sin(t)));
//       intensity += c;
//     }

//     vec3 color = vec3(0.8, 0.9, 1.0) * intensity;
//     gl_FragColor = vec4(color, glow);
//   }
// `;

// // Create a shader material with the vertex and fragment shaders
// const shaderMaterial = new THREE.ShaderMaterial({
//   uniforms: {
//     time: { value: 0 },
//     resolution: { value: new THREE.Vector2() },
//   },
// });

// // Set the shaders on the particle material
// particleSystem.material = shaderMaterial;
// shaderMaterial.vertexShader = vertexShader;
// shaderMaterial.fragmentShader = fragmentShader;

// // Update the shader resolution uniform when the window is resized
// window.addEventListener('resize', () => {
//   renderer.setSize(window.innerWidth, window.innerHeight);
//   shaderMaterial.uniforms.resolution.value.x = renderer.domElement.width;
//   shaderMaterial.uniforms.resolution.value.y = renderer.domElement.height;
// });

// // Animate the particles
// function animateParticles() {
//   requestAnimationFrame(animateParticles);

//   const time = Date.now() * 0.001;
//   shaderMaterial.uniforms.time.value = time;

//   renderer.render(scene, camera);
// }

// animateParticles();

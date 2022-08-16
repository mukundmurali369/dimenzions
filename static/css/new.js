import gsap from "https://cdn.skypack.dev/gsap";

const canvas = document.getElementById("globe");

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);

const renderer = new THREE.WebGLRenderer({
  antialias: true,
  alpha: true,
});

renderer.setClearColor( 0xffffff, 0);
renderer.setSize(500,500);
renderer.setPixelRatio(devicePixelRatio);

const container = document.getElementById('globe-container');

container.appendChild(renderer.domElement);

const sphereGeom = new THREE.SphereGeometry(5,50,50);

const globe_image = new THREE.TextureLoader().load("https://i.postimg.cc/0Ndr7GpN/earth-world-map-3d-model-low-poly-max-obj-fbx-c4d-ma-blend.jpg");

const sphereMat = new THREE.ShaderMaterial({
	vertexShader: document.getElementById('vertexShader').textContent,
	fragmentShader: document.getElementById('fragmentShader').textContent,
	uniforms: {
		globeTexture: {
			value: globe_image,
		}
	}
});

const sphere = new THREE.Mesh(
  sphereGeom, sphereMat
);

const outerGlowMat = new THREE.ShaderMaterial({
	vertexShader: document.getElementById('atmosphereVertexShader').textContent,
	fragmentShader: document.getElementById('atmosphereFragmentShader').textContent,
	side: THREE.BackSide
});

const outer_glow = new THREE.Mesh(
	sphereGeom, outerGlowMat
);

outer_glow.scale.set(1.01, 1.01, 1.01);

console.log(sphere);

scene.add(outer_glow);

const group = new THREE.Group();
group.add(sphere);
scene.add(group);

camera.position.z = 10;

const mouse = {
	x: 0,
	y: 0
}

function animate(){
  requestAnimationFrame(animate)
  renderer.render(scene, camera);
	sphere.rotation.y -= 0.002;
	sphere.rotation.z -= 0.002;
	var scale = Math.random() * (1.013 - 1.01) + 1.015;
	outer_glow.scale.set(scale, scale, scale);

	gsap.to(group.rotation, {
		y: mouse.x * 0.1,
		x: -mouse.y * 0.1,
	});
}
animate();

addEventListener('mousemove', () => {
	mouse.x = (event.clientX / innerWidth) *  2 - 1;
	mouse.y = -(event.clientY / innerHeight) *  2 - 1;
})


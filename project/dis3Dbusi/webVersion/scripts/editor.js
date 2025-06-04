// Guardar el estado actual en el historial
function saveToHistory() {
    // Guardar una copia profunda del estado actual
    const currentState = JSON.parse(JSON.stringify(currentMetadata));
    
    // Añadir al historial
    undoStack.push(currentState);
    
    // Limpiar el stack de rehacer cuando se realiza una nueva acción
    redoStack = [];
    
    // Limitar el tamaño del historial para evitar problemas de memoria
    if (undoStack.length > 50) {
        undoStack.shift();
    }
    
    // Actualizar la información en pantalla
    updateHistoryInfo();
}

// Deshacer la última acción
function undo() {
    if (undoStack.length === 0) return;
    
    // Marcar que estamos en una operación de deshacer/rehacer
    isUndoRedo = true;
    
    // Guardar el estado actual para poder rehacerlo
    redoStack.push(JSON.parse(JSON.stringify(currentMetadata)));
    
    // Recuperar el estado anterior
    currentMetadata = undoStack.pop();
    
    // Renderizar la escena con el estado recuperado
    renderFolder();
    
    // Fin de la operación de deshacer/rehacer
    isUndoRedo = false;
    
    // Actualizar la información en pantalla
    updateHistoryInfo();
}

// Rehacer la última acción deshecha
function redo() {
    if (redoStack.length === 0) return;
    
    // Marcar que estamos en una operación de deshacer/rehacer
    isUndoRedo = true;
    
    // Guardar el estado actual para poder deshacerlo
    undoStack.push(JSON.parse(JSON.stringify(currentMetadata)));
    
    // Recuperar el estado siguiente
    currentMetadata = redoStack.pop();
    
    // Renderizar la escena con el estado recuperado
    renderFolder();
    
    // Fin de la operación de deshacer/rehacer
    isUndoRedo = false;
    
    // Actualizar la información en pantalla
    updateHistoryInfo();
}

// Actualizar la información del historial en pantalla
function updateHistoryInfo() {
    const historyInfo = document.getElementById('history-info');
    if (historyInfo) {
        historyInfo.textContent = `Deshacer: ${undoStack.length} | Rehacer: ${redoStack.length}`;
    }
}import * as THREE from 'https://esm.sh/three';
import { OrbitControls } from 'https://esm.sh/three/examples/jsm/controls/OrbitControls.js';
import { TransformControls } from 'https://esm.sh/three/examples/jsm/controls/TransformControls.js';
import { createNodeObject3D } from './nodeObject3D.js';
import { createImagePlane } from './imageLoader.js';

// Variables globales
let scene, camera, renderer, orbitControls, transformControls;
let currentMetadata = null;
let nodeGroup = null;
let selectedObject = null;
let folderStructure = null;
let currentFolderPath = null;

// Variables para el historial
let undoStack = [];
let redoStack = [];
let isUndoRedo = false; // Flag para evitar añadir al historial durante operaciones de deshacer/rehacer

// Inicializar la escena
function initScene() {
    // Crear escena
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    
    // Crear cámara
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(30, 30, 30);
    
    // Crear renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth - 250, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
    
    // Añadir luces
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);
    
    // Controles de órbita
    orbitControls = new OrbitControls(camera, renderer.domElement);
    
    // Controles de transformación - Usando el método correcto
    transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.addEventListener('change', render);
    transformControls.addEventListener('dragging-changed', function(event) {
        orbitControls.enabled = !event.value;
        if (!event.value && selectedObject) {
            updateObjectTransform(selectedObject);
        }
    });
    
    // Eventos de teclado para cambiar modo del transformControl
    window.addEventListener('keydown', function(event) {
        // Manejar atajos de deshacer/rehacer
        if (event.ctrlKey) {
            switch (event.key.toLowerCase()) {
                case 'z':
                    event.preventDefault();
                    undo();
                    return;
                case 'y':
                    event.preventDefault();
                    redo();
                    return;
            }
        }
        
        switch (event.key.toLowerCase()) {
            case 'g':
            case 'w': // Añadido para mantener coherencia con el ejemplo
                transformControls.setMode('translate');
                render();
                break;
            case 'r':
            case 'e': // Añadido para mantener coherencia con el ejemplo
                transformControls.setMode('rotate');
                render();
                break;
            case 's': 
                transformControls.setMode('scale');
                render();
                break;
            case ' ': // Espacio para activar/desactivar los controles
                transformControls.enabled = !transformControls.enabled;
                render();
                break;
            case 'escape': // Resetear transformación
                if (selectedObject) {
                    // Guardar el estado actual antes de resetear
                    saveToHistory();
                    transformControls.reset();
                    updateObjectTransform(selectedObject);
                    render();
                }
                break;
        }
    });
    
    // Evento para redimensionar la ventana
    window.addEventListener('resize', function() {
        camera.aspect = (window.innerWidth - 250) / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth - 250, window.innerHeight);
    });
    
    // Evento para seleccionar objetos
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    
    renderer.domElement.addEventListener('click', function(event) {
        mouse.x = ((event.clientX - 250) / (window.innerWidth - 250)) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
        
        raycaster.setFromCamera(mouse, camera);
        
        if (nodeGroup) {
            const intersects = raycaster.intersectObjects(nodeGroup.children, true);
            
            if (intersects.length > 0) {
                const object = intersects[0].object;
                // Ignorar el plano base
                if (object !== nodeGroup.children[0]) { 
                    selectObject(object);
                }
            } else {
                // Deseleccionar si se hace clic en un espacio vacío
                if (selectedObject) {
                    transformControls.detach();
                    selectedObject = null;
                }
            }
        }
    });
    
    // Iniciar bucle de renderizado
    animate();
    
    // Añadir transformControls a la escena siguiendo el método del ejemplo
    const gizmo = transformControls.getHelper();
    scene.add(gizmo);
}

// Actualizar la transformación del objeto en los metadatos
function updateObjectTransform(object) {
    if (!currentMetadata || !currentMetadata.files) return;
    
    // Encontrar el índice del archivo en los metadatos
    const index = Array.from(nodeGroup.children).indexOf(object) - 1;
    if (index < 0 || index >= currentMetadata.files.length) return;
    
    // Guardar el estado actual en el historial antes de modificarlo
    if (!isUndoRedo) {
        saveToHistory();
    }
    
    const file = currentMetadata.files[index];
    
    // Crear o actualizar datos de transformación
    if (!file.data) file.data = {};
    
    // Guardar posición
    file.data.pos = [
        object.position.y,
        object.position.x,
        object.position.z
    ];
    
    // Convertir rotación de radianes a grados
    file.data.rot = [
        (object.rotation.y * 180) / Math.PI,
        (object.rotation.x * 180) / Math.PI,
        (object.rotation.z * 180) / Math.PI
    ];
    
    // Guardar escala (asumiendo escala uniforme)
    file.data.scale = object.scale.x;
}

// Seleccionar un objeto
function selectObject(object) {
    // Deseleccionar el objeto anterior si existe
    if (selectedObject) {
        transformControls.detach();
    }
    
    selectedObject = object;
    
    // Asegurarse de que el objeto sea válido antes de adjuntarlo
    if (object && object instanceof THREE.Object3D) {
        transformControls.attach(object);
        // Forzar un renderizado para que se muestren los controles inmediatamente
        render();
    } else {
        console.error('Error: No se pudo adjuntar el objeto al transformControls', object);
    }
}

// Función de animación
function animate() {
    requestAnimationFrame(animate);
    render();
}

// Función de renderizado
function render() {
    renderer.render(scene, camera);
}

// Cargar la estructura de carpetas
async function loadFolderStructure() {
    try {
        const response = await fetch('../estructura.json');
        folderStructure = await response.json();
        renderFolderStructure();
    } catch (error) {
        console.error('Error al cargar la estructura de carpetas:', error);
    }
}

// Renderizar la estructura de carpetas en el sidebar
function renderFolderStructure() {
    const folderStructureElement = document.getElementById('folder-structure');
    folderStructureElement.innerHTML = '';
    
    // Crear una estructura jerárquica a partir de las IDs de nodos
    const hierarchy = {};
    
    folderStructure.nodes.forEach(node => {
        const parts = node.id.split('/');
        let current = hierarchy;
        
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            if (!current[part]) {
                current[part] = {};
            }
            current = current[part];
        }
    });
    
    // Renderizar la jerarquía
    renderFolderHierarchy(hierarchy, folderStructureElement, '');
}

// Renderizar la jerarquía de carpetas recursivamente
function renderFolderHierarchy(hierarchy, element, path) {
    for (const key in hierarchy) {
        const newPath = path ? `${path}/${key}` : key;
        const folderElement = document.createElement('div');
        folderElement.className = 'folder';
        folderElement.textContent = key;
        folderElement.dataset.path = newPath; // Añadir atributo para identificar la ruta
        folderElement.addEventListener('click', () => loadFolder(newPath));
        element.appendChild(folderElement);
        
        if (Object.keys(hierarchy[key]).length > 0) {
            const subfolderElement = document.createElement('div');
            subfolderElement.className = 'subfolder';
            element.appendChild(subfolderElement);
            renderFolderHierarchy(hierarchy[key], subfolderElement, newPath);
        }
    }
}

// Cargar una carpeta específica
async function loadFolder(path) {
    try {
        // Actualizar el indicador de carpeta actual
        document.getElementById('current-folder').textContent = `Carpeta actual: ${path}`;
        
        // Resaltar la carpeta seleccionada en el panel lateral
        const folderElements = document.querySelectorAll('.folder');
        folderElements.forEach(el => {
            el.classList.remove('selected');
            if (el.dataset.path === path) {
                el.classList.add('selected');
            }
        });
        
        currentFolderPath = path;
        const response = await fetch(`/data/${path}/metadata.json`);
        currentMetadata = await response.json();
        
        // Limpiar el historial al cargar una nueva carpeta
        undoStack = [];
        redoStack = [];
        
        renderFolder();
        updateHistoryInfo();
    } catch (error) {
        console.error(`Error al cargar la carpeta ${path}:`, error);
    }
}

// Renderizar los contenidos de la carpeta en la escena 3D
function renderFolder() {
    // Limpiar la escena
    if (nodeGroup) {
        scene.remove(nodeGroup);
        // Deseleccionar cualquier objeto seleccionado actualmente
        if (selectedObject) {
            transformControls.detach();
            selectedObject = null;
        }
    }
    
    // Crear nuevo grupo de nodos
    nodeGroup = createNodeObject3D(currentMetadata);
    scene.add(nodeGroup);
    
    // Ajustar la cámara para ver todo el contenido
    fitCameraToObject(nodeGroup);
}

// Ajustar la cámara para ver todo el contenido
function fitCameraToObject(object, offset = 1.2) {
    const boundingBox = new THREE.Box3().setFromObject(object);
    const center = boundingBox.getCenter(new THREE.Vector3());
    const size = boundingBox.getSize(new THREE.Vector3());
    
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / (2 * Math.tan(fov / 2)));
    cameraZ *= offset;
    
    camera.position.set(center.x + cameraZ, center.y + cameraZ, center.z + cameraZ);
    camera.lookAt(center);
    orbitControls.target.copy(center);
    camera.updateProjectionMatrix();
    orbitControls.update();
}

// Guardar los cambios en el archivo metadata.json
function saveChanges() {
    if (!currentMetadata || !currentFolderPath) return;
    
    // Filtrar archivos que no tienen transformaciones
    currentMetadata.files.forEach(file => {
        if (file.data && Object.keys(file.data).length === 0) {
            delete file.data;
        }
    });
    
    // Crear el JSON resultante
    const jsonString = JSON.stringify(currentMetadata, null, 2);
    
    // Crear un enlace para descargar el archivo
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'metadata.json';
    document.body.appendChild(a);
    a.click();
    
    // Limpiar
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 0);
    
    console.log('JSON guardado:', jsonString);
}

// Inicializar todo
function init() {
    initScene();
    loadFolderStructure();
    
    // Inicializar el historial
    undoStack = [];
    redoStack = [];
    updateHistoryInfo();
    
    // Inicializar el indicador de carpeta actual
    document.getElementById('current-folder').textContent = 'Carpeta actual: Ninguna';
    
    // Añadir evento al botón de guardar
    document.getElementById('save-btn').addEventListener('click', saveChanges);
}

// Iniciar la aplicación
init();
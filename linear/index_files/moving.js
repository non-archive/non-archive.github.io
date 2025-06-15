// dynamic-agents.js
// Script para generar y animar agentes dinámicamente según la ruta actual

// Configuración de los agentes
const agentsConfig = [
    {
        id: 'linear',
        image: '/linear/index_files/jellyfish.png',
        title: 'Linear Character',
        description: 'Guides you through a structured narrative from beginning to end.',
        link: '/linear/'
    },
    {
        id: 'files',
        image: '/linear/index_files/moon.png',
        title: 'Files Character',
        description: 'Lets you freely explore raw project files and data sources.',
        link: '/files/'
    },
    {
        id: 'infrastructure',
        image: '/linear/index_files/hastag.png',
        title: 'Infrastructure Character',
        description: 'Reveals data relationships and connections between all involved agents.',
        link: '/infrastructure/'
    },
    {
        id: 'spatial',
        image: '/linear/index_files/contoller.png',
        title: 'Spatial',
        description: 'Organizes and animates data within a three-dimensional space.',
        link: '#'
    },
    {
        id: 'link',
        image: '/linear/index_files/links.png',
        title: 'Conections',
        description: 'Allows exploring connections between Ocean Archive data',
        link: '/project/oceanArchive/APIVisualization.html'
    }
];

// Configuración del movimiento
const moveSpeed = 0.5;
const changeDirectionChance = 0.01;
const maxTurnAngle = 0.1;

// Estado global
let agents = [];
let expandedAgent = null;
let isAnimating = true;
let playground, overlay;

// Función para obtener la ruta actual
function getCurrentPath() {
    return window.location.pathname;
}

// Función para crear el HTML de un agente
function createAgentHTML(config) {
    return `
        <div class="agent absolute h-40 aspect-square cursor-pointer z-30" data-agent-id="${config.id}">
            <img src="${config.image}" class="rotate-90 pointer-events-auto hover:scale-150 transition-all" />
            <div class="absolute top-4 left-4 text-xl pointer-events-auto">
                <h3 class="text-3xl mb-2 hidden agent-text">
                    <mark class="bg-white">${config.title}</mark>
                </h3>
                <p class="mb-6 hidden agent-text">
                    <mark class="bg-white">${config.description}</mark>
                </p>
                <a href="${config.link}" class="bg-white p-2 border hover:bg-blue-200 hidden agent-text">Access</a>
            </div>
        </div>
    `;
}

// Función para filtrar agentes según la ruta actual
function getFilteredAgents() {
    const currentPath = getCurrentPath();
    
    // Si estamos en la raíz, mostramos todos
    if (currentPath === '/' || currentPath === '') {
        return agentsConfig;
    }
    
    // Filtramos los agentes que no coincidan con la ruta actual
    return agentsConfig.filter(agent => {
        // Extraemos la ruta del enlace del agente
        const agentPath = agent.link.startsWith('/') ? agent.link : null;
        return agentPath !== currentPath;
    });
}

// Función para generar los agentes en el DOM
function generateAgents() {
    const filteredAgents = getFilteredAgents();
    
    // Limpiamos el playground
    playground.innerHTML = '';
    
    // Generamos cada agente
    filteredAgents.forEach(config => {
        playground.innerHTML += createAgentHTML(config);
    });
    
    // Actualizamos la referencia a los elementos del DOM
    agents = document.querySelectorAll('.agent');
    
    console.log(`Generados ${agents.length} agentes para la ruta: ${getCurrentPath()}`);
}

// Función para obtener un número aleatorio entre min y max
function random(min, max) {
    return Math.random() * (max - min) + min;
}

// Función para obtener las dimensiones del playground
function getPlaygroundBounds() {
    const rect = playground.getBoundingClientRect();
    return {
        width: rect.width,
        height: rect.height,
        left: rect.left,
        top: rect.top
    };
}

// Función para inicializar los agentes con posición y movimiento
function initializeAgents() {
    const bounds = getPlaygroundBounds();
    
    agents.forEach(agent => {
        // Posición inicial dentro del playground
        agent.x = random(0, bounds.width - 160);
        agent.y = random(0, bounds.height - 160);
        
        // Dirección aleatoria
        agent.angle = random(0, Math.PI * 2);
        agent.vx = Math.cos(agent.angle) * moveSpeed;
        agent.vy = Math.sin(agent.angle) * moveSpeed;
        
        // Estado del agente
        agent.isExpanded = false;
        
        // Posicionamos el agente
        agent.style.left = agent.x + 'px';
        agent.style.top = agent.y + 'px';
        
        // Event listener para expandir
        const img = agent.querySelector('img');
        if (img) {
            img.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                expandAgent(agent);
            });
        }
    });
}

// Función para expandir un agente
function expandAgent(agent) {
    if (expandedAgent) return;
    
    expandedAgent = agent;
    agent.isExpanded = true;
    isAnimating = false;
    
    // Mostramos el overlay
    overlay.classList.remove('hidden');
    
    // Creamos el botón de cerrar
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '×';
    closeButton.className = 'absolute -top-5 -right-5 text-6xl text-gray-700 hover:text-gray-900 z-50 w-10 h-10 flex items-center justify-center cursor-pointer';
    closeButton.addEventListener('click', closeAgent);
    agent.appendChild(closeButton);
    
    // Estilos de expansión
    agent.style.position = 'fixed';
    agent.style.top = '50%';
    agent.style.left = '50%';
    agent.style.transform = 'translate(-50%, -50%)';
    agent.style.width = '80%';
    agent.style.height = '80%';
    agent.style.maxWidth = '300px';
    agent.style.maxHeight = '600px';
    agent.style.zIndex = '60';
    agent.style.transition = 'all 0s ease';
    
    // Mostramos el texto
    const textElements = agent.querySelectorAll('.agent-text');
    textElements.forEach(el => el.classList.remove('hidden'));
    
    // Ajustamos la imagen
    const img = agent.querySelector('img');
    if (img) {
        img.style.height = '200px';
        img.style.width = '200px';
        img.style.margin = '0 auto 20px auto';
        img.style.pointerEvents = 'none';
    }
}

// Función para cerrar el agente expandido
function closeAgent() {
    if (!expandedAgent) return;
    
    overlay.classList.add('hidden');
    
    // Removemos el botón de cerrar
    const closeButton = expandedAgent.querySelector('button');
    if (closeButton) closeButton.remove();
    
    // Restauramos estilos originales
    expandedAgent.style.position = 'absolute';
    expandedAgent.style.width = '10rem';
    expandedAgent.style.height = '10rem';
    expandedAgent.style.maxWidth = '';
    expandedAgent.style.maxHeight = '';
    expandedAgent.style.zIndex = '';
    expandedAgent.style.transition = '';
    
    // Restauramos posición
    expandedAgent.style.left = expandedAgent.x + 'px';
    expandedAgent.style.top = expandedAgent.y + 'px';
    expandedAgent.style.transform = `rotate(${Math.atan2(expandedAgent.vy, expandedAgent.vx) * (180 / Math.PI)}deg)`;
    
    // Ocultamos el texto
    const textElements = expandedAgent.querySelectorAll('.agent-text');
    textElements.forEach(el => el.classList.add('hidden'));
    
    // Restauramos la imagen
    const img = expandedAgent.querySelector('img');
    if (img) {
        img.style.height = '';
        img.style.width = '';
        img.style.margin = '';
        img.style.pointerEvents = 'auto';
    }
    
    expandedAgent.isExpanded = false;
    expandedAgent = null;
    isAnimating = true;
}

// Función principal de animación
function animate() {
    if (isAnimating) {
        const bounds = getPlaygroundBounds();
        
        agents.forEach(agent => {
            if (agent.isExpanded) return;
            
            // Cambio ocasional de dirección
            if (Math.random() < changeDirectionChance) {
                agent.angle += random(-maxTurnAngle, maxTurnAngle);
                agent.vx = Math.cos(agent.angle) * moveSpeed;
                agent.vy = Math.sin(agent.angle) * moveSpeed;
            }
            
            // Movimiento
            agent.x += agent.vx;
            agent.y += agent.vy;
            
            // Wrapping (reaparece por el lado opuesto)
            if (agent.x > bounds.width) agent.x = -160;
            else if (agent.x < -160) agent.x = bounds.width;
            
            if (agent.y > bounds.height) agent.y = -160;
            else if (agent.y < -160) agent.y = bounds.height;
            
            // Aplicamos posición y rotación
            const visualAngle = Math.atan2(agent.vy, agent.vx) * (180 / Math.PI);
            agent.style.left = agent.x + 'px';
            agent.style.top = agent.y + 'px';
            agent.style.transform = `rotate(${visualAngle}deg)`;
        });
    }
    
    requestAnimationFrame(animate);
}

// Función de inicialización
function init() {
    playground = document.getElementById('playground');
    overlay = document.getElementById('overlay');
    
    if (!playground) {
        console.error('No se encontró el elemento #playground');
        return;
    }
    
    // Creamos el overlay si no existe
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'overlay';
        overlay.className = 'fixed inset-0 backdrop-blur-lg bg-opacity-50 z-20 hidden';
        document.body.appendChild(overlay);
    }
    
    // Event listener para cerrar al hacer clic en el overlay
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeAgent();
    });
    
    // Generamos e inicializamos los agentes
    generateAgents();
    initializeAgents();
    
    // Iniciamos la animación
    animate();
}

// Iniciamos cuando se carga la página
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
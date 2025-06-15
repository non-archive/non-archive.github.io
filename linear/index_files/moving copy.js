// agents-movement.js
// Script para hacer que los agentes se muevan aleatoriamente por la página

// Seleccionamos todos los agentes, el overlay y el playground
const agents = document.querySelectorAll('.agent');
const overlay = document.getElementById('overlay');
const playground = document.getElementById('playground');

// Configuración del movimiento
const moveSpeed = 0.5; // velocidad de movimiento
const changeDirectionChance = 0.01; // probabilidad de cambiar dirección
const maxTurnAngle = 0.1; // máximo ángulo de giro en radianes

// Estado global
let expandedAgent = null;
let isAnimating = true;

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

// Inicializamos cada agente con posición y dirección aleatoria
agents.forEach(agent => {
    const bounds = getPlaygroundBounds();
    
    // Posición inicial dentro del playground
    agent.x = random(0, bounds.width - 160);
    agent.y = random(0, bounds.height - 160);
    
    // En lugar de velocidades directas, usamos un ángulo de dirección
    agent.angle = random(0, Math.PI * 2); // ángulo en radianes
    agent.vx = Math.cos(agent.angle) * moveSpeed;
    agent.vy = Math.sin(agent.angle) * moveSpeed;
    
    // Guardamos la posición original para poder restaurarla
    agent.originalX = agent.x;
    agent.originalY = agent.y;
    agent.isExpanded = false;
    
    // Posicionamos el agente
    agent.style.left = agent.x + 'px';
    agent.style.top = agent.y + 'px';
    
    // Añadimos el event listener para el clic SOLO en el model-viewer
    const modelViewer = agent.querySelector('img');
    if (modelViewer) {
        modelViewer.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            expandAgent(agent);
        });
        // Habilitamos pointer events solo para el model-viewer cuando no está expandido
        modelViewer.style.pointerEvents = 'auto';
    }
});

// Función para expandir un agente
function expandAgent(agent) {
    if (expandedAgent) return; // Si ya hay uno expandido, no hacer nada
    
    expandedAgent = agent;
    agent.isExpanded = true;
    isAnimating = false; // Pausamos la animación
    
    // Mostramos el overlay
    overlay.classList.remove('hidden');
    
    // Creamos y añadimos el botón de cerrar
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '×';
    closeButton.className = 'absolute -top-5 -right-5 text-6xl text-gray-700 hover:text-gray-900 z-50 w-10 h-10 flex items-center justify-center cursor-pointer';
    closeButton.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        closeAgent();
    });
    agent.appendChild(closeButton);
    
    // Deshabilitamos el click en el model-viewer cuando está expandido
    const modelViewer = agent.querySelector('model-viewer');
    if (modelViewer) {
        modelViewer.style.pointerEvents = 'none';
    }
    
    // Aplicamos los estilos de expansión
    agent.style.position = 'fixed';
    agent.style.top = '50%';
    agent.style.left = '50%';
    agent.style.transform = 'translate(-50%, -50%)';
    agent.style.width = '80%';
    agent.style.height = '80%';
    agent.style.maxWidth = '300px';
    agent.style.maxHeight = '600px';
    agent.style.zIndex = '60'; // Mayor que el playground
    agent.style.transition = 'all 0s ease';
    
    // Mostramos el texto
    const textElements = agent.querySelectorAll('.agent-text');
    textElements.forEach(el => {
        el.classList.remove('hidden');
    });
    
    // Ajustamos el model-viewer para que sea más pequeño
    if (modelViewer) {
        modelViewer.style.height = '200px';
        modelViewer.style.width = '200px';
        modelViewer.style.margin = '0 auto 20px auto';
    }
    
    // Habilitamos los enlaces dentro del agente expandido
    const links = agent.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.stopPropagation(); // Evitamos que se cierre el modal
        });
    });
}

// Función para cerrar el agente expandido
function closeAgent() {
    if (!expandedAgent) return;
    
    // Ocultamos el overlay
    overlay.classList.add('hidden');
    
    // Removemos el botón de cerrar
    const closeButton = expandedAgent.querySelector('button');
    if (closeButton) {
        closeButton.remove();
    }
    
    // Restauramos los estilos originales
    expandedAgent.style.position = 'absolute';
    expandedAgent.style.width = '10rem'; // h-40 = 10rem
    expandedAgent.style.height = '10rem';
    expandedAgent.style.aspectRatio = '1';
    expandedAgent.style.backgroundColor = '';
    expandedAgent.style.padding = '';
    expandedAgent.style.borderRadius = '';
    expandedAgent.style.boxShadow = '';
    expandedAgent.style.zIndex = '';
    expandedAgent.style.maxWidth = '';
    expandedAgent.style.transition = '';
    
    // Restauramos la posición
    expandedAgent.style.left = expandedAgent.x + 'px';
    expandedAgent.style.top = expandedAgent.y + 'px';
    expandedAgent.style.transform = `rotate(${Math.atan2(expandedAgent.vy, expandedAgent.vx) * (180 / Math.PI)}deg)`;
    
    // Ocultamos el texto
    const textElements = expandedAgent.querySelectorAll('.agent-text');
    textElements.forEach(el => {
        el.classList.add('hidden');
    });
    
    // Marcamos como no expandido
    expandedAgent.isExpanded = false;
    expandedAgent = null;
    
    // Reanudamos la animación
    isAnimating = true;
}

// Event listener para cerrar al hacer clic en el overlay
overlay.addEventListener('click', (e) => {
    // Solo cerramos si el click fue directamente en el overlay, no en sus hijos
    if (e.target === overlay) {
        closeAgent();
    }
});

// Función principal de animación
function animate() {
    if (isAnimating) {
        const bounds = getPlaygroundBounds();
        
        agents.forEach(agent => {
            if (agent.isExpanded) return; // No mover agentes expandidos
            
            // Ocasionalmente hacemos pequeños ajustes a la dirección
            if (Math.random() < changeDirectionChance) {
                // Pequeño cambio aleatorio en la dirección
                agent.angle += random(-maxTurnAngle, maxTurnAngle);
                agent.vx = Math.cos(agent.angle) * moveSpeed;
                agent.vy = Math.sin(agent.angle) * moveSpeed;
            }
            
            // Movemos el agente
            agent.x += agent.vx;
            agent.y += agent.vy;
            
            // Espacio continuo dentro del playground: si sale por un lado, aparece por el otro
            if (agent.x > bounds.width) {
                agent.x = -160; // aparece por la izquierda
            } else if (agent.x < -160) {
                agent.x = bounds.width; // aparece por la derecha
            }
            
            if (agent.y > bounds.height) {
                agent.y = -160; // aparece por arriba
            } else if (agent.y < -160) {
                agent.y = bounds.height; // aparece por abajo
            }
            
            // Calculamos el ángulo de rotación basado en la dirección
            const visualAngle = Math.atan2(agent.vy, agent.vx) * (180 / Math.PI);
            
            // Aplicamos la posición y rotación
            agent.style.left = agent.x + 'px';
            agent.style.top = agent.y + 'px';
            agent.style.transform = `rotate(${visualAngle}deg)`;
        });
    }
    
    // Continuamos la animación
    requestAnimationFrame(animate);
}

// Iniciamos la animación cuando se carga la página
animate();
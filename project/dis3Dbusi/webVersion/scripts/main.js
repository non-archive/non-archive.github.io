import { createNodeObject3D } from "./nodeObject3D.js";

// Creamos un cache para almacenar los metadatos
const metadataCache = {};

// Función para cargar los metadatos de un nodo
async function obtenerArchivos(nodeId) {
    try {
        const response = await fetch(`data/${nodeId}/metadata.json`);
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const metadata = await response.json();
        return metadata;
    } catch (error) {
        console.error(`Error al obtener metadatos:`, error);
        return {}; // Devuelve un objeto vacío en caso de error
    }
}

// Función para precargar todos los metadatos
async function precargarMetadatos(nodes) {
    // Crear un array de promesas para cargar todos los metadatos en paralelo
    const promesas = nodes.map(async (node) => {
        try {
            metadataCache[node.id] = await obtenerArchivos(node.id);
        } catch (error) {
            console.error(`Error al precargar metadatos para ${node.id}:`, error);
            metadataCache[node.id] = {};
        }
    });

    // Esperar a que todas las cargas terminen
    await Promise.all(promesas);
}

// Inicializar el grafo solo después de cargar los datos
async function inicializarGrafo() {
    try {
        // 1. Cargar estructura.json
        const response = await fetch("estructura.json");
        const data = await response.json();

        // 2. Precargar todos los metadatos
        await precargarMetadatos(data.nodes);

        // 3. Inicializar el grafo una vez que tenemos todos los metadatos
        const Graph = new ForceGraph3D(document.getElementById("3d-graph"), { controlType: "orbit" })
            .graphData(data) // Usamos directamente los datos cargados en lugar de jsonUrl
            .nodeLabel("id")
            .nodeThreeObject((node) => {
                // Ahora usamos la función importada para crear el objeto 3D
                // Obtenemos los metadatos precargados
                const metadata = metadataCache[node.id] || {};
                return createNodeObject3D(metadata);
            });
    } catch (error) {
        console.error("Error al inicializar el grafo:", error);
    }
}

// Iniciar todo el proceso
inicializarGrafo();
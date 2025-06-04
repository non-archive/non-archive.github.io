import * as THREE from "https://esm.sh/three";

export function createImagePlane(imagePath) {
    // Definir el tamaño predeterminado (se ajustará después)
    const defaultSize = 3;
    
    // Crear la geometría del plano con un tamaño predeterminado
    const geometry = new THREE.PlaneGeometry(defaultSize, defaultSize);
    
    // Crear material inicialmente sin textura
    const material = new THREE.MeshBasicMaterial({
        color: 0xcccccc,
        side: THREE.DoubleSide, // Hacer visible por ambos lados
    });
    
    // Crear la malla
    const mesh = new THREE.Mesh(geometry, material);

    const maxSize = 10;
    
    // Cargar la imagen como textura
    const textureLoader = new THREE.TextureLoader();
    textureLoader.load(imagePath, function(texture) {
        // Obtener las proporciones de la imagen
        const imageWidth = texture.image.width;
        const imageHeight = texture.image.height;
        const aspectRatio = imageWidth / imageHeight;
        
        // Calcular dimensiones manteniendo la proporción y respetando el tamaño máximo
        let width, height;
        if (aspectRatio >= 1) {
            // Imagen más ancha que alta
            width = maxSize;
            height = maxSize / aspectRatio;
        } else {
            // Imagen más alta que ancha
            width = maxSize * aspectRatio;
            height = maxSize;
        }
        
        // Actualizar la geometría con las dimensiones correctas
        mesh.geometry.dispose(); // Liberar la geometría anterior
        mesh.geometry = new THREE.PlaneGeometry(width, height);
        
        // Actualizar el material con la textura
        mesh.material.map = texture;
        mesh.material.needsUpdate = true;
    });
    
    return mesh;
}
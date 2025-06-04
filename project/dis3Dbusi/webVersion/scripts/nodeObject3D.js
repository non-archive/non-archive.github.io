import * as THREE from "https://esm.sh/three";
import { createImagePlane } from "./imageLoader.js";

export function createNodeObject3D(metadata) {
    
    // Crear un grupo para contener todos los objetos
    const group = new THREE.Group();
    
    // Crear el plano base
    const sizePlane = 30;
    const plane = new THREE.Mesh(
        new THREE.PlaneGeometry(sizePlane, sizePlane).rotateX(-90 * (Math.PI / 180)),
        new THREE.MeshLambertMaterial({
            color: Math.round(Math.random() * Math.pow(2, 24)),
            transparent: true,
            opacity: 0.75,
            wireframe: true,
        })
    );
    
    // Añadir el plano al grupo
    group.add(plane);
    
    // Si hay archivos, ajustar el tamaño basado en la cantidad
    if (metadata.files && metadata.files.length) {
        const escala = Math.max(0.5, Math.min(4, metadata.files.length / 4));
        plane.scale.set(escala, escala, escala);
        
        let distancia = 0;
        
        metadata.files.map((file) => {
            let mesh;
            
            if (file.type == "image") {
                const pathToImage = "/project/dis3Dbusi/webVersion/" + metadata.path + "/" + file.name;
                // Usar la función importada
                mesh = createImagePlane(pathToImage);
            } else {
                mesh = new THREE.Mesh(
                    new THREE.SphereGeometry(1, 10, 5),
                    new THREE.MeshLambertMaterial({
                        color: Math.round(Math.random() * Math.pow(2, 24)),
                        transparent: true,
                        opacity: 0.9,
                        wireframe: true,
                    })
                );
            }
            
            if (file.data && file.data.rot) {
                mesh.rotateY(file.data.rot[0] * (Math.PI / 180));
                mesh.rotateX(file.data.rot[1] * (Math.PI / 180));
                mesh.rotateZ(file.data.rot[2] * (Math.PI / 180));
            } else {
                // Aplicar rotación por defecto
                mesh.rotateY(45 * (Math.PI / 180));
            }
            
            if (file.data && file.data.pos) {
                mesh.position.y = file.data.pos[0];
                mesh.position.x = file.data.pos[1];
                mesh.position.z = file.data.pos[2];
            } else {
                // Posicionamiento por defecto
                mesh.position.y = 5;
                mesh.position.x = -(escala * sizePlane) / 2 + distancia;
                mesh.position.z = -(escala * sizePlane) / 2;
                distancia += 4;
            }
            
            if (file.data && file.data.scale) {
                mesh.scale.set(file.data.scale, file.data.scale, file.data.scale);
            }
            
            group.add(mesh);
        });
    }
    
    return group;
}
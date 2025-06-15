import os
from pathlib import Path
from typing import List
from generateTags import *

# Returns the HTML header with embedded CSS styles.
def get_html_header() -> str:
    return """
    <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📁</title>
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            <style>
            /* CSS personalizado solo para las animaciones */
            .animate-marquee {
                animation: marquee 40s linear infinite;
            }

            .animate-marquee2 {
                animation: marquee2 40s linear infinite;
            }

            @keyframes marquee {
                0% {
                    transform: translateX(0%);
                }
                100% {
                    transform: translateX(-100%);
                }
            }

            @keyframes marquee2 {
                0% {
                    transform: translateX(100%);
                }
                100% {
                    transform: translateX(0%);
                }
            }
        </style>
        </head>
        <body class="">
        <main>

        <h1 class="fixed top-2 right-2 text-4xl sm:text-6xl pointer-events-none z-10">NON-ARCHIVES</h1>
    """

# Returns the HTML footer section.
def get_html_footer() -> str:
    return """
        <div class="fixed bottom-10 right-4"><p>inspired by Distribusi</p></div>
        </main>

        <div class="fixed bottom-1 overflow-hidden flex items-center">
            <div class="relative flex whitespace-nowrap">
                <div class="flex animate-marquee">
                    <span class="text-lg px-8 font-medium">
                        A project created within the framework of the Organismo | Art in Applied Critical Ecologies independent study program, promoted by
                        TBA21–Academy and the Museo Nacional Thyssen-Bornemisza as part of the case study Non-Archives facilitated by TBA21–Academy –––––
                    </span>
                </div>
                <div class="flex animate-marquee2 absolute top-0">
                    <span class="text-lg px-8 font-medium">
                        A project created within the framework of the Organismo | Art in Applied Critical Ecologies independent study program, promoted by
                        TBA21–Academy and the Museo Nacional Thyssen-Bornemisza as part of the case study Non-Archives facilitated by TBA21–Academy –––––
                    </span>
                </div>
            </div>
        </div>

               <div id="playground" class="absolute inset-0 z-30 pointer-events-none overflow-hidden">
            <div class="agent absolute h-40 aspect-square cursor-pointer z-30" style="top: 0; left: 0">
                <model-viewer
                    class="mb-2 w-full h-full pointer-events-none"
                    src="/project/characters/controler.glb"
                    tone-mapping="neutral"
                    shadow-intensity="2"
                    shadow-softness="0"
                    exposure="1.15"
                    camera-orbit="99.92deg 0deg 3.792m"
                    field-of-view="30deg"
                    auto-rotate
                >
                </model-viewer>
                <div class="absolute top-4 left-4 text-xl  pointer-events-auto">
                    <h3 class="text-3xl mb-2 hidden agent-text">Linear Character</h3>
                    <p class="mb-6 hidden agent-text">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Culpa sit recusandae voluptas velit placeat maxime reprehenderit aliquam odio
                        adipisci, ut laudantium autem obcaecati explicabo iusto rerum illum error possimus aperiam!
                    </p>
                    <a href="/linear" class="bg-white p-2 border hover:bg-blue-200 hidden agent-text">Access</a>
                </div>
            </div>

            <div class="agent absolute h-40 aspect-square cursor-pointer z-30" style="top: 0; left: 0">
                <model-viewer
                    class="mb-2 w-full h-full pointer-events-none"
                    src="/project/characters/hashtag.glb"
                    tone-mapping="neutral"
                    shadow-intensity="2"
                    shadow-softness="0"
                    exposure="1.15"
                    camera-orbit="99.92deg 0deg 3.792m"
                    field-of-view="30deg"
                    auto-rotate
                >
                </model-viewer>
                <div class="absolute top-4 left-4 text-xl  pointer-events-auto">
                    <h3 class="text-3xl mb-2 hidden agent-text">Files Character</h3>
                    <p class="mb-6 hidden agent-text">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Culpa sit recusandae voluptas velit placeat maxime reprehenderit aliquam odio
                        adipisci, ut laudantium autem obcaecati explicabo iusto rerum illum error possimus aperiam!
                    </p>
                    <a href="/files" class="bg-white p-2 border hover:bg-blue-200 hidden agent-text">Access</a>
                </div>
            </div>

            <div class="agent absolute h-40 aspect-square cursor-pointer z-30" style="top: 0; left: 0">
                <model-viewer
                    class="mb-2 w-full h-full pointer-events-none"
                    src="/project/characters/controler.glb"
                    tone-mapping="neutral"
                    shadow-intensity="2"
                    shadow-softness="0"
                    exposure="1.15"
                    camera-orbit="99.92deg 0deg 3.792m"
                    field-of-view="30deg"
                    auto-rotate
                >
                </model-viewer>
                <div class="absolute top-4 left-4 text-xl  pointer-events-auto">
                    <h3 class="text-3xl mb-2 hidden agent-text">Infrastructure Character</h3>
                    <p class="mb-6 hidden agent-text">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Culpa sit recusandae voluptas velit placeat maxime reprehenderit aliquam odio
                        adipisci, ut laudantium autem obcaecati explicabo iusto rerum illum error possimus aperiam!
                    </p>
                    <a href="/infrastructure" class="bg-white p-2 border hover:bg-blue-200 hidden agent-text">Access</a>
                </div>
            </div>

            <div class="agent absolute h-40 aspect-square cursor-pointer z-30" style="top: 0; left: 0">
                <model-viewer
                    class="mb-2 w-full h-full pointer-events-none"
                    src="/project/characters/hashtag.glb"
                    tone-mapping="neutral"
                    shadow-intensity="2"
                    shadow-softness="0"
                    exposure="1.15"
                    camera-orbit="99.92deg 0deg 3.792m"
                    field-of-view="30deg"
                    auto-rotate
                >
                </model-viewer>
                <div class="absolute top-4 left-4 text-xl  pointer-events-auto">
                    <h3 class="text-3xl mb-2 hidden agent-text">Spatial</h3>
                    <p class="mb-6 hidden agent-text">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Culpa sit recusandae voluptas velit placeat maxime reprehenderit aliquam odio
                        adipisci, ut laudantium autem obcaecati explicabo iusto rerum illum error possimus aperiam!
                    </p>
                    <a href="#" class="bg-white p-2 border hover:bg-blue-200 hidden agent-text">Access</a>
                </div>
            </div>
        </div>

        <!-- Overlay para cerrar al hacer clic fuera -->
        <div id="overlay" class="fixed inset-0 backdrop-blur-lg bg-opacity-50 z-20 hidden"></div>

        <!-- Cargamos el script externo -->
        <script src="/linear/index_files/moving.js"></script>
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>
        </body>
    </html>
    """

# Normalizes a path for URL usage by replacing special directories.
def normalize_path_for_url(path: str) -> str:
    return path.replace("../../", "/").replace(".github", "_github").replace(".git", "_git")

# Normalizes a path for display purposes.
def normalize_path_for_display(path: str) -> str:
    return path.replace("../../", "/").replace("_github", ".github").replace("_git", ".git")

# Checks if a folder should be excluded from the index.
def should_exclude_folder(folder_name: str) -> bool:
    excluded_folders = {"files", ".git", "__pycache__"}
    return folder_name in excluded_folders

# Generates HTML links for folders.
def generate_folder_links(path_real: str, folders: List[str]) -> str:

    folder_links = []
    
    for folder in folders:
        if not should_exclude_folder(folder):
            folder_url = normalize_path_for_url(folder)
            folder_link = f"""
            <a class="w-full group text-blue-600" href="{path_real}/{folder_url}">
                <p class="text-7xl sm:text-9xl text-center mb-10 -translate-x-2 sm:-translate-x-0">📁</p>
                <p class="text-xs sm:text-base text-center group-hover:underline">/{folder}</p>
            </a>
            """

            folder_links.append(folder_link)
    
    return '\n'.join(folder_links)

# Generates the main HTML body content.
def generate_html_body(path: Path, path_real: str, path_view: str, files: List[str], folders: List[str]) -> str:
    # Generate back button
    parent_path = str(Path(path_real).parent)
    disable = ""
    if parent_path == "/":
        disable = 'pointer-events-none bg-slate-200 text-slate-400'
    back_button = f'<a href="{parent_path}" class="{disable} hover:bg-emerald-300 border p-2 border-emerald-500"><p>&#8604;back</p></a>'
    
    # Generate folder links
    folder_links = generate_folder_links(path_real, folders)
    files_tags = generateTags(files, path_view.replace("/files/", "/"))
    
    # Clean path for title display
    title_path = path_view.replace("/files/", "/").replace("/files", "/")
    
    return f"""
    <div class="flex items-center pt-20 sm:pt-10 p-10 px-4 sm:px-10 gap-2 text-xl sm:text-2xl">
                {back_button}
                <h1 class="p-2 border border-emerald-500 flex-1">{title_path}</h1>
            </div>
            <div class="grid grid-cols-3 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 p-10 px-4 sm:px-10 gap-10">
                {folder_links}
                {files_tags}
            </div>
        """

# Generates an HTML index file for the given directory.
def generateIndex(path: Path, files: List[str], folders: List[str]) -> None:
    
    # Convert paths for different purposes
    path_real = normalize_path_for_url(str(path))
    path_view = normalize_path_for_display(str(path))
    
    # Generate HTML components
    html_header = get_html_header()
    html_body = generate_html_body(path, path_real, path_view, files, folders)
    html_footer = get_html_footer()
    
    # Combine all HTML content
    html_content = html_header + html_body + html_footer
    
    # Write to index.html file
    index_path = path / "index.html"
    with open(index_path, "w", encoding="utf-8") as file:
        file.write(html_content)
import html
import json
import os

img_ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.avif')

def generateImage(file, path):
    adjusted_path = path.replace("/files", "")
    return f"""
    <div class="col-span-2 sm:col-auto">
        <img class="shadow-lg border border-slate-300 mb-6" src="{adjusted_path + "/" + file}" />
        <div class="text-center">
        <a href="{adjusted_path + "/" + file}" class=" break-all hover:underline text-blue-600 p-4">{file}</a>
        </div>
    </div>
    """

txt_ext = ('.txt', '.md')

def generateText(file, path):
    adjusted_path = path.replace("/files", "")
    with open(f"../..{adjusted_path}/{file}", 'r', encoding='utf-8') as f:
        content = f.read()
        
    content_html = content.replace('\n', '<br>')
    content_html = html.escape(content_html).replace('&lt;br&gt;', '<br>')
        
    return f"""
    <div class="col-span-2 sm:col-auto">
        <div class="shadow-lg border border-slate-300 mb-6 p-4 bg-white max-h-80 overflow-auto">
            {content_html}
        </div>
        <div class="text-center">
        <a href="{path.replace("/files", "")}/{file}" class=" break-all hover:underline text-blue-600 p-4">{file}</a>
        </div>
    </div>
    """

video_ext = ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.3gp')

def generateVideo(file, path):
    return f"""
    <div class="col-span-2 sm:col-auto">
        <video controls class="shadow-lg border border-slate-300 mb-6"  loop>
            <source src="{path}/{file}" type="video/{file.split('.')[-1].lower()}">
            Tu navegador no soporta el elemento video.
        </video>
        <div class="text-center">
        <a href="{path}/{file}" class=" break-all hover:underline text-blue-600 p-4">{file}</a>
        </div>
    </div>
    """

audio_ext = ('.mp3', '.wav', '.ogg', '.aac', '.flac', '.m4a', '.wma', '.opus')

def generateAudio(file, path):
    return f"""
    <div class="col-span-2 sm:col-auto">
        <audio controls class="w-full mb-6" loop>
            <source src="{path}/{file}" type="audio/{file.split('.')[-1].lower()}">
            Tu navegador no soporta el elemento audio.
            <a href="{path}/{file}">Descargar audio</a>
        </audio>
        <div class="text-center">
        <a href="{path}/{file}" class=" break-all hover:underline text-blue-600 p-4">{file}</a>
        </div>
    </div>
    """

pdf_ext = ('.pdf',)

def generatePDF(file, path):
    return f"""
    <div class="col-span-2 sm:col-auto">
        <iframe src="{path}/{file}" 
                class=" w-full h-80 mb-6 shadow-lg border border-slate-300">
            <p>Tu navegador no puede mostrar PDFs. 
            <a href="{path}/{file}">Descargar PDF</a>
            </p>
        </iframe>
        <div class="text-center">
        <a class="hover:underline text-blue-600 p-4 break-all" href="{path}/{file}">{file}</a>
        </div>
    </div>
    """

html_ext = ('.html', '.htm')

def generateHTML(file, path):
    return f"""
    <div class="col-span-2 sm:col-auto">
        <a href="{path.replace("/files", "")}/{file}"><iframe src="{path.replace("/files", "..")}/{file}" 
                class=" w-full h-80 mb-6 shadow-lg border border-slate-300"
                sandbox="allow-same-origin">
            <p>Tu navegador no puede mostrar este archivo HTML. 
            <a href="{path}/{file}">Abrir en nueva pestaña</a>
            </p>
        </iframe></a>
        <div class="text-center">
        <a class="hover:underline text-blue-600 p-4 break-all" href="{path.replace("/files", "")}/{file}">{file}</a>
        </div>
    </div>
    """

link_ext = ('.link')

def generateLINK(file, path):
    adjusted_path = path.replace("/files", "")
    try:
        with open(f"../..{adjusted_path}/{file}", 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(f"../..{adjusted_path}/{file}", 'r', encoding='latin-1') as f:
            content = f.read()
    return f"""
    <div class="col-span-2 sm:col-auto">
        <a href="{content}"><iframe src="{content}" 
                class=" w-full h-80 mb-6 shadow-lg border border-slate-300"
                sandbox="allow-same-origin">
            <p>Tu navegador no puede mostrar este archivo HTML. 
            <a href="{content}">Abrir en nueva pestaña</a>
            </p>
        </iframe></a>
        <div class="text-center">
        <a class="hover:underline text-blue-600 p-4 break-all" href="{content}">{content}</a>
        </div>
    </div>
    """

glb_ext = ('.glb')

def generateGLB(file, path):
    adjusted_path = path.replace("/files", "")
    return f"""
    <div class="col-span-2 sm:col-auto">
        <model-viewer class=" w-full h-80 mb-6 shadow-lg border border-slate-300" src="{adjusted_path}/{file}" camera-controls tone-mapping="neutral" shadow-intensity="2" shadow-softness="0" exposure="1.15" auto-rotate camera-orbit="99.92deg 42.31deg 3.792m" field-of-view="30deg">
        </model-viewer> 

        <div class="text-center">
        <a class="hover:underline text-blue-600 p-4 break-all" href="{adjusted_path + "/" + file}">{file}</a>
        </div>
    </div>
    """

code_ext = ('.py', '.js', '.gd', '.godot', '.uid', '.tscn', '.yml', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', 
           '.rs', '.swift', '.kt', '.ts', '.jsx', '.tsx', '.vue', '.scss', '.sass', 
           '.less', '.sql', '.sh', '.bat', '.ps1', '.r', '.m', '.scala', '.pl')

def generateCode(file, path):
    # Leer el contenido del archivo
    adjusted_path = path.replace("/files", "")
    with open(f"../..{adjusted_path}/{file}", 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Escapar caracteres HTML especiales
    content_html = html.escape(content)
        
    return f"""
    <div class="col-span-2 sm:col-auto">
        <pre class="shadow-lg border border-slate-300 mb-6 p-4 bg-slate-700 text-emerald-300 max-h-80 overflow-auto">
        <code>{content_html}</code>
        </pre>

        <div class="text-center">
        <a class=class="hover:underline text-blue-600 p-4 break-all" href="{path}/{file}">{file}</a>
        </div>
    </div>
    """

json_ext = ('.json',)

def generateJSON(file, path, max_size_kb=500):        
    return f"""
    <div class="col-span-2 sm:col-auto">
        <iframe src="{path + "/" + file}" 
                class=" w-full h-80 mb-6 shadow-lg border border-slate-300"
                sandbox="allow-same-origin">
            <p>Tu navegador no puede mostrar este archivo HTML. 
            <a href="{path + "/" + file}">Abrir en nueva pestaña</a>
            </p>
        </iframe>

        <div class="text-center">
        <a class=class="hover:underline text-blue-600 p-4 break-all" href="{path}/{file}">{file}</a>
        </div>
    </div>
    """

def generateTags(files, path):
    filesTag = []
    for file in files:
        if file.lower().endswith(img_ext):
            fileTag = generateImage(file, path)
        elif file.lower().endswith(txt_ext):
            fileTag = generateText(file, path)
        elif file.lower().endswith(video_ext):
            fileTag = generateVideo(file, path)
        elif file.lower().endswith(audio_ext):
            fileTag = generateAudio(file, path)
        elif file.lower().endswith(pdf_ext):
            fileTag = generatePDF(file, path)
        elif file.lower().endswith(html_ext):
            fileTag = generateHTML(file, path)
        elif file.lower().endswith(link_ext):
            fileTag = generateLINK(file, path)
        elif file.lower().endswith(glb_ext):
            fileTag = generateGLB(file, path)
        elif file.lower().endswith(code_ext):
            fileTag = generateCode(file, path)
        elif file.lower().endswith(json_ext):
            fileTag = generateJSON(file, path)
        else:
            fileTag = f"""
                <div>
                    <a class="file-name" href="{path + "/" + file}">{file}</a>
                    <p>unknown format :/</p>
                </div>
                """
        filesTag.append(fileTag)
    return '\n'.join(filesTag)

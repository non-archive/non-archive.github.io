import html

img_ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg')

def generateImage(file, path):
    return f"""
    <div class="image-div">
        <a class="file-name" href="{path + "/" + file}">{file}</a>
        <img src="{path + "/" + file}" />
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
    <div>
        <a class="file-name" href="{path.replace("/files", "")}/{file}">{file}</a>
        <div class="text-content">
            {content_html}
        </div>
    </div>
    """

video_ext = ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.3gp')

def generateVideo(file, path):
    return f"""
    <div>
        <a class="file-name" href="{path}/{file}">{file}</a>
        <video controls width="100%" style="max-width: 600px;" loop>
            <source src="{path}/{file}" type="video/{file.split('.')[-1].lower()}">
            Tu navegador no soporta el elemento video.
        </video>
    </div>
    """

audio_ext = ('.mp3', '.wav', '.ogg', '.aac', '.flac', '.m4a', '.wma', '.opus')

def generateAudio(file, path):
    return f"""
    <div>
        <a class="file-name" href="{path}/{file}">{file}</a>
        <audio controls style="width: 100%; max-width: 600px;" loop>
            <source src="{path}/{file}" type="audio/{file.split('.')[-1].lower()}">
            Tu navegador no soporta el elemento audio.
            <a href="{path}/{file}">Descargar audio</a>
        </audio>
    </div>
    """

pdf_ext = ('.pdf',)

def generatePDF(file, path):
    return f"""
    <div class="iframe-div">
        <a class="file-name" href="{path}/{file}">{file}</a>
        <iframe src="{path}/{file}" 
                width="100%" 
                height="600px" 
                style="max-width: 600px;">
            <p>Tu navegador no puede mostrar PDFs. 
            <a href="{path}/{file}">Descargar PDF</a>
            </p>
        </iframe>
    </div>
    """

html_ext = ('.html', '.htm')

def generateHTML(file, path):
    return f"""
    <div class="iframe-div">
        <a class="file-name" href="{path.replace("/files", "")}/{file}">{file}</a>
        <iframe src="{path.replace("/files", "..")}/{file}" 
                style="border: 1px solid #ccc"
                sandbox="allow-same-origin">
            <p>Tu navegador no puede mostrar este archivo HTML. 
            <a href="{path}/{file}">Abrir en nueva pestaña</a>
            </p>
        </iframe>
    </div>
    """

glb_ext = ('.glb')

def generateGLB(file, path):
    return f"""
    <div class="model-div">
        <a class="file-name" href="{path + "/" + file}">{file}</a>
        <model-viewer src="{path}/{file}" camera-controls tone-mapping="neutral" shadow-intensity="2" shadow-softness="0" exposure="1.15" auto-rotate camera-orbit="99.92deg 42.31deg 3.792m" field-of-view="30deg">
        </model-viewer> 
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
        elif file.lower().endswith(glb_ext):
            fileTag = generateGLB(file, path)
        else:
            fileTag = f"""
                <div>
                    <a class="file-name" href="{path + "/" + file}">{file}</a>
                    <p>unknown format :/</p>
                </div>
                """
        filesTag.append(fileTag)
    return '\n'.join(filesTag)

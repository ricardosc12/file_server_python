let TIMER = 25

function request(data){
    return new Promise (resolve=>{
        fetch(`http://${HOST}/get`,{
            method:'POST',
            body:JSON.stringify(data),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        }).then(resp=>resp.json())
        .then(resp=>resolve(resp))
    })
}

function getFile(data){
    return new Promise (resolve=>{
        fetch(`http://${HOST}/getFile`,{
            method:'POST',
            body:JSON.stringify(data),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        }).then(resp=>resp.json())
        .then(resp=>resolve(resp))
    })
}

function inputValue(path){
    return /*html*/`
        <input id='path_input' type="text" value="${path}">
    `
    
}

function goPath(path,back){
    files = path.split('.')
    toltipEnd()
    if(files.length>1 && !back) {
        let extension = files.pop()
        
        getFile({'path':PATH+'/'+path}).then(resolve=>{
            let blob = b64toBlob(resolve.dados.content,'application/octet-stream')
            downloadFile(blob,files.join(''),extension)
        })
    }
    else {
        request({'path':back?path:PATH+'/'+path}).then(resolve=>{
            if(resolve.status){
                PATH = back?path:PATH+'/'+path
                document.getElementsByClassName('search')[0].innerHTML = inputValue(PATH)
                document.getElementsByClassName('list')[0].innerHTML = createFile(resolve.dados)
            }
        })
    }
}

function backPath(){
    let paths = PATH.split('/')
    if(paths.length==2) return
    paths.pop()
    goPath(paths.join('/'),true)
    toltipEnd()
}

function createFile(data){
    string = ''
    data.map(dt=>{
        let file = dt.split('.').length>1
        string = string+
        /*html*/`
            <div onmouseleave="toltipEnd(event)" onmouseenter="toltipIni(event);" class="file" onclick="goPath('${dt}')">
                ${!file?iconFolder():iconFile()}
                ${file?`<p>${dt.split('.').pop().toUpperCase()}</p>`:''}
                <span>${dt}</span>
            </div>
        `
    })
    return string
}


const b64toBlob = (b64Data, contentType='', sliceSize=512) => {
    try{
      const byteCharacters = window.atob(b64Data);
      const byteArrays = [];
    
      for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize);
    
        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }
    
        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }
    
      const blob = new Blob(byteArrays, {type: contentType});
      return blob;
    }
    catch{
      return false
    }
  }

function downloadFile(blob,name,type){

    const url = window.URL.createObjectURL(blob); //xml → pdf
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${name}.${type}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(link.href), 7000);
}

function handlerDragOver(e) {
    e.preventDefault();
    return false
}

function handlerDragStart() {
    TIMER = 80
    startMatrix()
}
function handlerDragEnd(){
    TIMER = 25
    startMatrix()
    console.log("SAIU")
}

function handlerDrop(ev) { 
    ev.preventDefault();
    TIMER = 25
    startMatrix()
    var data = new FormData();
    if (ev.dataTransfer.items) {
      for (var i = 0; i < ev.dataTransfer.items.length; i++) {
        if (ev.dataTransfer.items[i].kind === 'file') {
          var file = ev.dataTransfer.items[i].getAsFile();
          data.append("file[]",file)
        }
      }
    }
    data.append("path",PATH)
    sendFile(data).then(resolve=>{
        if(resolve.status){
            goPath(PATH,true)
        }
    })
    return false
}

function sendFile(data){
    return new Promise (resolve=>{
        fetch(`http://${HOST}/sendFile`,{
            method:'POST',
            body:data
        }).then(resp=>resp.json())
        .then(resp=>resolve(resp))
    })
}

function toltip(name,top,left){
    return nodeHtml(/*html*/`
        <div class='toltip' style="top:${top}px;left:${left}px" >${name}</div>
    `)
}

let timer_toltip = null

function toltipEnd(e){
    let toltip_ = document.getElementsByClassName('toltip')
    if(toltip_.length) toltip_[0].remove()
    clearTimeout(timer_toltip)
}
function toltipIni(e){
    let toltip_ = document.getElementsByClassName('toltip')
    if(toltip_.length) toltip_[0].remove()
    timer_toltip = setTimeout(()=>{
        let name = e.target.getElementsByTagName('span')[0].innerHTML
        var {top,right,bottom,left} = e.target.getBoundingClientRect();
        toltip_ = toltip(name,top,left)
        document.getElementsByClassName('root')[0].appendChild(toltip_)
    },500)
}

function nodeHtml(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    return div.firstChild;
  }
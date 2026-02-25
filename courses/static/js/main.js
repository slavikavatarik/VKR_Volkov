const data = JSON.parse(document.getElementById('file_path-id').textContent);
//console.log("data: " + data); 
const url = '../../../media/docs/' + data.substring(1, data.length-1);     //sample-local-pdf.pdf';
//console.log(url); 
let pdfDoc = null,
pageNum = 1,
pageIsRendering = false,
pageNumIsPending = null;

const scale = 1.5,
canvas = document.querySelector('#pdf-render'),
ctx = canvas.getContext('2d');

const renderPage = num => {
pageIsRendering = true;
pdfDoc.getPage(num).then(page => {
    //console.log(page);
    const viewport = page.getViewport({scale});
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    const renderCtx = {
        canvasContext: ctx,
        viewport
    }

    page.render(renderCtx).promise.then(()=>{
        pageIsRendering = false;

        if(pageNumIsPending != null) {
            renderPage(pageNumIsPending);
            pageNumIsPending = null;
        }
    });
    document.querySelector('#page-num').textContent = num;
});
};

const queueRenderPage = num => {
    if(pageIsRendering) {
        pageNumIsPending = num;
    } else {
        renderPage(num);
    }
}

const showPrevPage = () => {
    if(pageNum <= 1) {
        return;
    }
    pageNum--;
    queueRenderPage(pageNum);
}

const showNextPage = () => {
    if(pageNum >= pdfDoc.numPages) {
        return;
    }
    pageNum++;
    queueRenderPage(pageNum);
}

pdfjsLib.getDocument(url).promise.then(pdfDoc_ => {
    pdfDoc=pdfDoc_;
    //console.log(pdfDoc);
    document.querySelector('#page-count').textContent = pdfDoc.numPages;
    renderPage(pageNum) ;  // у Бреда нет ;
})
.catch(err => {
    const div = document.createElement('div');
    div.className = 'error';
    div.appendChild(document.createTextNode(err.message));
    document.querySelector('body').insertBefore(div, canvas);
    document.querySelector('.top-bar').computedStyleMap.display = 'none';
});

document.querySelector('#prev-page').addEventListener('click', showPrevPage);
document.querySelector('#next-page').addEventListener('click', showNextPage);
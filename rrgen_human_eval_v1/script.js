// document.addEventListener('prodigyanswer', getSemanticContent);

document.addEventListener('prodigyanswer', event => {
    event.detail.task.anno.sem_rel = getSemanticRel();
    console.log('updated annotation: SEM REL=', event.detail.task.anno.sem_rel)
    // window.prodigy.update({ 'anno.semantic_content': sc
    // });
    event.detail.task.anno.fluency = getFluencyScore();
    console.log('updated annotation: FLUENCY=', event.detail.task.anno.fluency)
    event.detail.task.anno.approp = getAppropriateScore();
    console.log('updated annotation: APPROP=', event.detail.task.anno.approp)
    event.detail.task.anno.acc = getAccuracyScore();
    console.log('updated annotation: ACC=', event.detail.task.anno.acc)
})

function getSemanticRel() {
    const score = document.querySelector('input[name="sem_rel"]:checked').value;
    return parseInt(score)
}

function getFluencyScore() {
    const score = document.querySelector('input[name="fluency"]:checked').value;
    return parseInt(score)
}

function getAppropriateScore() {
    const score = document.querySelector('input[name="approp"]:checked').value;
    return parseInt(score)
}

function getAccuracyScore() {
    const score = document.querySelector('input[name="acc"]:checked').value;
    return parseInt(score)
}

// function insertLineBreaks(s) {
//     s.replace(/<GREETING>/g, '<GREETING>\n');
//     s.replace(/<SALUTATION>/g, '\n<SALUTATION>');
//     s.replace(/---SEP---/g, '\n');
//     return s
// }

    // if (answer == 'accept') {
    //     // console.log('accept')
    //     console.log(task.anno)
    //     task.anno = getSemanticContent()
    //     console.log(task.anno)
    //     // do something with the task here
    // }

document.addEventListener('DOMContentLoaded', () => getRandomWord());

async function getRandomWord() {
    const url = 'https://nms-words.kgabriel.dev/random-word.php';

    const response = await fetch(url, { method: 'GET', mode: 'no-cors'});
    
    if(response.status !== 200) {
        console.error('Error fetching random word');
        return;
    }

    const data = await response.json();
    
    if(!data) {
        console.error('Error parsing JSON');
        return;
    }

    console.log(data);
    setDataInDom(data);
}

function setDataInDom(data) {
    const language = data.language;
    
    const translation = data.word.split(':')[0];
    const wordData = data.word.split(':')[1].split(';');

    console.log(wordData);

    setStringForDomElementWithId('word', translation);
    setStringForDomElementWithId('translation', wordData[0] || 'Unknown');
    setStringForDomElementWithId('translation_caps', wordData[1] || 'Unknown');
    setStringForDomElementWithId('translation_all-caps', wordData[2] || 'Unknown');
    setStringForDomElementWithId('language', language);
}

function setStringForDomElementWithId(id, string) {
    const element = document.getElementById(id);
    element.innerText = string;
}
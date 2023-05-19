document.addEventListener('DOMContentLoaded', () => {
    getRandomWord();
    setLanguageSelection();
});

async function getRandomWord() {
    const urlSearchParams = new URLSearchParams(window.location.search),
        currentLanguage = urlSearchParams.get('language');

    const languageScriptUrl = 'https://nms-words.kgabriel.dev/random-word.php';

    const url = currentLanguage ? `${languageScriptUrl}?language=${currentLanguage.toString()}` : languageScriptUrl;

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

    setDataInDom(data);
}

function setDataInDom(data) {
    const language = data.language;
    
    const translation = data.word.split(':')[0];
    const wordData = data.word.split(':')[1].split(';');

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

function setNmsLanguage() {
    const selection = document.getElementById('language-selection').value;
    const language = selection === 'random' ? '' : selection.charAt(0).toUpperCase() + selection.slice(1);

    const url = selection !== 'random' ? 'https://nms-words.kgabriel.dev?language=' + language : 'https://nms-words.kgabriel.dev';
    
    window.location.href = url;
}

function setLanguageSelection() {
    const urlSearchParams = new URLSearchParams(window.location.search),
        urlLanguage = urlSearchParams.get('language');
    const selection = document.getElementById('language-selection');

    if(!urlLanguage) {
        selection.value = 'random';
        return;
    };

    const value = urlLanguage.toLowerCase();
    selection.value = ["gek", "korvax", "vy'keen", "atlas"].includes(value) ? value : ['random'];
}
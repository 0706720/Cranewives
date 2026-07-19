let globalIndex = -1;
let currentArray = 'original';

let originalOrder = [];
let originalDict;
let randomOrder = [];
let singlesDict;

async function startUp()
{
    setVideoButtonDisplay();
    await init();
}

function setVideoButtonDisplay()
{
    // if the funtion for originalShuffle exists in this script, then the video option buttons will be relevant.
    // therefore, the 'finally' block will run to change each button to appear usuable.
    // however, if there isnt a function (as in, the catch block runs) then return is used to stop the 'finally' block running
    try {
        originalShuffle();
    } catch(err) {
        return;
    } finally {
        changeButtons();
    }
}

function changeButtons()
{
    // there are only 4 video option buttons assigned the class 'notapplicable'. query selector will create an array-like object.
    const videoButtons = document.querySelectorAll('.notapplicable');
    // for every array element, remove the class which creates the not-allowed cursor type and greys out the background
    for (let i = 0; i < videoButtons.length; i++) {
        let list = videoButtons[i].classList;
        // appreciably, this doesn't ever need to be re-added since the CSS loads fresh from each HTML page.
        list.remove("notapplicable");
    }
}

async function init()
{
    const response = await fetch('../json/albums.json');
    originalDict = await response.json();
    const response2 = await fetch('../json/singles.json');
    singlesDict = await response2.json();
    // this will compare the albums dict to the singles dict, and eliminate duplicates that appear in the singles section to avoid error.
    // this is a necessity due to the garbage singles search by ytmusicapi on the crane wives.
    let groupedAlbums = createAlbums(originalDict, singlesDict);
    //document.getElementById('videodiv').innerHTML += JSON.stringify(groupedAlbums);
    createAlbumPageElements(groupedAlbums);
}

function createAlbums(albums, singles)
{
    // this section will group albums. this first line is const because the albums will never change whilst in javascript, they are only
    // ever modified in python.
    const groupedAlbums = {};

    // https://www.w3schools.com/js/js_object_intro.asp
    // similar to python syntax, where 'song' represents each index of 'albums', which is the json data provided by python scripts. albums
    // will represent a array of individual objects, noted by {}.
    for (const song of albums) {
        // this line reads as: if a property equal to the string of an album name DOESN'T exist inside of the 'groupedAlbums' dict, then
        // this evals true.
        if (!groupedAlbums[song.album]) {
            // if the previous line evaluated true, this will create a new property for 'groupedAlbums' such as ('Foxlore'), etc. This means
            // for as long as new indexes have the exact same album property value, all new songs will be under the same object.
            groupedAlbums[song.album] = [];
        }
        // this line adds an array element to a specific property based on album name read.
        groupedAlbums[song.album].push(song);
    }

    // this object will always be statically named 'Singles', and store singles across all artists.
    groupedAlbums['Singles'] = [];
    for (const song of singles) {
        // exact same methodology as the prior for loop, but less computation due to a fixed object parent.
        groupedAlbums['Singles'].push(song);
    }
    // value is returned back to function init() in order to reduce global variable usage and namespace pollution.
    return groupedAlbums;
}

function createAlbumPageElements(songList)
{
    const pageLocation = document.getElementById('albums');

    let keyExtract = Object.keys(songList);
    for (let property of keyExtract) {
        pageLocation.appendChild(document.createElement('br'));
        let buttonElement = document.createElement('button');
        buttonElement.textContent = property;
        pageLocation.appendChild(buttonElement);
        buttonElement.onclick = function() {
            playAlbum(property, songList);
        };
        pageLocation.appendChild(document.createElement('br'));
        for (let song of songList[property]) {
            let albumElement = document.createElement('span');
            //albumElement.id = songList[]
            albumElement.textContent = song.name + ', ';
            pageLocation.appendChild(albumElement);
        }
    }
}

function playAlbum(albumString, songList)
{
    // clear the main array so that choosing a new album will not include remnants of the previous one.
    originalOrder = [];
    // the map keyword creates a new array from calling a function for every array element. Therefore, for every song index inside of a
    // particular object property of songList, populate originalOrder with only the ids. It works similar to a loop. For example: 
    // songList['Foxlore'].map({"album":"Foxlore","id":"56rtvwq3qvA","name":"Nothing at All"} => "56rtvwq3qvA");
    originalOrder = songList[albumString].map(song => song.id);
    //document.getElementById('videodiv').innerHTML = JSON.stringify(originalOrder);
    originalShuffle();
}

// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() 
{
    player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'CwwFQj_dQso',
    playerVars: {
        'playsinline': 1
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
        });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) 
{
    event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done = false;
function onPlayerStateChange(event) 
{
    if (event.data == YT.PlayerState.ENDED) {
        incrementIndex();
    }
}

function stopVideo() 
{
    // currently rendered redundant by func incrementIndex.
    player.stopVideo();
    incrementIndex();
}

function incrementIndex()
{
    globalIndex++;
    if(currentArray == 'original') {
        player.loadVideoById(videoId = originalOrder[globalIndex], startSeconds = 0);
    } else {
        player.loadVideoById(videoId = randomOrder[globalIndex], startSeconds = 0);
    }
}

function next()
{
    incrementIndex();
}

function previous()
{
    if (globalIndex >= -1) {
        globalIndex -= 2;
    } else {
        globalIndex = -1;
    }
    incrementIndex();
}

function originalShuffle()
{
    globalIndex = -1;
    currentArray = 'original';
    incrementIndex();
}

function randomShuffle()
{
    globalIndex = -1;
    currentArray = 'random';
    shuffle();
    incrementIndex();
}
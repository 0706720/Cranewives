let globalIndex = -1;
let currentArray = 'original';

let originalOrder = [];
let randomOrder = [];

async function startUp()
{
    await init();
    shuffle(); 
}

async function init()
{
    const response = await fetch('./videos.json');
    originalOrder = await response.json();
}

function shuffle()
{
    randomOrder = [...originalOrder];
    //   set the index to the arrays length
    let i = randomOrder.length, j, temp;
    //   create a loop that subtracts everytime it iterates through
    while (--i > 0) {
    //  create a random number and store it in a variable
    j = Math.floor(Math.random () * (i+1));
    // create a temporary position from the item of the random number    
    temp = randomOrder[j];
    // swap the temp with the position of the last item in the array    
    randomOrder[j] = randomOrder[i];
    // swap the last item with the position of the random number 
    randomOrder[i] = temp;
    } 
    
}

function display()
{
    // currently useless due to full url not being necessary, just the video ID.
    for (let i = 0; i < importedVideos.length; i++) {
        let url = "https://www.youtube.com/embed/" + importedVideos[i] + "?autoplay=1";
        videoURLs.push(url);
    }
    //createVid();
}

//function createVid()
//{
    //for (let i = 0; i < videoURLs.length; i++) {
        //const parentlocation = document.getElementById('videodiv');
        //let videoInstance = document.createElement('iframe');
        //videoInstance.src = videoURLs[i];
        //videoInstance.width = '420';
        //videoInstance.height = '315';
        //videoInstance.allow = 'autoplay';
        //parentlocation.appendChild(videoInstance);
    //}

//}
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
    videoId: 'tPEE9ZwTmy0',
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
async function startUp()
{
    setVideoButtonDisplay();
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
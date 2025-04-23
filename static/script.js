let selectedItems = [];

function selectItem(button) {
  button.classList.toggle("selected");
  
  const itemText = button.innerText.replace(/[^a-zA-Z]/g, '');
  
  if (button.classList.contains("selected")) {
    selectedItems.push(itemText);
  } else {
    selectedItems = selectedItems.filter(item => item !== itemText);
  }
  
  document.getElementById("selectionCounter").textContent = 
    `${selectedItems.length} item${selectedItems.length !== 1 ? 's' : ''} selected`;
  
  document.getElementById("generateBtn").disabled = selectedItems.length === 0;
}

async function generateStory() {
    if (selectedItems.length === 0) {
        alert("Please select at least 1 item to create a story!");
        return;
    }

    // Show loading animation
    document.getElementById("story").innerHTML = `
        <div class="loading-container">
        <div class="loading-fairy">
            <div class="fairy"></div>
            <div class="fairy-dust"></div>
            <div class="fairy-dust"></div>
            <div class="fairy-dust"></div>
        </div>
        <div style='color:#ff8c42; font-size:1.5em; text-align: center;'>
            ✨ Creating your magical story with ${selectedItems.join(', ')}... ✨
            <br><span style='font-size:0.7em;'>Please wait while the fairies work their magic!</span>
        </div>
        </div>`;
    
    document.getElementById("storyImage").style.display = "none";
    document.getElementById("storyAudio").style.display = "none";

    try {
        const response = await fetch("/generate", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: selectedItems })
        });

        const data = await response.json();

        // Remove loading animation and show results
        document.getElementById("story").innerText = data.story;
        document.getElementById("storyImage").src = data.image_url;
        document.getElementById("storyImage").style.display = "block";
        document.getElementById("storyAudio").src = data.audio_url;
        document.getElementById("storyAudio").style.display = "block";
    } catch (error) {
        document.getElementById("story").innerHTML = 
        `<div style='color:#ff6b9d;'>
            Oh no! The story machine took a nap!<br>
            Please try again later.
        </div>`;
    }
}

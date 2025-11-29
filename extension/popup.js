// Get elements
const topicInput = document.getElementById('topic');
const toneSelect = document.getElementById('tone');
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const output = document.getElementById('output');
const loading = document.getElementById('loading');

// API endpoint (your FastAPI backend)
const API_URL = 'http://localhost:8000/generate';

// Store the generated post
let generatedPost = '';

// Generate post
generateBtn.addEventListener('click', async () => {
  const topic = topicInput.value.trim();
  
  if (!topic) {
    showError('Please enter a topic!');
    return;
  }

  // Show loading
  loading.style.display = 'block';
  output.style.display = 'none';
  copyBtn.style.display = 'none';
  generateBtn.disabled = true;

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: topic,
        tone: toneSelect.value
      })
    });

    const data = await response.json();

    // Hide loading
    loading.style.display = 'none';
    generateBtn.disabled = false;

    if (data.success) {
      generatedPost = data.response;
      showOutput(generatedPost);
      copyBtn.style.display = 'block';
    } else {
      showError(data.error || 'Failed to generate post. Make sure your backend is running!');
    }

  } catch (error) {
    loading.style.display = 'none';
    generateBtn.disabled = false;
    showError('Cannot connect to API. Is your backend running on http://localhost:8000?');
    console.error('Error:', error);
  }
});

// Copy to clipboard
copyBtn.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(generatedPost);
    
    // Change button text temporarily
    const originalText = copyBtn.textContent;
    copyBtn.textContent = '✅ Copied!';
    copyBtn.style.background = '#059669';
    
    setTimeout(() => {
      copyBtn.textContent = originalText;
      copyBtn.style.background = '#10b981';
    }, 2000);
    
  } catch (error) {
    showError('Failed to copy to clipboard');
  }
});

// Show output
function showOutput(text) {
  output.textContent = text;
  output.style.display = 'block';
  output.classList.remove('error');
}

// Show error
function showError(message) {
  output.textContent = '❌ ' + message;
  output.style.display = 'block';
  output.classList.add('error');
}

// Allow Enter key in textarea to trigger generation
topicInput.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === 'Enter') {
    generateBtn.click();
  }
});

// Load saved topic (optional feature)
chrome.storage.local.get(['lastTopic'], (result) => {
  if (result.lastTopic) {
    topicInput.value = result.lastTopic;
  }
});

// Save topic when typing (optional feature)
topicInput.addEventListener('input', () => {
  chrome.storage.local.set({ lastTopic: topicInput.value });
});
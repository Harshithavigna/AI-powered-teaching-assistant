console.log("Script loaded successfully.");

// Tab Switching
function switchTab(tabName) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(el => {
        if (el.id === tabName + '-section') {
            el.classList.remove('hidden');
        } else {
            el.classList.add('hidden');
        }
    });

    const btns = document.querySelectorAll('.tab-btn');
    if (tabName === 'query') {
        btns[0].classList.add('active');
        btns[1].classList.remove('active');
    } else {
        btns[0].classList.remove('active');
        btns[1].classList.add('active');
    }
}

// Fill Query
function fillQuery(element) {
    const input = document.getElementById('queryInput');
    if (input) {
        input.value = element.innerText;
    }
}

// API Calls
async function analyzeQuery() {
    const queryInput = document.getElementById('queryInput');
    const btn = document.getElementById('analyzeBtn');
    const resultBox = document.getElementById('queryResult');

    if (!queryInput || !btn) return;
    const query = queryInput.value;
    if (!query) {
        alert("Please enter a query.");
        return;
    }

    // Loading State
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="btn-icon">⏳</span> Analyzing...';
    btn.disabled = true;

    // Hide previous results
    resultBox.classList.add('hidden');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
        } else {
            // Update Intent
            document.getElementById('resIntent').innerText = data.intent;
            document.getElementById('resIntentConf').innerText = data.intent_conf + "% confidence";
            document.getElementById('resIntentBar').style.width = data.intent_conf + "%";

            // Update Topic
            document.getElementById('resTopic').innerText = data.topic;
            document.getElementById('resTopicConf').innerText = data.topic_conf + "% confidence";
            document.getElementById('resTopicBar').style.width = data.topic_conf + "%";

            // Update Difficulty
            document.getElementById('resDifficulty').innerText = data.difficulty;
            document.getElementById('resDifficultyConf').innerText = data.difficulty_conf + "% confidence";
            document.getElementById('resDifficultyBar').style.width = data.difficulty_conf + "%";

            // Update Keywords
            const kwContainer = document.getElementById('resKeywords');
            kwContainer.innerHTML = '';
            data.keywords.forEach(kw => {
                const span = document.createElement('span');
                span.className = 'keyword-pill';
                span.innerText = kw;
                kwContainer.appendChild(span);
            });

            // Update Suggestion
            document.getElementById('resSuggestion').innerText = data.suggestion;

            // Show Results
            resultBox.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Fetch Error:', error);
        alert('Failed to connect to server.');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

async function getRecommendation() {
    const topic = document.getElementById('topicInput').value;
    const difficulty = document.getElementById('difficultyInput').value;
    const score = parseFloat(document.getElementById('scoreInput').value);
    const attempts = parseInt(document.getElementById('attemptsInput').value);
    const time = parseFloat(document.getElementById('timeInput').value);
    const resultBox = document.getElementById('adaptiveResult');

    const payload = {
        topic: topic,
        difficulty: difficulty,
        score: score,
        attempts: attempts,
        time_spent: time
    };

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (data.error) {
            alert(data.error);
        } else {
            // Next Topic
            document.getElementById('recTopic').innerText = data.next_topic;
            document.getElementById('recTopicConf').innerText = (data.next_topic_conf || 85) + "% confidence";
            document.getElementById('recTopicBar').style.width = (data.next_topic_conf || 85) + "%";

            // Action
            document.getElementById('recAction').innerText = data.action;
            document.getElementById('recActionConf').innerText = (data.action_conf || 90) + "% confidence";
            document.getElementById('recActionBar').style.width = (data.action_conf || 90) + "%";

            // Difficulty Adjustment
            document.getElementById('recDiff').innerText = data.difficulty_adjustment;
            document.getElementById('recDiffConf').innerText = (data.difficulty_adjustment_conf || 95) + "% confidence";
            document.getElementById('recDiffBar').style.width = (data.difficulty_adjustment_conf || 95) + "%";

            // Reasoning
            document.getElementById('recReasoning').innerText = data.reasoning || "Based on score and attempts analysis.";

            // Show Apply Button Logic
            const applyBtn = document.getElementById('applyBtn');
            if (applyBtn) {
                applyBtn.onclick = function () {
                    applyRecommendation(data.next_topic, data.difficulty_adjustment);
                };
            }

            resultBox.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get recommendation.');
    }
}

function applyRecommendation(nextTopic, diffAdj) {
    // Update Topic
    const topicSelect = document.getElementById('topicInput');
    // Check if topic exists in options, if not, alert or add it
    let topicExists = false;
    for (let i = 0; i < topicSelect.options.length; i++) {
        if (topicSelect.options[i].value === nextTopic) {
            topicSelect.selectedIndex = i;
            topicExists = true;
            break;
        }
    }
    if (!topicExists) {
        // Option to add it dynamically or just alert
        alert("Next topic '" + nextTopic + "' is not in the dropdown list!");
    }

    // Update Difficulty (Simple logic for now: Increase -> Next level, Decrease -> Prev level)
    const diffSelect = document.getElementById('difficultyInput');
    const levels = ["Beginner", "Intermediate", "Advanced"];
    let currentIdx = levels.indexOf(diffSelect.value);

    if (diffAdj === "Increase" && currentIdx < levels.length - 1) {
        diffSelect.value = levels[currentIdx + 1];
    } else if (diffAdj === "Decrease" && currentIdx > 0) {
        diffSelect.value = levels[currentIdx - 1];
    }

    // Reset inputs for next simulation
    document.getElementById('scoreInput').value = "";
    document.getElementById('attemptsInput').value = "0";
    document.getElementById('timeInput').value = "0";

    // Hide results
    document.getElementById('adaptiveResult').classList.add('hidden');

    // Scroll to top of form
    document.querySelector('.form-container').scrollIntoView({ behavior: 'smooth' });
}

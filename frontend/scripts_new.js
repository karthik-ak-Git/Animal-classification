// ========================================
// PROFESSIONAL ANIMAL AI CLASSIFICATION
// Enhanced JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const fileInput = document.getElementById('file-input');
    const uploadZone = document.getElementById('upload-zone');
    const uploadPanel = document.getElementById('upload-panel');
    const previewSection = document.getElementById('preview-section');
    const processingState = document.getElementById('processing-state');
    const resultsPanel = document.getElementById('results-panel');
    const previewImage = document.getElementById('preview-image');
    const previewFilename = document.getElementById('preview-filename');
    const previewSize = document.getElementById('preview-size');
    const analyzeBtn = document.getElementById('analyze-btn');

    // Result elements
    const resultIcon = document.getElementById('result-icon');
    const resultName = document.getElementById('result-name');
    const confidenceBar = document.getElementById('confidence-bar');
    const confidenceValue = document.getElementById('confidence-value');
    const predictionsList = document.getElementById('predictions-list');

    let currentImageData = null;
    let currentPrediction = null;
    let allClasses = [];
    let isProcessing = false; // Flag to prevent duplicate uploads

    // Animal Emoji Map
    const animalEmojis = {
        'Dog': '🐕', 'German Shepherd': '🐕‍🦺', 'Golden Retriever': '🦮', 'Labrador': '🐕‍🦺', 'Pug': '🐶',
        'Domestic Dog': '🐕',
        'Cat': '🐈', 'Persian Cat': '😺', 'Siamese Cat': '🐈', 'Bengal Cat': '🐈‍⬛', 'Maine Coon': '🐈',
        'Bird': '🐦', 'Eagle': '🦅', 'Owl': '🦉', 'Parrot': '🦜', 'Amazon parrot': '🦜',
        'Swan': '🦢', 'Duck': '🦆', 'Ducks': '🦆', 'Penguin': '🐧', 'Flamingo': '🦩',
        'Hummingbird': '🐦', 'Peacock': '🦚', 'Ostrich': '🦤', 'Crows': '🐦‍⬛', 'Cuckoo': '🐦',
        'Cockatiel': '🦜', 'Kingfishers': '🐦', 'Woodpeckers': '🦜', 'Falcons': '🦅',
        'House Sparrows': '🐦', 'pigeons': '🦜', 'Swallows': '🐦',
        'Bear': '🐻', 'Polar_Bear': '🐻‍❄️', 'Grizzly_Bear': '🐻', 'American_Black_Bear': '🐻',
        'Asiatic_Black_Bear': '🐻', 'Sloth_Bear': '🐻', 'Sun_Bear': '🐻',
        'Panda': '🐼', 'Giant Panda': '🐼', 'Red Panda': '🐼',
        'Lion': '🦁', 'African Lion': '🦁', 'Asiatic Lion': '🦁',
        'Tiger': '🐯', 'Bengal Tiger': '🐅', 'Siberian Tiger': '🐯',
        'Elephant': '🐘', 'African Elephant': '🐘', 'Asian Elephant': '🐘',
        'Giraffe': '🦒', 'Reticulated Giraffe': '🦒', 'Masai Giraffe': '🦒',
        'Horse': '🐴', 'Arabian Horse': '🐴', 'Thoroughbred': '🐴', 'Clydesdale': '🐎',
        'Cow': '🐄', 'Jersey Cow': '🐄', 'Angus': '🐂', 'Domestic Cattle': '🐮',
        'Deer': '🦌', 'Red Deer': '🦌', 'White-tailed Deer': '🦌', 'Mule_Deer': '🦌',
        'Dolphin': '🐬', 'Bottlenose Dolphin': '🐬', 'Spinner Dolphin': '🐬',
        'Kangaroo': '🦘', 'Red Kangaroo': '🦘', 'Eastern Grey Kangaroo': '🦘',
        'Zebra': '🦓', 'Plains Zebra': '🦓', 'Mountain Zebra': '🦓',
        'Wildcat': '🐆', 'African Wildcat': '🐆'
    };

    // Get emoji for animal
    function getAnimalEmoji(name) {
        if (animalEmojis[name]) return animalEmojis[name];

        for (const [key, emoji] of Object.entries(animalEmojis)) {
            if (name.includes(key) || key.includes(name.split('_')[0])) {
                return emoji;
            }
        }
        return '🐾';
    }

    // Format class name
    function formatClassName(name) {
        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    // Load classes count and populate feedback dropdown
    async function loadClassesCount() {
        try {
            const response = await fetch('/classes');
            const data = await response.json();
            if (data.num_classes) {
                document.getElementById('class-count').textContent = data.num_classes;
            }
            if (data.classes) {
                allClasses = data.classes;
                populateFeedbackDropdown();
            }
        } catch (error) {
            console.error('Failed to load classes:', error);
        }
    }

    // Populate feedback species dropdown
    function populateFeedbackDropdown() {
        const correctSpeciesSelect = document.getElementById('correct-species-select');
        if (!correctSpeciesSelect) return;

        // Clear existing options except the first one
        correctSpeciesSelect.innerHTML = '<option value="">Select correct species...</option>';

        // Add all classes as options
        allClasses.forEach(className => {
            const option = document.createElement('option');
            option.value = className;
            option.textContent = formatClassName(className);
            correctSpeciesSelect.appendChild(option);
        });
    }

    // File Upload Handlers (prevent duplicate processing)
    fileInput.addEventListener('change', function (e) {
        if (e.target.files.length > 0 && !isProcessing) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and Drop
    // Clicking the upload zone should open the file dialog, but if the user
    // clicks the internal "Browse Files" button (which also opens the dialog),
    // we must ignore the outer zone click to avoid opening the file dialog twice.
    uploadZone.addEventListener('click', function (e) {
        // If click originated from inside an element with class 'btn-browse', ignore
        try {
            if (e.target && e.target.closest && e.target.closest('.btn-browse')) {
                return;
            }
        } catch (err) {
            // ignore and continue
        }
        fileInput.click();
    });

    uploadZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', function () {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // Handle File Selection
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            showToast('Please select a valid image file', 'error');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            showToast('Image must be less than 10MB', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            currentImageData = e.target.result;
            previewImage.src = e.target.result;
            previewFilename.textContent = file.name;
            previewSize.textContent = formatFileSize(file.size);

            // Show preview
            uploadZone.style.display = 'none';
            previewSection.style.display = 'block';
            resultsPanel.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    // Format file size
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    // Clear Image
    window.clearImage = function () {
        fileInput.value = '';
        currentImageData = null;
        currentPrediction = null;
        isProcessing = false; // Reset processing flag
        uploadZone.style.display = 'block';
        previewSection.style.display = 'none';
        processingState.style.display = 'none';
        resultsPanel.style.display = 'none';

        // Hide feedback section if visible
        const feedbackSection = document.getElementById('feedback-section');
        if (feedbackSection) {
            feedbackSection.style.display = 'none';
        }
    };

    // Analyze Image (prevent duplicate submissions)
    window.analyzeImage = async function () {
        if (!currentImageData) {
            showToast('No image selected', 'error');
            return;
        }

        if (isProcessing) {
            showToast('Already processing...', 'info');
            return;
        }

        // Set processing flag
        isProcessing = true;

        // Show processing state
        previewSection.style.display = 'none';
        processingState.style.display = 'block';
        resultsPanel.style.display = 'none';

        // Hide feedback section if visible
        const feedbackSection = document.getElementById('feedback-section');
        if (feedbackSection) {
            feedbackSection.style.display = 'none';
        }

        try {
            // Convert base64 to blob
            const blob = dataURItoBlob(currentImageData);
            const formData = new FormData();
            formData.append('file', blob, 'image.jpg');

            // Make prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Prediction failed');
            }

            const data = await response.json();
            currentPrediction = data;

            // Show results
            displayResults(data);
            showToast('Analysis complete!', 'success');

        } catch (error) {
            console.error('Prediction error:', error);
            showToast(error.message || 'Prediction failed', 'error');
            previewSection.style.display = 'block';
            processingState.style.display = 'none';
        } finally {
            // Reset processing flag
            isProcessing = false;
        }
    };

    // Display Results
    function displayResults(data) {
        // Hide processing, show results
        processingState.style.display = 'none';
        resultsPanel.style.display = 'block';

        // Update primary result
        const emoji = getAnimalEmoji(data.prediction);
        resultIcon.textContent = emoji;
        resultName.textContent = formatClassName(data.prediction);

        // Update confidence
        const confidencePercent = Math.round(data.confidence * 100);
        confidenceValue.textContent = confidencePercent + '%';

        // Animate confidence bar
        setTimeout(() => {
            confidenceBar.style.width = confidencePercent + '%';
        }, 100);

        // Display top predictions
        predictionsList.innerHTML = '';
        if (data.breeds && data.scores) {
            data.breeds.forEach((breed, index) => {
                const score = Math.round(data.scores[index] * 100);
                const item = document.createElement('div');
                item.className = 'prediction-item';
                item.innerHTML = `
                    <div class="prediction-info">
                        <div class="prediction-rank">${index + 1}</div>
                        <div class="prediction-species">${formatClassName(breed)}</div>
                    </div>
                    <div class="prediction-score">${score}%</div>
                `;
                predictionsList.appendChild(item);
            });
        }

        // Smooth scroll to results
        setTimeout(() => {
            resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 200);
    }

    // Download Results
    window.downloadResults = function () {
        if (!currentPrediction) {
            showToast('No results to download', 'error');
            return;
        }

        const results = {
            prediction: formatClassName(currentPrediction.prediction),
            confidence: Math.round(currentPrediction.confidence * 100) + '%',
            timestamp: new Date().toISOString(),
            topPredictions: currentPrediction.breeds.map((breed, idx) => ({
                rank: idx + 1,
                species: formatClassName(breed),
                confidence: Math.round(currentPrediction.scores[idx] * 100) + '%'
            }))
        };

        const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `animal-classification-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);

        showToast('Results downloaded!', 'success');
    };

    // Convert data URI to Blob
    function dataURItoBlob(dataURI) {
        const byteString = atob(dataURI.split(',')[1]);
        const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: mimeString });
    }

    // Show Toast Notification
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = type === 'success' ? 'check-circle-fill' :
            type === 'error' ? 'exclamation-circle-fill' : 'info-circle-fill';

        toast.innerHTML = `
            <i class="bi bi-${icon}"></i>
            <span>${message}</span>
        `;

        const container = document.getElementById('toast-container');
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'toastSlideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Toggle Feedback Section
    window.toggleFeedback = function () {
        const feedbackSection = document.getElementById('feedback-section');
        if (!feedbackSection) return;

        if (!currentPrediction) {
            showToast('No prediction available', 'error');
            return;
        }

        const isVisible = feedbackSection.style.display === 'block';
        feedbackSection.style.display = isVisible ? 'none' : 'block';

        if (!isVisible) {
            // Update current prediction display - use correct ID from HTML
            const currentPredictionEl = document.getElementById('feedback-current');
            if (currentPredictionEl) {
                currentPredictionEl.textContent = formatClassName(currentPrediction.prediction);
            }

            // Scroll feedback into view
            setTimeout(() => {
                feedbackSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        } else {
            // Clear form when hiding - use correct IDs from HTML
            const correctSpeciesSelect = document.getElementById('correct-species-select');
            const feedbackComments = document.getElementById('feedback-comments');
            if (correctSpeciesSelect) correctSpeciesSelect.value = '';
            if (feedbackComments) feedbackComments.value = '';
        }
    };

    // Submit Feedback
    window.submitFeedback = async function () {
        const correctSpeciesSelect = document.getElementById('correct-species-select');
        const feedbackComments = document.getElementById('feedback-comments');

        if (!correctSpeciesSelect || !feedbackComments) {
            showToast('Feedback form not found', 'error');
            return;
        }

        const correctSpecies = correctSpeciesSelect.value;
        const comments = feedbackComments.value.trim();

        // Validation
        if (!correctSpecies) {
            showToast('Please select the correct species', 'error');
            correctSpeciesSelect.focus();
            return;
        }

        if (!currentPrediction) {
            showToast('No prediction data available', 'error');
            return;
        }

        // Prepare feedback data with image
        const feedbackData = {
            predicted_class: currentPrediction.prediction,
            correct_class: correctSpecies,
            confidence: currentPrediction.confidence,
            comments: comments || '',
            timestamp: new Date().toISOString(),
            image_data: currentImageData  // Include the image for retraining
        };

        try {
            // Submit feedback to backend
            const response = await fetch('/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(feedbackData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to submit feedback');
            }

            const result = await response.json();

            // Show success message with retraining info
            let successMessage = 'Feedback submitted successfully! Thank you.';
            if (result.retraining_triggered) {
                successMessage += ' 🎓 Model retraining started in background.';
            }
            showToast(successMessage, 'success');

            // Clear and hide feedback form
            correctSpeciesSelect.value = '';
            feedbackComments.value = '';
            document.getElementById('feedback-section').style.display = 'none';

        } catch (error) {
            console.error('Feedback submission error:', error);
            showToast(error.message || 'Failed to submit feedback', 'error');
        }
    };

    // Cancel Feedback
    window.cancelFeedback = function () {
        const feedbackSection = document.getElementById('feedback-section');
        const correctSpeciesSelect = document.getElementById('correct-species-select');
        const feedbackComments = document.getElementById('feedback-comments');

        // Clear form
        if (correctSpeciesSelect) correctSpeciesSelect.value = '';
        if (feedbackComments) feedbackComments.value = '';

        // Hide section
        if (feedbackSection) feedbackSection.style.display = 'none';

        showToast('Feedback cancelled', 'info');
    };

    // Initialize
    loadClassesCount();
});

// Add toast slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes toastSlideOut {
        to {
            opacity: 0;
            transform: translateX(120%);
        }
    }
`;
document.head.appendChild(style);

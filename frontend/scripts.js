// ============================================document.addEventListener('DOMContentLoaded', function () {

// MODERN ANIMAL CLASSIFICATION AI - SCRIPTS    // DOM Elements

// ============================================    const submitCorrectionButton = document.getElementById('submit-correction');

const correctionDropdown = document.getElementById('correction-dropdown');

document.addEventListener('DOMContentLoaded', function () {
    const animalClassesList = document.getElementById('animal-classes-list');

    // DOM Elements    const imageUpload = document.getElementById('image-upload');

    const imageUpload = document.getElementById('image-upload'); const predictButton = document.getElementById('predict-button');

    const predictButton = document.getElementById('predict-button'); const resultContainer = document.getElementById('result-container');

    const resultContainer = document.getElementById('result-container'); const feedbackCard = document.getElementById('feedback-card');

    const uploadArea = document.getElementById('upload-area'); const feedbackReceivedAlert = document.getElementById('feedback-received-alert');

    const imagePreviewContainer = document.getElementById('image-preview-container'); const showFeedbackBtn = document.getElementById('show-feedback-btn');

    const imagePreview = document.getElementById('image-preview'); const uploadArea = document.getElementById('upload-area');

    const previewFilename = document.getElementById('preview-filename'); const imagePreviewContainer = document.getElementById('image-preview-container');

    const processingIndicator = document.getElementById('processing-indicator'); const imagePreview = document.getElementById('image-preview');

    const copyBreedBtn = document.getElementById('copy-breed-btn');

    // Result elements    const toastContainer = document.getElementById('toast-container');

    const predictionName = document.getElementById('prediction-name');

    const predictionIcon = document.getElementById('prediction-icon');    // Prediction display elements

    const confidencePercentage = document.getElementById('confidence-percentage'); const classEmoji = document.getElementById('class-emoji');

    const confidenceBadge = document.getElementById('confidence-badge'); const mainClassLabel = document.getElementById('main-class-label');

    const confidenceBar = document.getElementById('confidence-bar'); const breedDisplay = document.getElementById('breed-display');

    const confidenceText = document.getElementById('confidence-text'); const breedName = document.getElementById('breed-name');

    const predictionsList = document.getElementById('predictions-list'); const confidenceText = document.getElementById('confidence-text');



    let currentImageData = null; let animalClasses = [];

    let currentBreedName = '';

    // Animal emoji mapping

    const animalEmojis = {    // Animal emoji mapping

        'Dog': '🐶', 'German Shepherd': '🐕', 'Golden Retriever': '🦮', 'Labrador': '🐕‍🦺', 'Pug': '🐶', const animalEmojis = {

            'Cat': '🐱', 'Persian Cat': '🐱', 'Siamese Cat': '🐈', 'Bengal Cat': '🐈', 'Maine Coon': '🐈‍⬛', 'Dog': '🐶',

            'Bird': '🐦', 'Eagle': '🦅', 'Owl': '🦉', 'Parrot': '🦜', 'Swan': '🦢', 'Duck': '🦆', 'Cat': '🐱',

            'Penguin': '🐧', 'Flamingo': '🦩', 'Hummingbird': '🐦', 'Peacock': '🦚', 'Bird': '🐦',

            'Bear': '🐻', 'Polar_Bear': '🐻‍❄️', 'Grizzly_Bear': '🐻', 'Panda': '🐼', 'Giant Panda': '🐼', 'Red Panda': '🐼', 'Bear': '🐻',

            'Lion': '🦁', 'African Lion': '🦁', 'Asiatic Lion': '🦁', 'Lion': '🦁',

            'Tiger': '🐯', 'Bengal Tiger': '🐅', 'Siberian Tiger': '🐯', 'Tiger': '🐯',

            'Elephant': '🐘', 'African Elephant': '🐘', 'Asian Elephant': '🐘', 'Elephant': '🐘',

            'Giraffe': '🦒', 'Reticulated Giraffe': '🦒', 'Masai Giraffe': '🦒', 'Giraffe': '🦒',

            'Horse': '🐎', 'Arabian Horse': '🐴', 'Thoroughbred': '🐴', 'Clydesdale': '🐎', 'Horse': '🐎',

            'Cow': '🐮', 'Jersey Cow': '🐄', 'Angus': '🐂', 'Domestic Cattle': '🐮', 'Cow': '🐮',

            'Deer': '🦌', 'Red Deer': '🦌', 'White-tailed Deer': '🦌', 'Mule_Deer': '🦌', 'Deer': '🦌',

            'Dolphin': '🐬', 'Bottlenose Dolphin': '🐬', 'Spinner Dolphin': '🐬', 'Dolphin': '🐬',

            'Kangaroo': '🦘', 'Red Kangaroo': '🦘', 'Eastern Grey Kangaroo': '🦘', 'Kangaroo': '🦘',

            'Zebra': '🦓', 'Plains Zebra': '🦓', 'Mountain Zebra': '🦓', 'Panda': '🐼',

            'Wildcat': '🐆', 'African Wildcat': '🐆', 'Zebra': '🦓',

            'Ostrich': '🦤', 'Crows': '🐦‍⬛', 'Pigeons': '🐦', 'Sparrow': '🐦'        'Penguin': '🐧',

        }; 'Owl': '🦉',

        'Eagle': '🦅',

        // Get emoji for animal        'Parrot': '🦜',

        function getAnimalEmoji(animalName) { 'Swan': '🦢',

            // Check direct match        'Duck': '🦆',

            if (animalEmojis[animalName]) {
                'Crow': '🐦',

            return animalEmojis[animalName]; 'Sparrow': '🐦',

        } 'Hummingbird': '🐦',

        'Woodpecker': '🐦',

        // Check if name contains any keyword        'Kingfisher': '🐦',

        for (const [key, emoji] of Object.entries(animalEmojis)) {
        'Falcon': '🦅',

            if (animalName.includes(key) || key.includes(animalName.split('_')[0])) {
            'Ostrich': '🦃',

                return emoji; 'Pigeon': '🕊️',

            } 'Swallow': '🐦',

        } 'Cuckoo': '🐦'

};

return '🐾'; // Default

    }    // Toast notification system

function showToast(message, type = 'info', duration = 4000) {

    // Format class name for display        const toast = document.createElement('div');

    function formatClassName(name) {
        toast.className = `toast ${type}`;

        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()); toast.textContent = message;

    }

    toastContainer.appendChild(toast);

    // Drag and drop functionality

    uploadArea.addEventListener('dragover', function (e) {        // Auto remove after duration

        e.preventDefault(); setTimeout(() => {

            uploadArea.classList.add('dragover'); toast.style.animation = 'slideOutRight 0.3s cubic-bezier(0.4, 0, 0.2, 1)';

        }); setTimeout(() => {

            if (toast.parentNode) {

                uploadArea.addEventListener('dragleave', function () {
                    toast.parentNode.removeChild(toast);

                    uploadArea.classList.remove('dragover');
                }

    });
    }, 300);

}, duration);

uploadArea.addEventListener('drop', function (e) { }

        e.preventDefault();

uploadArea.classList.remove('dragover');    // Fetch classes from backend

const files = e.dataTransfer.files; async function loadClassOptions() {

    if (files.length > 0) {
        try {

            handleFileSelect(files[0]); const res = await fetch('/classes');

        }            const data = await res.json();

    }); animalClasses = data.classes || [];

    populateClassDropdowns();

    // File input change        } catch (error) {

    imageUpload.addEventListener('change', function (e) {
        console.error("Error loading class options:", error);

        if (e.target.files.length > 0) {
            showToast('Failed to load animal classes', 'error');

            handleFileSelect(e.target.files[0]);
        }

    }    }

    });

// Populate dropdowns

// Handle file selection    function populateClassDropdowns() {

function handleFileSelect(file) {
    correctionDropdown.innerHTML = '<option value="">Select correct class...</option>';

    if (!file.type.startsWith('image/')) {

        showToast('Please select a valid image file', 'error'); animalClasses.forEach((animal) => {

            return; const displayName = animal.replace(/_/g, ' ');

        }            const option = document.createElement('option');

        option.value = animal;

        if (file.size > 10 * 1024 * 1024) {
            option.textContent = displayName;

            showToast('Image size must be less than 10MB', 'error'); correctionDropdown.appendChild(option);

            return;
        });

    }
}



const reader = new FileReader();    // Get emoji for animal class

reader.onload = function (e) {
    function getAnimalEmoji(className) {

        currentImageData = e.target.result; const baseClass = getBaseClass(className);

        imagePreview.src = e.target.result; return animalEmojis[baseClass] || '🐾';

        previewFilename.textContent = file.name;
    }



    // Show preview, hide upload area    // Get base class from full class name

    uploadArea.classList.add('d-none'); function getBaseClass(className) {

        imagePreviewContainer.classList.remove('d-none'); const cleanName = className.replace(/_/g, ' ');

        predictButton.disabled = false; for (const [baseClass, emoji] of Object.entries(animalEmojis)) {

            if (cleanName.includes(baseClass)) {

                // Hide previous results                return baseClass;

                resultContainer.classList.add('d-none');
            }

        };
    }

    reader.readAsDataURL(file); return cleanName.split(' ')[0];

}    }



// Remove image    // Handle image upload

window.removeImage = function () {
    function handleImageUpload(file) {

        imageUpload.value = ''; if (!file) return;

        currentImageData = null;

        uploadArea.classList.remove('d-none');        // Validate file type

        imagePreviewContainer.classList.add('d-none'); if (!file.type.startsWith('image/')) {

            predictButton.disabled = true; showToast('Please select a valid image file', 'error');

            resultContainer.classList.add('d-none'); return;

        };
    }



    // Reset app        // Validate file size (10MB limit)

    window.resetApp = function () {
        if (file.size > 10 * 1024 * 1024) {

            removeImage(); showToast('Image size must be less than 10MB', 'error');

        }; return;

    }

    // Predict button click

    predictButton.addEventListener('click', async function () {
        const reader = new FileReader();

        if (!currentImageData) {
            reader.onload = function (e) {

                showToast('Please select an image first', 'error'); imagePreview.src = e.target.result;

                return; imagePreviewContainer.classList.remove('d-none');

            }            uploadArea.classList.add('d-none');

            predictButton.disabled = false;

            // Show processing indicator

            predictButton.disabled = true;            // Animate in the preview

            processingIndicator.classList.remove('d-none'); imagePreviewContainer.style.animation = 'slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1)';

            resultContainer.classList.add('d-none');
        };

        reader.readAsDataURL(file);

        try { }

            // Convert base64 to blob

            const blob = dataURItoBlob(currentImageData);    // Remove image

        const formData = new FormData(); window.removeImage = function () {

            formData.append('file', blob, 'image.jpg'); imageUpload.value = '';

            imagePreviewContainer.classList.add('d-none');

            // Make prediction request        uploadArea.classList.remove('d-none');

            const response = await fetch('/predict', {
                predictButton.disabled = true;

                method: 'POST', resultContainer.classList.add('d-none');

                body: formData

            });        // Reset animations

            imagePreviewContainer.style.animation = '';

            if (!response.ok) { };

            throw new Error(`Server error: ${response.status}`);

        }    // Animated prediction display

        async function displayPrediction(result) {

            const data = await response.json(); const baseClass = getBaseClass(result.prediction);

            displayPrediction(data); const emoji = getAnimalEmoji(result.prediction);

            const confidence = (result.confidence * 100).toFixed(1);

        } catch (error) {

            console.error('Prediction error:', error);        // Reset display

            showToast('Prediction failed. Please try again.', 'error'); resultContainer.classList.remove('d-none');

        } finally {
            breedDisplay.classList.add('d-none');

            predictButton.disabled = false; copyBreedBtn.classList.add('d-none');

            processingIndicator.classList.add('d-none');

        }        // Show main class with animation

    }); classEmoji.textContent = emoji;

    mainClassLabel.textContent = baseClass;

    // Display prediction results

    function displayPrediction(data) {        // Wait for main class animation, then show breed

        // Update main prediction        setTimeout(() => {

        const emoji = getAnimalEmoji(data.prediction); if (result.breeds && result.breeds.length > 0) {

            predictionIcon.textContent = emoji; currentBreedName = result.breeds[0];

            predictionName.textContent = formatClassName(data.prediction); breedName.textContent = currentBreedName;

            confidenceText.textContent = `Confidence: ${confidence}%`;

            // Update confidence                breedDisplay.classList.remove('d-none');

            const confidencePercent = Math.round(data.confidence * 100); copyBreedBtn.classList.remove('d-none');

            confidencePercentage.textContent = `${confidencePercent}%`;
        }

        confidenceBar.style.width = `${confidencePercent}%`;
    }, 1500);

    confidenceText.textContent = `Confidence: ${confidencePercent}%`;

    showFeedbackBtn.classList.remove('d-none');

    // Set confidence badge color        window.currentPrediction = result.prediction;

    if (confidencePercent >= 80) { }

    confidenceBadge.style.background = 'var(--gradient-success)';

} else if (confidencePercent >= 60) {    // Copy breed name to clipboard

    confidenceBadge.style.background = 'var(--gradient-primary)'; copyBreedBtn.addEventListener('click', async () => {

    } else {
        try {

            confidenceBadge.style.background = 'var(--gradient-purple)'; await navigator.clipboard.writeText(currentBreedName);

        }            copyBreedBtn.classList.add('copy-success');

        copyBreedBtn.innerHTML = '<i class="bi bi-check me-1"></i>Copied!';

        // Display top predictions            showToast('Breed name copied to clipboard', 'success', 2000);

        predictionsList.innerHTML = '';

        if(data.breeds && data.scores) {
            setTimeout(() => {

                data.breeds.forEach((breed, index) => {
                    copyBreedBtn.classList.remove('copy-success');

                    const score = Math.round(data.scores[index] * 100); copyBreedBtn.innerHTML = '<i class="bi bi-clipboard me-1"></i>Copy Breed';

                    const item = document.createElement('div');
                }, 2000);

                item.className = 'prediction-item';
            } catch (err) {

                item.innerHTML = `            console.error('Failed to copy: ', err);

                    <div class="prediction-item-left">            showToast('Failed to copy breed name', 'error');

                        <div class="rank-badge">${index + 1}</div>        }

                        <div class="prediction-item-name">${formatClassName(breed)}</div>    });

                    </div>

                    <div class="prediction-item-score">${score}%</div>    // Image upload event

                `; imageUpload.addEventListener('change', (e) => {

                    predictionsList.appendChild(item); const file = e.target.files[0];

                }); handleImageUpload(file);

            }
    });



    // Show results    // Drag and drop functionality

    resultContainer.classList.remove('d-none'); uploadArea.addEventListener('dragover', (e) => {

        e.preventDefault();

        // Smooth scroll to results        uploadArea.classList.add('dragover');

        setTimeout(() => { });

        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    }, 100); uploadArea.addEventListener('dragleave', (e) => {

    }        e.preventDefault();

    uploadArea.classList.remove('dragover');

    // Convert data URI to Blob    });

    function dataURItoBlob(dataURI) {

        const byteString = atob(dataURI.split(',')[1]); uploadArea.addEventListener('drop', (e) => {

            const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]; e.preventDefault();

            const ab = new ArrayBuffer(byteString.length); uploadArea.classList.remove('dragover');

            const ia = new Uint8Array(ab); const file = e.dataTransfer.files[0];

            for (let i = 0; i < byteString.length; i++) {
                if (file && file.type.startsWith('image/')) {

                    ia[i] = byteString.charCodeAt(i); imageUpload.files = e.dataTransfer.files;

                } handleImageUpload(file);

                return new Blob([ab], { type: mimeString });
            } else {

            } showToast('Please drop a valid image file', 'error');

        }

    // Show toast notification    });

    function showToast(message, type = 'info') {

                const toast = document.createElement('div');    // Click to upload

                toast.className = `toast-notification toast-${type}`; uploadArea.addEventListener('click', () => {

                    toast.innerHTML = `        imageUpload.click();

            <i class="bi bi-${type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>    });

            <span>${message}</span>

        `;    // Prediction handler

                    predictButton.addEventListener('click', async () => {

                        document.body.appendChild(toast); const imageFile = imageUpload.files[0];

                        if (!imageFile) {

                            setTimeout(() => {
                                showToast('Please upload an image first', 'error');

                                toast.style.opacity = '1'; return;

                                toast.style.transform = 'translateY(0)';
                            }

        }, 10);

                    const formData = new FormData();

                    setTimeout(() => {
                        formData.append('file', imageFile);

                        toast.style.opacity = '0';

                        toast.style.transform = 'translateY(-20px)'; predictButton.disabled = true;

                        setTimeout(() => toast.remove(), 300); predictButton.innerHTML = '<span class="loading me-2"></span>Analyzing...';

                    }, 3000);

                }        try {

                    const res = await fetch('/predict', { method: 'POST', body: formData });

                    // Initialize - Load available classes

                    async function loadClasses() {
                        if (!res.ok) {

                            try {
                                throw new Error(`HTTP error! status: ${res.status}`);

                                const response = await fetch('/classes');
                            }

            const data = await response.json();

                            if (data.num_classes) {
                                const result = await res.json();

                                document.getElementById('total-classes').textContent = data.num_classes;

                            } if (result.error) {

                            } catch (error) {
                                throw new Error(result.error);

                                console.error('Failed to load classes:', error);
                            }

                        }

                    } await displayPrediction(result);

                    showToast('Analysis completed successfully', 'success');

                    loadClasses();
                } catch (err) {

                }); console.error('Prediction error:', err);



        // Add toast notification styles dynamically            // Show error in prediction card

        const toastStyles = document.createElement('style'); classEmoji.textContent = '❌';

        toastStyles.textContent = `            mainClassLabel.textContent = 'Error';

    .toast-notification {            breedDisplay.classList.remove('d-none');

        position: fixed;            breedName.textContent = 'Failed to analyze image';

        top: 20px;            confidenceText.textContent = 'Please try again';

        right: 20px;            resultContainer.classList.remove('d-none');

        padding: 1rem 1.5rem;

        background: rgba(30, 41, 59, 0.95);            showToast('Failed to analyze image. Please try again.', 'error');

        backdrop-filter: blur(10px);        } finally {

        border: 1px solid rgba(99, 102, 241, 0.3);            predictButton.disabled = false;

        border-radius: 1rem;            predictButton.innerHTML = '<i class="bi bi-search me-2"></i>Analyze Image';

        color: #f1f5f9;        }

        display: flex;    });

        align-items: center;

        gap: 0.5rem;    // Feedback submit

        z-index: 9999;    submitCorrectionButton.addEventListener('click', async () => {

        opacity: 0;        const corrected = correctionDropdown.value;

        transform: translateY(-20px);        const imageFile = imageUpload.files[0];

        transition: all 0.3s ease;

        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);        if (!corrected) {

    }            showToast('Please select a correct class', 'error');

                return;

    .toast-error {        }

        border-color: #ef4444;

    }        if (!imageFile) {

                showToast('No image to submit feedback for', 'error');

    .dragover {            return;

        border-color: #6366f1 !important;        }

        background: rgba(99, 102, 241, 0.05) !important;

    }        const formData = new FormData();

`; formData.append('file', imageFile);

        document.head.appendChild(toastStyles); formData.append('predicted', window.currentPrediction || 'Unknown');

        formData.append('actual', corrected);

        submitCorrectionButton.disabled = true;
        submitCorrectionButton.innerHTML = '<span class="loading me-2"></span>Submitting...';

        try {
            const res = await fetch('/feedback', { method: 'POST', body: formData });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const result = await res.json();

            showToast(result.message, 'success');
            feedbackCard.classList.remove('show');
            submitCorrectionButton.innerHTML = '<i class="bi bi-check me-1"></i>Submitted!';

            setTimeout(() => {
                submitCorrectionButton.innerHTML = '<i class="bi bi-check me-1"></i>Submit Correction';
                submitCorrectionButton.disabled = false;
            }, 3000);
        } catch (e) {
            console.error('Feedback error:', e);
            showToast('Error submitting feedback. Please try again.', 'error');
            submitCorrectionButton.innerHTML = '<i class="bi bi-check me-1"></i>Submit Correction';
            submitCorrectionButton.disabled = false;
        }
    });

    // Toggle feedback
    showFeedbackBtn.addEventListener('click', () => {
        new bootstrap.Collapse(feedbackCard, { toggle: true });
    });

    // Add slideOutRight animation for toast removal
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOutRight {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }
    `;
    document.head.appendChild(style);

    // Initialize
    loadClassOptions();
});

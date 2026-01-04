document.addEventListener('DOMContentLoaded', () => {
    const cropForm = document.getElementById('cropForm');
    const fertilizerForm = document.getElementById('fertilizerForm');
    const loadingOverlay = document.getElementById('loading');

    function showLoading() {
        if (loadingOverlay) loadingOverlay.style.display = 'flex';
    }

    function hideLoading() {
        if (loadingOverlay) loadingOverlay.style.display = 'none';
    }

    if (cropForm) {
        cropForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            showLoading(); // Show loader
            document.getElementById('result').style.display = 'none'; // Hide previous result

            const formData = new FormData(cropForm);
            const data = Object.fromEntries(formData);

            for (let key in data) {
                data[key] = parseFloat(data[key]);
            }

            try {
                // Simulate a small delay for better UX (so loader is visible)
                await new Promise(r => setTimeout(r, 800));

                const response = await fetch('/predict-crop', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });

                const result = await response.json();
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';

                if (result.prediction) {
                    resultDiv.innerHTML = `
                        <p style="color: #555; font-size: 0.9rem;">Based on your soil parameters, the best crop is:</p>
                        <h2 style="color: var(--primary); font-size: 2.5rem; margin: 10px 0;">${result.prediction.toUpperCase()} 🌾</h2>
                        <div style="text-align: left; margin-top: 1.5rem; background: rgba(255,255,255,0.6); padding: 1rem; border-radius: 10px;">
                            <p style="margin-bottom: 0.8rem;"><strong>📝 Condition Analysis:</strong> ${result.description}</p>
                            <p style="margin-bottom: 0.8rem;"><strong>📈 ${result.yield_outcome}</strong></p>
                            <a href="${result.link}" target="_blank" style="color: var(--secondary); font-weight: bold; text-decoration: underline;">🔗 Click to Learn More & Research</a>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
                }
            } catch (error) {
                console.error('Error:', error);
            } finally {
                hideLoading(); // Hide loader
            }
        });
    }

    if (fertilizerForm) {
        fertilizerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            showLoading();
            document.getElementById('result').style.display = 'none';

            const formData = new FormData(fertilizerForm);
            const data = Object.fromEntries(formData);

            const numericFields = ['Temperature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous'];
            numericFields.forEach(field => {
                if (data[field]) data[field] = parseFloat(data[field]);
            });

            try {
                await new Promise(r => setTimeout(r, 800));

                const response = await fetch('/predict-fertilizer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });

                const result = await response.json();
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';

                if (result.prediction) {
                    resultDiv.innerHTML = `
                        <p style="color: #555; font-size: 0.9rem;">To maximize yield, we recommend:</p>
                        <h2 style="color: var(--secondary); font-size: 2.5rem; margin: 10px 0;">${result.prediction} 🧪</h2>
                        <div style="text-align: left; margin-top: 1.5rem; background: rgba(255,255,255,0.6); padding: 1rem; border-radius: 10px;">
                            <p style="margin-bottom: 0.8rem;"><strong>📝 Why this fertilizer?</strong> ${result.description}</p>
                            <p style="margin-bottom: 0.8rem;"><strong>📈 Impact:</strong> ${result.yield_outcome}</p>
                            <a href="${result.link}" target="_blank" style="color: var(--primary); font-weight: bold; text-decoration: underline;">🔗 Click to Learn More & Research</a>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
                }
            } catch (error) {
                console.error('Error:', error);
            } finally {
                hideLoading();
            }
        });
    }
});

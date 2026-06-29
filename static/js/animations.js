/**
 * FraudSense v2.1 - Animations Module
 * Manages numerical text count-ups, progress bar animations, and sequential loaders.
 */

const animations = {
  /**
   * Animates a numeric percentage value from 0 to target.
   * @param {string|HTMLElement} element - Target element or ID
   * @param {number} target - Target percentage value
   * @param {number} duration - Animation duration in ms
   */
  countUp(element, target, duration = 800) {
    const el = typeof element === 'string' ? document.getElementById(element) : element;
    if (!el) return;

    const start = 0;
    const end = Number(target ?? 0);
    if (start === end) {
      el.textContent = end.toFixed(1) + '%';
      return;
    }

    const startTime = performance.now();

    function update(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease out quad
      const ease = progress * (2 - progress);
      const current = start + (end - start) * ease;
      
      el.textContent = current.toFixed(1) + '%';

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = end.toFixed(1) + '%';
      }
    }

    requestAnimationFrame(update);
  },

  /**
   * Animates the linear confidence progress bar fill.
   * @param {number} confidence - Confidence percentage (0-100)
   */
  animateLinearMeter(confidence) {
    const fill = document.getElementById('conf-fill');
    if (!fill) return;

    const pct = Math.min(Math.max(Number(confidence ?? 0), 0), 100);
    fill.style.width = pct + '%';

    // Clear background styles
    fill.style.backgroundColor = '';
    
    // Set color based on ranges
    if (pct < 35) {
      fill.style.backgroundColor = 'var(--green)';
    } else if (pct < 70) {
      fill.style.backgroundColor = 'var(--orange)';
    } else if (pct < 90) {
      fill.style.backgroundColor = 'var(--orange)';
    } else {
      fill.style.backgroundColor = 'var(--red)';
    }
  },

  /**
   * Cycles loading step messages.
   * @param {Function} callback - Callback executed on load completion
   */
  showLoadingSequence(callback) {
    const loader = document.getElementById('loading-overlay');
    const results = document.getElementById('result-panel');
    const stepText = document.getElementById('loading-step-text');
    
    if (!loader) {
      if (callback) callback();
      return;
    }

    if (results) results.style.display = 'none';
    loader.style.display = 'flex';
    loader.classList.add('fade-in');

    const steps = [
      'Analyzing Transaction Data...',
      'Mapping card security parameters...',
      'Evaluating Random Forest & XGBoost nodes...',
      'Compiling final report...'
    ];
    
    let currentStep = 0;
    stepText.textContent = steps[0];

    const interval = setInterval(() => {
      currentStep++;
      if (currentStep < steps.length) {
        stepText.textContent = steps[currentStep];
      } else {
        clearInterval(interval);
        loader.style.display = 'none';
        if (callback) callback();
      }
    }, 400);
  }
};

// Export to window
window.animations = animations;
